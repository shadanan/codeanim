#!/usr/bin/env python3
from codeanim import chrome

# Bring Chrome to the front
chrome.activate()

# Create a new window
chrome.new_window()

# Resize the window
chrome.resize((0, 0), (800, 600))

# Navigate to the Codeanim GitHub repository
chrome.navigate("https://github.com/shadanan/codeanim")

# Open new tab and Navigate to the Friendly TL Channel
chrome.new_tab()
chrome.navigate("https://www.youtube.com/@FriendlyTL")

# Open Chrome DevTools
chrome.toggle_devtools()

# Select previous tab
chrome.previous_tab()

# Select next tab
chrome.next_tab()

# Refresh the page
chrome.refresh()

# Close the tab
chrome.close_tab()

# We're now on the CodeAnim page in the first tab. Navigate to a different page
chrome.navigate("https://www.youtube.com/@FriendlyTL")

# Go back
chrome.back()

# Go forward
chrome.forward()

# Close the window
chrome.close_window()
