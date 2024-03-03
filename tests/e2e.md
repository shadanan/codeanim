# End-to-End Tests

## VS Code Tests

```python codeanim vscode
vscode.open("demo")
vscode.resize((0, 25), (1024, 768))
```

Open the demo project, resize VS Code.

```python codeanim
vscode.newfile()
write('print("Hello, World!")\n')
vscode.save("scratch.py")
```

Create a new file, add hello world, and save it as scratch.py.

```python codeanim
vscode.toggle_terminal()
write("python3 scratch.py\n")
```

Execute the script using the terminal.

```python codeanim
vscode.focus_editor()
vscode.newline(1)
write("#!/usr/bin/env python3")
vscode.save()
```

Add Python shebang to the script and save it.

```python codeanim
vscode.palette(">python.execInTerminal")
```

Run the script using the palette command

## Chrome Tests

```python codeanim chrome
chrome.activate()
chrome.resize((50, 75), (1024, 768))
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
