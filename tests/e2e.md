# End-to-End Tests

Open the demo project, resize VS Code.

```python codeanim
# Open the demo project
vscode.open("demo")

# Resize VS Code
vscode.resize((0, 25), (1024, 768))

```

Create a new file and save it.

```python codeanim
# Create a new script
vscode.newfile()

# Insert print("Hello, World!") into scratch.py
write('print("Hello, World!")\n')
vscode.save("scratch.py")
```

Execute the script using the terminal

```python codeanim
vscode.focus_terminal()
write("python3 scratch.py\n")
```

Edit the script and save it.

```python codeanim
vscode.focus_editor()
vscode.newline(1)
write("#!/usr/bin/env python3\n")
vscode.save()
```

Run the script using palette

```python codeanim
# Execute the script
vscode.palette(">python.execInTerminal")
```
