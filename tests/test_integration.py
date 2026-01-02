"""Integration tests requiring actual VS Code and Chrome applications.

These tests are marked with @pytest.mark.integration and can be skipped with:
    pytest -m "not integration"

They require:
- macOS
- VS Code installed with 'code' CLI command
- Google Chrome installed
"""

import pyperclip
import pytest

from codeanim import Chrome, CodeAnim, Key, VSCode
from codeanim.interpolators import Sigmoid, Spring

pytestmark = pytest.mark.integration


@pytest.fixture
def ca() -> CodeAnim:
    return CodeAnim()


@pytest.fixture
def vscode(ca: CodeAnim) -> VSCode:
    return VSCode(ca)


@pytest.fixture
def chrome(ca: CodeAnim) -> Chrome:
    return Chrome(ca)


def test_vscode_activate_and_resize(vscode: VSCode):
    vscode.activate()
    vscode.resize(position=(100, 100), size=(1200, 800))


def test_vscode_command_palette(vscode: VSCode):
    vscode.activate()
    vscode.palette(">View: Zoom In")
    vscode.palette(">View: Zoom Out")


def test_chrome_activate_and_navigate(ca: CodeAnim, chrome: Chrome):
    chrome.activate()
    chrome.new_tab()
    chrome.navigate("example.com")
    ca.tap("a", modifiers=[Key.cmd])
    ca.tap("c", modifiers=[Key.cmd])
    chrome.close_tab()
    assert "Example Domain" in pyperclip.paste()


def test_smooth_mouse_movement(ca: CodeAnim):
    ca.move((600, 600), start=(200, 200), interpolator=Spring())
    ca.move((200, 200), interpolator=Sigmoid())


def test_full_demo_workflow(ca: CodeAnim, vscode: VSCode):
    vscode.activate()
    vscode.resize((100, 100), (1200, 800))
    vscode.palette(">workbench.action.files.newUntitledFile")
    ca.write("Hello, World!")

    ca.tap("a", modifiers=[Key.cmd])
    ca.tap("c", modifiers=[Key.cmd])

    # Close the tab
    vscode.clear_editor()
    ca.tap("w", modifiers=[Key.cmd])

    assert pyperclip.paste() == "Hello, World!"
