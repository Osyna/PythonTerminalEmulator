# PythonCMD Emulator

![PythonCMD Logo]([https://via.placeholder.com/150x150.png?text=PythonCMD](https://raw.githubusercontent.com/Osyna/PythonTerminalEmulator/main/cmd_screenshot.png))

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

PythonCMD is a powerful and customizable command-line interface emulator written in Python. It provides a rich set of built-in commands, support for custom commands, and a file management system, all wrapped in a user-friendly interface.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Built-in Commands](#built-in-commands)
- [Custom Commands](#custom-commands)
- [File Manager](#file-manager)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- 🚀 Easy-to-use command-line interface
- 🎨 Colorful and intuitive user interface
- 📁 Built-in file manager
- 🛠 Customizable command system
- 📜 Command history and search
- 🔧 Configurable aliases
- 📊 Interactive help system

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/pythoncmd.git
   ```
3. Navigate to the project directory:
   ```
   cd pythoncmd
   ```
4. Run the main script:
   ```
   python main.py
   ```

## Usage

To start PythonCMD, simply run the `main.py` script:

```
python main.py
```

You'll be greeted with a welcome screen and a command prompt. Type `help` to see a list of available commands.

## Built-in Commands

PythonCMD comes with a variety of built-in commands:

| Command | Description |
|---------|-------------|
| `cd <path>` | Change the current directory |
| `dir` / `ls` | List directory contents |
| `echo <text>` | Display a line of text |
| `pwd` | Print working directory |
| `cls` / `clear` | Clear the screen |
| `history` | Show command history |
| `alias <name> <command>` | Create a command alias |
| `help [command]` | Show help for all commands or a specific command |
| `exit` | Exit the program |
| `fm` | Open the file manager |
| `search <query>` | Search command history |

For more details on each command, use `help <command>` within PythonCMD.

## Custom Commands

PythonCMD allows you to create and manage custom commands:

- `addcmd`: Add a new custom command
- `rmcmd`: Remove a custom command
- `listcmd`: List all custom commands
- `refresh_commands`: Reload custom commands from the configuration file

### Adding a Custom Command

To add a custom command:

1. Use the `addcmd` command in PythonCMD.
2. Follow the prompts to enter the command name, the command to execute, help text, and any arguments.

Example:
```
> addcmd
Enter command name: greet
Enter command to execute: echo "Hello, $1!"
Enter help text: Greet a person
Enter argument names (space-separated): name
```

This creates a custom command `greet` that takes one argument `name` and echoes a greeting.

### Using Custom Commands

Once created, you can use custom commands just like built-in ones:

```
> greet Alice
Hello, Alice!
```

## File Manager

PythonCMD includes a built-in file manager. To access it, use the `fm` command. The file manager provides the following features:

- Navigate directories
- Copy, move, and delete files and directories
- Select multiple items for batch operations
- Toggle between list and grid view
- Sort items by name, size, or date

File Manager Commands:
- `cd <dir>`: Change directory
- `p`: Go to parent directory
- `v`: Toggle view mode (list/grid)
- `s <option>`: Change sort (name/size/date)
- `r`: Reverse sort order
- `sel <item>`: Select/deselect item
- `copy`: Copy selected items
- `move`: Move selected items
- `delete`: Delete selected items
- `q`: Quit file manager

## Configuration

PythonCMD uses a configuration file `commands.cfg` to store custom commands and aliases. This file is automatically created and updated as you add or modify custom commands and aliases.

You can manually edit this file, but be careful to maintain the correct syntax:

```ini
[command_name]
command = echo "This is a custom command"
help = Help text for the custom command
args = arg1 arg2
```

## Contributing

Contributions to PythonCMD are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Please ensure your code adheres to the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by Irvin aka Osyna

For issues, feature requests, or questions, please [open an issue](https://github.com/yourusername/pythoncmd/issues).
