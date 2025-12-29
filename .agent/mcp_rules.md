# MCP Global Rules

> Auto-copy this to `.agent/` or your AI agent's rules directory

## Required Behavior

1. **Before ANY coding task**, run:
   ```bash
   python mcp-global-rules/mcp.py autocontext
   ```

2. **Before modifying a file**, check impact:
   ```bash
   python mcp-global-rules/mcp.py impact <file>
   python mcp-global-rules/mcp.py predict-bugs <file>
   ```

3. **After making changes**, verify:
   ```bash
   python mcp-global-rules/mcp.py review <file>
   python mcp-global-rules/mcp.py security <file>
   ```

4. **Remember important decisions**:
   ```bash
   python mcp-global-rules/mcp.py remember "<key>" "<value>"
   ```

5. **Recall prior knowledge**:
   ```bash
   python mcp-global-rules/mcp.py recall "<query>"
   ```

## Command Shortcuts

Create alias `mcp` for convenience:
```bash
alias mcp="python mcp-global-rules/mcp.py"
```

Then use:
```bash
mcp autocontext
mcp search "query"
mcp remember "key" "value"
mcp recall "query"
mcp predict-bugs .
mcp review .
```

## Enforced via Git Hooks

These checks run automatically and WILL BLOCK commits that:
- Have HIGH bug risk
- Have CRITICAL security issues
- Fail code review with >5 errors

## Do NOT

- Skip the autocontext step
- Ignore predict-bugs warnings
- Bypass pre-commit hooks (--no-verify)
- Forget to use remember/recall
