# CodeAnim

CodeAnim is a tool to help you animate VS Code. It provides methods that enable you to type, move the cursor, and send commands to VS Code. It works by sending keystrokes using the pynput library.

## Installation

We recommend install CodeAnim using [pipx](https://pipx.pypa.io/).

```shell
pipx install codeanim
```

## Usage

CodeAnim runs commands from Markdown files where codeanim commands are enclosed in a `python codeanim` fence.

### Example

Create a Markdown file called `codeanim-markdown-demo.md` with the following contents:

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

### Flags

- Set `-v` or `--verbose` to enable verbose mode. Commands will be printed out as they are executed.
- Set `--live` to enable presentation mode. In this mode, a wait() will be injected after every codeanim fence.

## Development

We use Poetry for development.

```shell
git clone https://github.com/shadanan/codeanim.git
cd codeanim
poetry install
```

### Formatting

This project adopts the Ruff formatter and is enforced by a GitHub action.

### VS Code

Useful extensions when developing CodeAnim:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)

## Tests

There aren't any unit tests yet. In the tests folder, there is an end-to-end test that uses CodeAnim to open the `scratch.py` file, types out some code, and executes it. To run the test:

```sh
./e2e-test.sh
```

Then, validate that it worked by observing that the animation runs, types out:

```python
print("Hello, World!")
```

And executes the script.

## Limitations

CodeAnim currently only works on MacOS because of a dependency on AppleScript, which is used to switch to the VS Code window. Also, many of the commands send Mac specific keystrokes. With some effort, CodeAnim can be made to work on other platforms.
