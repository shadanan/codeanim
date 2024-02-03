#!/usr/bin/env python3
from codeanim import vscode

# Bring VS Code to the front
vscode.activate()

# Open myfile.py
vscode.focus("myfile.py")

# Insert print("Hello, World!") into myfile.py
vscode.write('print("Hello, World!")\n')

# Execute the script
vscode.run()
