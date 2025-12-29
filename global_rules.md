# MCP Global Rules for AI Agents

> Add this file to your AI agent's rules/instructions to enable MCP integration.

## MANDATORY: Use MCP Tools

Before any coding task, you MUST run these commands:

```bash
# Load context
python mcp-global-rules/mcp.py autocontext

# Search for relevant code
python mcp-global-rules/mcp.py search "your query"

# Check what you know
python mcp-global-rules/mcp.py recall "topic"
```

## Before Making Changes

```bash
# What will break?
python mcp-global-rules/mcp.py impact file.py

# Predict bugs
python mcp-global-rules/mcp.py predict-bugs file.py
```

## After Making Changes

```bash
# Code review
python mcp-global-rules/mcp.py review file.py

# Security check  
python mcp-global-rules/mcp.py security file.py

# Generate tests
python mcp-global-rules/mcp.py test-gen file.py --impl
```

## Remember Important Information

```bash
# Store knowledge for later
python mcp-global-rules/mcp.py remember "key" "value"

# Example: remember file locations
python mcp-global-rules/mcp.py remember "auth_handler" "src/auth/handler.py"
python mcp-global-rules/mcp.py remember "db_config" "Uses PostgreSQL, config in src/config/db.py"
```

## Recall Knowledge

```bash
# Search memories
python mcp-global-rules/mcp.py recall "authentication"
python mcp-global-rules/mcp.py recall "database"
```

## Available Commands (48)

| Category | Commands |
|----------|----------|
| Context | `autocontext`, `context`, `search`, `find` |
| Memory | `remember`, `recall`, `forget`, `learn` |
| Analysis | `review`, `security`, `profile`, `errors` |
| Prediction | `predict-bugs`, `risk-score`, `impact` |
| Testing | `test-gen`, `test`, `test-coverage` |
| Indexing | `index-all`, `todos`, `git-history` |

## Git Hooks (Automatic)

These run automatically on git operations:
- **pre-commit**: Blocks high-risk/insecure code
- **post-commit**: Updates learning and indexes
- **post-checkout**: Warms context for new branch

## Key Principle

**ALWAYS use MCP tools.** They provide context, prevent bugs, and learn from your work.

```bash
# Quick workflow
mcp autocontext              # Before coding
mcp impact file.py           # Before changes
mcp review file.py           # After changes
mcp remember "key" "value"   # Save learnings
```
