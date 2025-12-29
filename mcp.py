#!/usr/bin/env python3
"""
MCP Tools Runner
================
Single entry point for all MCP AI enhancement tools.
"""

import sys
from pathlib import Path

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
if str(SCRIPT_DIR / "scripts") not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def show_help():
    """Show help message."""
    print("""
MCP AI Enhancement Tools (45 Commands)
=======================================

Usage: python mcp.py <command> [args...]

Code Quality:
    review [path] [--strict]    Code review automation
    docs [path] [--write]       Generate missing docstrings
    test [path]                 Generate pytest test stubs  
    deadcode [path]             Find unused code
    fix [path] [--safe --apply] Auto-fix issues

Analysis:
    deps [path]                 Dependency analysis
    profile [path]              Performance/complexity
    security [path]             Security audit
    errors [path]               Error handling
    architecture [path]         Architecture validation

Intelligence:
    context "query" [path]      Smart context extraction
    find "query" [path]         Natural language search
    refactor [path]             Suggest refactorings

Indexes:
    index-all                   Full reindex (all 7)
    git-history [file]          Git commit history
    todos                       List TODOs/FIXMEs
    impact [file]               What breaks?
    test-coverage               Coverage data

AI Memory:
    remember "key" "value"      Store knowledge
    recall "query"              Search memories
    forget "key"                Remove memory
    learn [--patterns]          Learn from feedback

AI Prediction:
    predict-bugs [file]         Predict bugs
    risk-score                  Change risk score
    test-gen [file] --impl      Generate full tests

Multi-Repo:
    search-all "query"          Search all projects
    repos --add [path]          Manage repos

CI/CD:
    github-action               Generate workflow
    pipeline [--gitlab]         Generate pipeline

Automation:
    watch [path]                Live index updates
    autocontext                 Auto-load context
    warm                        Pre-warm indexes

Setup:
    setup --all                 Full setup
    setup --hooks               Install git hooks
    setup --profile             Install shell profile
""")


# Map commands to modules
COMMANDS = {
    # Original tools
    'test': 'auto_test',
    'docs': 'auto_docs',
    'deadcode': 'dead_code',
    'deps': 'deps',
    'summarize': 'summarize',
    'changelog': 'changelog',
    'review': 'review',
    # Phase 2 tools
    'context': 'context',
    'refactor': 'refactor',
    'apidocs': 'api_docs',
    'coverage': 'doc_coverage',
    'security': 'security',
    'profile': 'profile',
    'find': 'finder',
    'errors': 'errors',
    'migrate': 'migrate',
    'architecture': 'architecture',
    'arch': 'architecture',
    'fix': 'fix',
    # Semantic
    'index': 'vector_store',
    'search': 'vector_store',
    'pattern': 'astgrep',
    'parse': 'treesitter_utils',
    'embed': 'embeddings',
    # Automation
    'watch': 'watcher',
    'autocontext': 'autocontext',
    'auto': 'autocontext',
    # Advanced indexes
    'index-all': 'index_all',
    'git-history': 'git_index',
    'blame': 'git_index',
    'todos': 'todo_index',
    'impact': 'impact',
    'test-coverage': 'coverage_index',
    'doc-index': 'doc_index',
    'config-index': 'config_index',
    # AI Enhancements
    'remember': 'memory',
    'recall': 'memory',
    'forget': 'memory',
    'learn': 'learning',
    'predict-bugs': 'predict',
    'risk-score': 'predict',
    'search-all': 'multi_repo',
    'repos': 'multi_repo',
    'github-action': 'cicd',
    'pipeline': 'cicd',
    'test-gen': 'test_gen',
    # Setup & Automation
    'setup': 'setup',
    'warm': 'warm',
    'auto-learn': 'auto_learn',
}


def main():
    """Main entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ('help', '-h', '--help'):
        show_help()
        return 0
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command not in COMMANDS:
        print(f"[FAIL] Unknown command: {command}")
        show_help()
        return 1
    
    module_name = COMMANDS[command]
    
    try:
        module = __import__(f'scripts.{module_name}', fromlist=[module_name])
        sys.argv = [f'scripts/{module_name}.py'] + args
        
        if hasattr(module, 'main'):
            return module.main() or 0
        else:
            print(f"[FAIL] Module {module_name} has no main function")
            return 1
            
    except ImportError as e:
        print(f"[FAIL] Could not import {module_name}: {e}")
        return 1
    except Exception as e:
        print(f"[FAIL] Error running {command}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

