# CodeAnim

CodeAnim is a tool to help you animate VS Code. It provides methods that enable you to type, move the cursor, and send commands to VS Code. It works by sending keystrokes using the pynput library.

## Installation

Create a venv and then pip install CodeAnim from the GitHub repo:

```shell
python3 -m venv .venv
. .venv/bin/activate
pip install git+https://github.com/shadanan/codeanim
```

The run command uses a custom keybinding. Please add this to your `keybindings.json` file in VS Code:

```json
// Place your key bindings in this file to override the defaultsauto[]
[
  {
    "key": "ctrl+shift+alt+cmd+enter",
    "command": "python.execInTerminal"
  }
]
```

## Usage

There are two ways to use CodeAnim:

- As commands in a Markdown file
- Imported as a library and executed in a Python script

### Usage of CodeAnim CLI

Create a Markdown file and enclose codeanim commands in a `python codeanim` fence.

#### Example

Add this to `codeanim-markdown-demo.md`:

````markdown
# A Markdown Header

Some text to be read.

```python codeanim
# Bring VS Code to the front
vscode.activate()

# Open myfile.py
vscode.focus("myfile.py")

# Insert print("Hello, World!") into myfile.py
write('print("Hello, World!")\n')

# Execute the script
vscode.run()
```
````

To execute the CodeAnim commands in the Markdown file:

```shell
codeanim codeanim-markdown-demo.md
```

### Usage of CodeAnim Library

Import CodeAnim, and call the functions.

#### Example

Add this to `codeanim_script_demo.py`:

```python
#!/usr/bin/env python3
from codeanim import *

# Bring VS Code to the front
vscode.activate()

# Open myfile.py
vscode.focus("myfile.py")

# Insert print("Hello, World!") into myfile.py
write('print("Hello, World!")\n')

# Execute the script
vscode.run()
```

Execute your Python script:

```sh
./codeanim_script_demo.py
```

## Development

Clone the repo, create a venv, and install dependencies:

```shell
git clone https://github.com/shadanan/codeanim.git
cd codeanim
python3 -m venv .venv
pip install .
```

## Tests

There aren't any unit tests yet. In the tests folder, there is an end-to-end test that uses CodeAnim to open the `scratch.py` file, types out some code, and executes it. To run the test:

```sh
PYTHONPATH=src codeanim tests/e2e.md -v
```

Then, validate that it worked by observing that the animation runs, types out:

```python
print("Hello, World!")
```

And executes the script.

### VS Code Tests

```sh
PYTHONPATH=src tests/vscode.py
```

## Limitations

CodeAnim currently only works on MacOS because of a dependency on AppleScript, which is used to switch to the VS Code window. Also, many of the commands send Mac specific keystrokes. With some effort, CodeAnim can be made to work on other platforms.
