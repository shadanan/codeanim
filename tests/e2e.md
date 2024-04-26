# End-to-End Tests

## Mouse Tests

```python codeanim mouse
move((300, 300))
move((1200, 300), interpolator=Sigmoid())
move((1200, 900), interpolator=Sigmoid(speed=8))
move((300, 300), interpolator=Spring(gamma=8, omega=16))
```

Move the mouse around.

## VS Code Tests

```python codeanim vscode
vscode.open("demo")
vscode.resize((50, 50), (1024, 768))
```

Open the demo project, resize VS Code.

```python codeanim print
vscode.new_file()
write('print("Hello, World!")\n')
vscode.save("scratch.py")
```

Create a new file, add hello world, and save it as scratch.py.

```python codeanim drag
drag((150, 222), (1020, 222))
click((780, 102))
```

Open the script a second time in a separate pane, then close it.

```python codeanim run
click((985, 105))
move((985, 300))
```

Run the script by clicking the run button

```python codeanim terminal
vscode.toggle_terminal()
write("python3 scratch.py\n")
```

Execute the script using the terminal.

```python codeanim edit
vscode.focus_editor()
vscode.newline(1)
write("#!/usr/bin/env python3")
vscode.save()
```

Add Python shebang to the script and save it.

```python codeanim palette
vscode.palette(">python.execInTerminal")
```

Run the script using the palette command

## Chrome Tests

```python codeanim chrome
chrome.activate()
chrome.resize((75, 75), (1024, 768))
```

Activate Chrome and resize it.

```python codeanim
chrome.new_tab()
chrome.navigate("https://github.com/shadanan/codeanim")
```

Open a new tab and navigate to the Codeanim GitHub repository.

```python codeanim
chrome.navigate("https://www.youtube.com/@FriendlyTL")
```

Navigate to the Friendly TL YouTube channel.

```python codeanim
chrome.back()
chrome.forward()
chrome.previous_tab()
chrome.next_tab()
chrome.refresh()
chrome.close_tab()
```
