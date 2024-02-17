#!/usr/bin/env python3
from codeanim import vscode, wait, write

# Bring VS Code to the front
vscode.activate()

# Wait for shift to be pressed
wait()

# Resize VS Code to 800x600
vscode.resize((0, 25), (800, 600))

# Open scratch.py
vscode.focus("scratch.py")

# Insert print("Hello, World!") into scratch.py
write('print("Hello, World!")\n')

# Execute the script
vscode.run()
