"""
Auto-Context Loader
===================
Automatically load relevant code context for AI agents.

Usage:
    python mcp.py context --auto      # Get auto-loaded context
    python mcp.py context --recent    # Context from recent files
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import Counter

from .utils import Console, find_project_root


@dataclass
class ContextCache:
    """Cache of context state."""
    recent_files: List[str] = field(default_factory=list)
    hot_files: Dict[str, int] = field(default_factory=dict)  # path -> access count
    last_query: str = ""
    last_task: str = ""
    timestamp: str = ""
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ContextCache':
        return cls(**data)


@dataclass
class ContextResult:
    """Result of context loading."""
    files: List[Tuple[str, str]]  # (path, content summary)
    token_count: int
    source: str  # 'recent', 'semantic', 'dependency'


def get_cache_path(root: Path = None) -> Path:
    """Get path to context cache."""
    root = root or find_project_root() or Path.cwd()
    return root / '.mcp' / 'memory' / 'context_cache.json'


def load_cache(root: Path = None) -> ContextCache:
    """Load context cache from disk."""
    cache_path = get_cache_path(root)
    
    if cache_path.exists():
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return ContextCache.from_dict(data)
        except Exception:
            pass
    
    return ContextCache()


def save_cache(cache: ContextCache, root: Path = None):
    """Save context cache to disk."""
    cache_path = get_cache_path(root)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    cache.timestamp = datetime.utcnow().isoformat() + 'Z'
    
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(cache.to_dict(), f, indent=2)


def track_file_access(path: Path, root: Path = None):
    """Track that a file was accessed."""
    cache = load_cache(root)
    
    path_str = str(path)
    
    # Update recent files (max 20)
    if path_str in cache.recent_files:
        cache.recent_files.remove(path_str)
    cache.recent_files.insert(0, path_str)
    cache.recent_files = cache.recent_files[:20]
    
    # Update hot files
    cache.hot_files[path_str] = cache.hot_files.get(path_str, 0) + 1
    
    save_cache(cache, root)


def get_recent_context(
    limit: int = 5,
    max_lines: int = 50,
    root: Path = None
) -> ContextResult:
    """Get context from recently accessed files."""
    cache = load_cache(root)
    root = root or find_project_root() or Path.cwd()
    
    files = []
    token_count = 0
    
    for file_path in cache.recent_files[:limit]:
        path = Path(file_path)
        if not path.is_absolute():
            path = root / path
        
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:max_lines]
                    content = ''.join(lines)
                    files.append((str(path), content))
                    token_count += len(content.split())
            except Exception:
                pass
    
    return ContextResult(files=files, token_count=token_count, source='recent')


def get_hot_context(
    limit: int = 5,
    max_lines: int = 50,
    root: Path = None
) -> ContextResult:
    """Get context from most frequently accessed files."""
    cache = load_cache(root)
    root = root or find_project_root() or Path.cwd()
    
    # Sort by access count
    sorted_files = sorted(cache.hot_files.items(), key=lambda x: x[1], reverse=True)
    
    files = []
    token_count = 0
    
    for file_path, _ in sorted_files[:limit]:
        path = Path(file_path)
        if not path.is_absolute():
            path = root / path
        
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:max_lines]
                    content = ''.join(lines)
                    files.append((str(path), content))
                    token_count += len(content.split())
            except Exception:
                pass
    
    return ContextResult(files=files, token_count=token_count, source='hot')


def get_semantic_context(
    query: str,
    limit: int = 5,
    root: Path = None
) -> ContextResult:
    """Get context via semantic search."""
    root = root or find_project_root() or Path.cwd()
    
    files = []
    token_count = 0
    
    try:
        from .vector_store import VectorStore
        store = VectorStore(root / '.mcp' / 'vector_index')
        
        if store.load():
            results = store.search(query, k=limit)
            
            for result in results:
                files.append((result.chunk.path, result.chunk.content))
                token_count += len(result.chunk.content.split())
    except Exception:
        pass
    
    # Update cache with query
    cache = load_cache(root)
    cache.last_query = query
    save_cache(cache, root)
    
    return ContextResult(files=files, token_count=token_count, source='semantic')


def get_dependency_context(
    file_path: Path,
    root: Path = None
) -> ContextResult:
    """Get context from file dependencies (imports)."""
    root = root or find_project_root() or Path.cwd()
    
    files = []
    token_count = 0
    
    try:
        from .treesitter_utils import parse_file
        parsed = parse_file(file_path)
        
        for imp in parsed.imports:
            # Try to resolve import to file
            parts = imp.replace('from ', '').replace('import ', '').split()[0].split('.')
            
            for i in range(len(parts), 0, -1):
                possible_path = root / '/'.join(parts[:i]) + '.py'
                if possible_path.exists():
                    try:
                        with open(possible_path, 'r', encoding='utf-8') as f:
                            content = f.read()[:2000]
                            files.append((str(possible_path), content))
                            token_count += len(content.split())
                    except Exception:
                        pass
                    break
    except Exception:
        pass
    
    return ContextResult(files=files, token_count=token_count, source='dependency')


def get_auto_context(
    task: str = "",
    token_budget: int = 4000,
    root: Path = None
) -> str:
    """Get automatically loaded context for AI agent."""
    root = root or find_project_root() or Path.cwd()
    
    all_files: Dict[str, str] = {}
    tokens_used = 0
    
    # 1. Recent files (highest priority)
    recent = get_recent_context(limit=3, root=root)
    for path, content in recent.files:
        if tokens_used + len(content.split()) < token_budget:
            all_files[path] = content
            tokens_used += len(content.split())
    
    # 2. Semantic search if task provided
    if task and tokens_used < token_budget:
        semantic = get_semantic_context(task, limit=3, root=root)
        for path, content in semantic.files:
            if path not in all_files and tokens_used + len(content.split()) < token_budget:
                all_files[path] = content
                tokens_used += len(content.split())
    
    # 3. Hot files
    if tokens_used < token_budget:
        hot = get_hot_context(limit=2, root=root)
        for path, content in hot.files:
            if path not in all_files and tokens_used + len(content.split()) < token_budget:
                all_files[path] = content
                tokens_used += len(content.split())
    
    # Format output
    output = ["# Auto-Loaded Context", f"# Files: {len(all_files)} | Tokens: ~{tokens_used}", ""]
    
    for path, content in all_files.items():
        output.append(f"## {Path(path).name}")
        output.append(f"# {path}")
        output.append("```python")
        output.append(content[:1500])
        output.append("```")
        output.append("")
    
    return '\n'.join(output)


def update_task(task: str, root: Path = None):
    """Update current task in cache."""
    cache = load_cache(root)
    cache.last_task = task
    save_cache(cache, root)


def main():
    """CLI entry point."""
    Console.header("Auto-Context Loader")
    
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    
    root = find_project_root() or Path.cwd()
    
    if '--recent' in sys.argv:
        result = get_recent_context(root=root)
        Console.info(f"Recent files: {len(result.files)}")
        for path, _ in result.files:
            print(f"  - {path}")
        return 0
    
    if '--hot' in sys.argv:
        result = get_hot_context(root=root)
        Console.info(f"Hot files: {len(result.files)}")
        for path, _ in result.files:
            print(f"  - {path}")
        return 0
    
    if '--auto' in sys.argv or not args:
        task = ' '.join(args) if args else ""
        context = get_auto_context(task=task, root=root)
        print(context)
        return 0
    
    # Semantic search with query
    query = ' '.join(args)
    result = get_semantic_context(query, root=root)
    
    Console.info(f"Found {len(result.files)} relevant files for: {query}")
    for path, content in result.files:
        print(f"\n## {path}")
        print(content[:500])
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
