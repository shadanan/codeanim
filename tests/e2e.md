# A Markdown Header

Some text to be read.

```python codeanim
# Bring VS Code to the front
vscode.activate()

# Open scratch.py
vscode.focus("scratch.py")

# Insert print("Hello, World!") into scratch.py
write('print("Hello, World!")\n')
```

If `codeanim` is executed with the `--live` command, a wait() will be inserted here.

```python codeanim
# Execute the script
vscode.run()
```
