# MCP Global Rules for AI Agents

> Add this file to your AI agent's rules/instructions to enable MCP integration.

---

## IMPORTANT: How to Run MCP Commands

Find the mcp.py file in the project and run with python3:

```bash
# First, find where mcp-global-rules is installed
find . -name "mcp.py" -path "*/mcp-global-rules/*" 2>/dev/null

# Then run commands using the full path, for example:
python3 ./mcp-global-rules/mcp.py <command>

# Or if installed elsewhere:
python3 /path/to/mcp-global-rules/mcp.py <command>
```

The mcp.py script will auto-detect its location and work correctly.

---

## CORE PRINCIPLES

### Fix Properly, Never Disable

Fix properly, never disable, never restrict or reduce capabilities of this program. ALWAYS FIX CORRECTLY AND FULLY AND COMPLETELY TO MAKE EVERYTHING WORK FULLY! All integrations, improvements, and adaptations must utilize what already exists and add on to it, never bypassing anything that we have intentionally developed and integrated. Unless explicitly requested by the user for a specific change that goes against this, you must always obey these rules.

### No Emojis or Icons in Code

Do NOT use emojis or icons in any code unless explicitly requested by the user or defined in the README.md file. Emojis and icons cause code errors and are not always the same between devices.

---

## TRIGGER COMMANDS

### "dev" - Autonomous Development Mode

When the user says only **"dev"**, you MUST:

1. **Find and Run MCP Tools**
   ```bash
   # Find mcp.py location
   MCP=$(find . -name "mcp.py" -path "*/mcp-global-rules/*" 2>/dev/null | head -1)
   
   # Load context
   python3 $MCP autocontext
   python3 $MCP recall "project"
   ```

2. **Read README.md as Single Source of Truth**
   - README.md defines what the project should do
   - README.md contains the development roadmap
   - All decisions must align with README.md

3. **Identify Development Tasks**
   ```bash
   python3 $MCP todos
   python3 $MCP recall "tasks"
   ```

4. **Identify Gaps**
   - Compare README.md goals vs current implementation
   - Check for missing features
   - Check for incomplete integrations

5. **Continue Development Autonomously**
   - Implement next priority task from README.md
   - NO human intervention required
   - Follow "fix properly" principle
   - Commit progress incrementally

### "go" - Context and Suggestions Mode

When the user says only **"go"**, you MUST:

1. **Find and Run MCP Tools** (same as "dev")
   ```bash
   MCP=$(find . -name "mcp.py" -path "*/mcp-global-rules/*" 2>/dev/null | head -1)
   python3 $MCP autocontext
   python3 $MCP recall "project"
   ```

2. **Read README.md as Single Source of Truth**

3. **Identify Development Tasks and Gaps**
   ```bash
   python3 $MCP todos
   ```

4. **STOP - Do NOT Make Changes**
   - Present findings to user
   - List suggested next steps
   - Wait for user direction on which task to proceed with

5. **Provide Suggestions**
   - What needs to be done
   - Priority order
   - Estimated complexity
   - Ask user which to proceed with

---

## MANDATORY: Use MCP Tools

Before any coding task, you MUST:

1. **Find MCP location**
   ```bash
   MCP=$(find . -name "mcp.py" -path "*/mcp-global-rules/*" 2>/dev/null | head -1)
   ```

2. **Load context**
   ```bash
   python3 $MCP autocontext
   ```

3. **Search for relevant code**
   ```bash
   python3 $MCP search "your query"
   ```

4. **Check what you know**
   ```bash
   python3 $MCP recall "topic"
   ```

## Before Making Changes

```bash
# What will break?
python3 $MCP impact file.py

# Predict bugs
python3 $MCP predict-bugs file.py
```

## After Making Changes

```bash
# Code review
python3 $MCP review file.py

# Security check  
python3 $MCP security file.py

# Generate tests
python3 $MCP test-gen file.py --impl
```

## Remember Important Information

```bash
# Store knowledge for later
python3 $MCP remember "key" "value"

# Example: remember file locations
python3 $MCP remember "auth_handler" "src/auth/handler.py"
```

## Recall Knowledge

```bash
# Search memories
python3 $MCP recall "authentication"
```

---

## Available Commands (48)

| Category | Commands |
|----------|----------|
| Context | `autocontext`, `context`, `search`, `find` |
| Memory | `remember`, `recall`, `forget`, `learn` |
| Analysis | `review`, `security`, `profile`, `errors` |
| Prediction | `predict-bugs`, `risk-score`, `impact` |
| Testing | `test-gen`, `test`, `test-coverage` |
| Indexing | `index-all`, `todos`, `git-history` |

---

## Git Hooks (Automatic)

These run automatically on git operations:
- **pre-commit**: Blocks high-risk/insecure code
- **post-commit**: Updates learning and indexes
- **post-checkout**: Warms context for new branch

---

## Summary

| Trigger | Behavior |
|---------|----------|
| `dev` | Autonomous development, no intervention needed |
| `go` | Context + suggestions, wait for user direction |

**README.md is the single source of truth for project development.**

**ALWAYS use MCP tools. They provide context, prevent bugs, and learn from your work.**
