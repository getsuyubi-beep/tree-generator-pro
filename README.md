📂 Project Tree Generator Pro
Developed by L.DOUADI

A professional, lightweight, and modern desktop application built with Python and PyQt5. This tool allows developers to visualize their project's folder structure instantly and export it to a clean .txt file.

✨ Features
Modern Dark UI: A sleek, "Soft-Dark" interface designed for comfort and clarity.

Interactive Ignore List: Automatically detects sub-folders and lets you choose which ones to exclude (e.g., node_modules, .git, .next) using a large, user-friendly checklist.

Dual Browse Buttons: Easily select your source project folder and your preferred output destination.

Recursive Mapping: Deeply scans all directories to provide a complete architecture map.

Custom Output: Choose your own file name and export path.

Glassmorphism Design: Featuring a "Soft About Box" for a premium look and feel.

🚀 How to Use
Select Project: Click "Browse" to pick the folder you want to scan.

Filter Folders: In the large central list, check the folders you want to Ignore.

Set Destination: Choose where to save the result and give it a name.

Run: Click "Generate Architecture" and you're done!

🛠️ Built With
Python 3.x

PyQt5 (GUI Framework)

OS Module (File system navigation)

Installation & Setup
If you want to run the script manually:

Bash
# Clone the repository
git clone https://github.com/getsuyubi-beep/tree-generator-pro

# Install dependencies
pip install PyQt5

# Run the app
python tree_app.py

Export Example
The output file will look like this:

Plaintext
STRUCTURE: C:/MyProject
========================================
+-- [src]
|   +-- [components]
|   |   |-- Header.jsx
|   |   |-- Footer.jsx
|   |-- App.js
|-- package.json
|-- README.md
========================================
By L.DOUADI
