#!/usr/bin/env python3
from codeanim import vscode, write

# Bring VS Code to the front
vscode.activate()

# Open scratch.py
vscode.focus("scratch.py")

# Insert print("Hello, World!") into scratch.py
write('print("Hello, World!")\n')

# Execute the script
vscode.run()
