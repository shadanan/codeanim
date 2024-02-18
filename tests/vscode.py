#!/usr/bin/env python3
from codeanim import KeyMonitor, vscode, write

# Start the key monitor
monitor = KeyMonitor()
monitor.start()

# Bring VS Code to the front
vscode.activate()

# Wait for shift to be pressed
monitor.wait()

# Resize VS Code to 800x600
vscode.resize((0, 25), (800, 600))

# Open scratch.py
vscode.focus("scratch.py")

# Insert print("Hello, World!") into scratch.py
write('print("Hello, World!")\n')

# Execute the script
vscode.run()

# Stop the key monitor
monitor.stop()
