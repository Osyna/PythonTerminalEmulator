import os
import sys
import time
import subprocess
from typing import List, Optional
import shutil
import datetime
import configparser


class Style:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'    
    BACKGROUND_BLUE = '\033[44m'
    BACKGROUND_GREEN = '\033[42m'
    BACKGROUND_RED = '\033[41m'
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    NORMAL = '\033[22m'


class Argument:
    def __init__(self, name: str, required: bool = True, default: Optional[str] = None):
        self.name = name
        self.required = required
        self.default = default

class Command:
    def __init__(self, name: str, function, help_text: str, arguments: List[Argument] = None):
        self.name = name
        self.function = function
        self.help_text = help_text
        self.arguments = arguments or []

    def execute(self, *args):
        try:
            if len(args) < sum(1 for arg in self.arguments if arg.required):
                return self.get_help()
            
            # Apply default values for optional arguments
            args = list(args) + [arg.default for arg in self.arguments[len(args):] if not arg.required]
            
            return self.function(*args)
        except Exception as e:
            return f"Error executing {self.name}: {str(e)}"

    def get_help(self):
        arg_help = " ".join(f"<{arg.name}>" if arg.required else f"[{arg.name}]" for arg in self.arguments)
        return f"{self.name} {arg_help}\n  {self.help_text}\n" + \
               "\n".join(f"  {arg.name}: {'Required' if arg.required else 'Optional, default: ' + str(arg.default)}" 
                         for arg in self.arguments)

class PythonCMD:
    def __init__(self):
        self.history = []
        self.aliases = {}
        self.commands = {}
        self.config_file = "commands.cfg"
        self.register_commands()
        self.load_config()
        self.custom_commands = {}
        self.load_custom_commands()

    def register_commands(self):
        self.add_command(
            "cd", self.change_directory, "Change directory",
            [Argument("path", required=False, default=".")]
        )
        self.add_command("dir", self.list_directory, "List directory contents")
        self.add_command("ls", self.list_directory, "List directory contents")
        self.add_command(
            "echo", self.echo, "Display a line of text",
            [Argument("text", required=False, default="")]
        )
        self.add_command("pwd", self.print_working_directory, "Print working directory")
        self.add_command("cls", self.clear_screen, "Clear the screen")
        self.add_command("clear", self.clear_screen, "Clear the screen")
        self.add_command("history", self.show_history, "Show command history")
        self.add_command(
            "alias", self.create_alias, "Create an alias",
            [Argument("name"), Argument("command")]
        )
        self.add_command("help", self.show_help, "Show help")
        self.add_command("exit", self.exit, "Exit the program")
        self.add_command("fm", self.file_manager, "Open file manager")
        self.add_command(
            "search", self.search_history, "Search command history",
            [Argument("query")]
        )
        
        self.add_command("addcmd", self.add_custom_command_interactive, "Add a new custom command")
        self.add_command("rmcmd", self.remove_custom_command, "Remove a custom command")
        self.add_command("listcmd", self.list_custom_commands, "List all custom commands")
        self.add_command("refresh_commands", self.refresh_commands, "Reload custom commands from commands.cfg")

    def add_command(self, name, function, help_text, arguments=None):
        self.commands[name] = Command(name, function, help_text, arguments)

    def add_custom_command_interactive(self):
        name = input("Enter command name: ").strip()
        command = input("Enter command to execute: ").strip()
        help_text = input("Enter help text: ").strip()
        args = input("Enter argument names (space-separated): ").strip().split()
        self.add_custom_command(name, command, help_text, args)
        return f"{Style.GREEN}Custom command '{name}' added successfully.{Style.RESET}"

    def list_custom_commands(self):
        if not self.custom_commands:
            return f"{Style.YELLOW}No custom commands defined.{Style.RESET}"
        return "\n".join(f"{name}: {cmd.help_text}" for name, cmd in self.custom_commands.items())

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        self.aliases[key] = value

    def save_config(self):
        with open(self.config_file, 'w') as f:
            for key, value in self.aliases.items():
                f.write(f"{key}={value}\n")

    def print_colored(self, text, color):
        print(f"{color}{text}{Style.RESET}")

    def print_typewriter(self, text, delay=0.002):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def display_header(self):
        term_width = os.get_terminal_size().columns
        header = f"{Style.BACKGROUND_BLUE}{Style.WHITE}{Style.BOLD} Python CMD Emulator {Style.RESET}"
        print(header.center(term_width))
        print(f"{Style.YELLOW}{'─' * term_width}{Style.RESET}")

    def display_status(self):
        term_width = os.get_terminal_size().columns
        current_dir = os.getcwd()
        status = f"{Style.CYAN}Dir: {current_dir} | History: {len(self.history)} | Aliases: {len(self.aliases)}{Style.RESET}"
        print(status.ljust(term_width))
  
    def print_centered(self, text):
        terminal_width = 80  # Assuming a default width
        for line in text.split('\n'):
            print(line.center(terminal_width))

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        return ""

    def change_directory(self, path="."):
        try:
            os.chdir(os.path.expanduser(path))
            return f"Changed directory to {os.getcwd()}"
        except Exception as e:
            return f"Error changing directory: {str(e)}"

    def list_directory(self):
        try:
            files = os.listdir()
            return "\n".join([f"{Style.BLUE if os.path.isdir(f) else Style.GREEN}{f}{Style.RESET}" for f in files])
        except Exception as e:
            return f"Error listing directory: {str(e)}"

    def echo(self, text=""):
        return text

    def print_working_directory(self):
        return os.getcwd()

    def show_history(self):
        return "\n".join(f"{Style.YELLOW}{i}{Style.RESET}: {cmd}" for i, cmd in enumerate(self.history, 1))

    def create_alias(self, name, command):
        self.aliases[name] = command
        self.save_config()
        return f"Alias created: {name} -> {command}"

    def show_help(self, command=None):
        if command:
            if command in self.commands:
                return self.format_command_help(self.commands[command])
            elif command in self.custom_commands:
                return self.format_command_help(self.custom_commands[command])
            else:
                return f"{Style.RED}No help available for '{command}'.{Style.RESET}"
        
        term_width = shutil.get_terminal_size().columns
        
        help_text = self.create_header("PYTHON CMD EMULATOR HELP", term_width)
        
        help_text += self.format_command_section("Base Commands", self.commands)
        
        if self.custom_commands:
            help_text += self.format_command_section("Custom Commands", self.custom_commands)
        
        help_text += f"\n{Style.CYAN}For more information on a specific command, type: {Style.BOLD}help <command>{Style.RESET}\n"
        help_text += "=" * term_width + "\n"
        
        return help_text

    def create_header(self, text, width):
        padding = "=" * ((width - len(text) - 2) // 2)
        return f"\n{Style.BOLD}{Style.BLUE}{padding} {text} {padding}{Style.RESET}\n\n"

    def format_command_section(self, title, commands):
        section = f"{Style.YELLOW}{title}:{Style.RESET}\n"
        max_name_length = max(len(cmd.name) for cmd in commands.values())
        for cmd in commands.values():
            if cmd.name != 'help':
                section += f"  {Style.GREEN}{cmd.name.ljust(max_name_length)}{Style.RESET} : {cmd.help_text}\n"
        return section + "\n"

    def format_command_help(self, command):
        term_width = shutil.get_terminal_size().columns
        help_text = self.create_header(f"HELP: {command.name.upper()}", term_width)
        help_text += f"{Style.CYAN}Usage:{Style.RESET} {command.name} "
        help_text += " ".join(f"<{arg.name}>" if arg.required else f"[{arg.name}]" for arg in command.arguments)
        help_text += f"\n\n{Style.YELLOW}Description:{Style.RESET}\n  {command.help_text}\n\n"
        
        if command.arguments:
            help_text += f"{Style.MAGENTA}Arguments:{Style.RESET}\n"
            for arg in command.arguments:
                status = f"{Style.GREEN}Required{Style.RESET}" if arg.required else f"{Style.BLUE}Optional{Style.RESET}"
                default = f" (Default: {arg.default})" if arg.default is not None else ""
                help_text += f"  {Style.BOLD}{arg.name}{Style.RESET}: {status}{default}\n"
        
        return help_text

    def display_welcome(self):
        self.clear_screen()
        term_width = os.get_terminal_size().columns
        
        welcome_text = [
            f"{Style.BOLD}{Style.BLUE}╔{'═' * (term_width - 2)}╗{Style.RESET}",
            f"{Style.BOLD}{Style.BLUE}║{' ' * (term_width - 2)}║{Style.RESET}",
            f"{Style.BOLD}{Style.BLUE}║{Style.GREEN}{'Welcome to the Python CMD Emulator'.center(term_width - 2)}{Style.BLUE}║{Style.RESET}",
            f"{Style.BOLD}{Style.BLUE}║{' ' * (term_width - 2)}║{Style.RESET}",
            f"{Style.BOLD}{Style.BLUE}╚{'═' * (term_width - 2)}╝{Style.RESET}",
        ]
        
        for line in welcome_text:
            self.print_typewriter(line)
        
        print(f"\n{Style.CYAN}Type 'help' for a list of commands.{Style.RESET}\n")
   
    def exit(self):
        self.print_typewriter(f"{Style.GREEN}Thank you for using Advanced Python CMD. Goodbye!{Style.RESET}")
        sys.exit(0)

    def file_manager(self):
        fm = FileManager()
        return fm.run()

    def search_history(self, query):
        results = [cmd for cmd in self.history if query in cmd]
        return "\n".join(f"{Style.YELLOW}{i}{Style.RESET}: {cmd}" for i, cmd in enumerate(results, 1))

    def run(self):
        self.display_welcome()
        
        while True:
            try:
                current_dir = os.getcwd()
                user_input = input(f"{Style.BOLD}{Style.BLUE}┌─[{current_dir}]\n└─▶ {Style.RESET}")
                
                if user_input.strip():
                    commands = user_input.split('&&')
                    for cmd in commands:
                        cmd = cmd.strip()
                        self.history.append(cmd)
                        output = self.execute_command(cmd)
                        if output:
                            print(f"\n{output}\n")
            except KeyboardInterrupt:
                print(f"\n{Style.YELLOW}Use 'exit' to quit.{Style.RESET}")
            except EOFError:
                self.exit()

    def execute_command(self, command):
        parts = command.split()
        cmd_name = parts[0]
        args = parts[1:]

        if cmd_name in self.aliases:
            return self.execute_command(self.aliases[cmd_name] + ' ' + ' '.join(args))

        if cmd_name in self.commands:
            return self.commands[cmd_name].execute(*args)
        elif cmd_name in self.custom_commands:
            return self.custom_commands[cmd_name].execute(*args)
        else:
            try:
                result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=30)
                return self.format_command_output(result.stdout, result.stderr)
            except subprocess.TimeoutExpired:
                return f"{Style.RED}Command execution timed out after 30 seconds.{Style.RESET}"
            except Exception as e:
                return f"{Style.RED}Error executing command: {str(e)}{Style.RESET}"
            
    def format_command_output(self, stdout, stderr):
        output = ""
        if stdout:
            output += f"{Style.GREEN}Command Output:{Style.RESET}\n{stdout}\n"
        if stderr:
            output += f"{Style.RED}Error Output:{Style.RESET}\n{stderr}\n"
        return output.strip()

    def exit(self):
        term_width = os.get_terminal_size().columns
        goodbye_msg = f"{Style.GREEN}Thank you for using Python CMD Emulator. Goodbye!{Style.RESET}"
        print(goodbye_msg.center(term_width))
        sys.exit(0)

    def load_custom_commands(self):
        config = configparser.ConfigParser()
        successful_loads = 0
        failed_commands = []

        if os.path.exists(self.config_file):
            config.read(self.config_file, encoding='utf-8')
            for section in config.sections():
                try:
                    name = section
                    command = config.get(section, 'command', raw=True)
                    help_text = config.get(section, 'help', fallback='No help available')
                    args = config.get(section, 'args', fallback='').split()
                    self.custom_commands[name] = CustomCommand(name, command, help_text, args)
                    successful_loads += 1
                except configparser.InterpolationSyntaxError as e:
                    failed_commands.append((name, "Syntax error in command string"))
                except configparser.Error as e:
                    failed_commands.append((name, f"Configuration error: {str(e)}"))
                except Exception as e:
                    failed_commands.append((name, f"Unexpected error: {str(e)}"))

            print(f"{Style.GREEN}Successfully loaded {successful_loads} custom command(s).{Style.RESET}")
            
            if failed_commands:
                print(f"{Style.YELLOW}The following commands failed to load:{Style.RESET}")
                for name, error in failed_commands:
                    print(f"{Style.RED}- {name}: {error}{Style.RESET}")
                print(f"{Style.YELLOW}Please check your {self.config_file} file and correct these issues.{Style.RESET}")
        else:
            print(f"{Style.YELLOW}No {self.config_file} file found. Custom commands will not be loaded.{Style.RESET}")

        return successful_loads, failed_commands

    def save_custom_commands(self):
        config = configparser.ConfigParser()
        for name, cmd in self.custom_commands.items():
            config[name] = {
                'command': cmd.command,
                'help': cmd.help_text,
                'args': ' '.join(cmd.args)
            }
        with open('commands.cfg', 'w') as configfile:
            config.write(configfile)

    def add_custom_command(self, name, command, help_text, args):
        self.custom_commands[name] = CustomCommand(name, command, help_text, args)
        self.save_custom_commands()

    def remove_custom_command(self, name):
        if name in self.custom_commands:
            del self.custom_commands[name]
            self.save_custom_commands()

    def refresh_commands(self):
        print(f"{Style.CYAN}Refreshing custom commands...{Style.RESET}")
        self.custom_commands.clear()
        successful_loads, failed_commands = self.load_custom_commands()
        return f"Refresh complete. {successful_loads} commands loaded successfully."

class CustomCommand:
    def __init__(self, name, command, help_text, args=None):
        self.name = name
        self.command = command
        self.help_text = help_text
        self.args = args or []

    def execute(self, *args):
        try:
            # Replace placeholders in the command with actual arguments
            cmd = self.command
            for i, arg in enumerate(args):
                cmd = cmd.replace(f'${i+1}', arg)
            
            # Check if the command is a Python one-liner
            if cmd.startswith('python -c'):
                # Execute Python code directly
                exec_globals = {}
                exec(cmd[10:].strip('"'), exec_globals)
                return str(exec_globals.get('result', ''))
            else:
                # Execute as a system command
                result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
                return result.stdout + result.stderr
        except Exception as e:
            return f"{Style.RED}Error executing command: {str(e)}{Style.RESET}"

    def get_help(self):
        args_help = ' '.join(f'<{arg}>' for arg in self.args)
        return f"{self.name} {args_help}\n  {self.help_text}"

class FileManager:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.selected_items = set()
        self.view_mode = 'list'  # 'list' or 'grid'
        self.sort_by = 'name'    # 'name', 'size', 'date'
        self.reverse_sort = False

    def run(self):
        while True:
            self.display_interface()
            command = input(f"{Style.BOLD}{Style.GREEN}File Manager>{Style.RESET} ").strip().lower()
            if command == 'q':
                break
            elif command == 'p':
                self.current_dir = os.path.dirname(self.current_dir)
            elif command.startswith('cd '):
                self.change_directory(command[3:])
            elif command == 'v':
                self.toggle_view_mode()
            elif command.startswith('s '):
                self.change_sort(command[2:])
            elif command == 'r':
                self.reverse_sort = not self.reverse_sort
            elif command.startswith('sel '):
                self.toggle_selection(command[4:])
            elif command == 'copy':
                self.copy_selected()
            elif command == 'move':
                self.move_selected()
            elif command == 'delete':
                self.delete_selected()
            elif command == 'help':
                self.show_help()
        return f"File manager closed. Current directory: {self.current_dir}"

    def display_interface(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Style.BACKGROUND_BLUE}{Style.BRIGHT}{'File Manager':^80}{Style.RESET}")
        print(f"{Style.YELLOW}Current Directory: {self.current_dir}{Style.RESET}")
        print(f"{Style.CYAN}View: {self.view_mode.capitalize()} | Sort: {self.sort_by.capitalize()} ({'Desc' if self.reverse_sort else 'Asc'}){Style.RESET}")
        print("─" * 80)

        items = self.get_sorted_items()
        if self.view_mode == 'list':
            self.display_list_view(items)
        else:
            self.display_grid_view(items)

        print("─" * 80)
        print(f"{Style.GREEN}Commands: cd <dir>, p (parent), v (toggle view), s <name|size|date>, r (reverse sort){Style.RESET}")
        print(f"{Style.GREEN}sel <item> (select), copy, move, delete, q (quit), help{Style.RESET}")

    def get_sorted_items(self):
        items = os.listdir(self.current_dir)
        key_func = lambda x: x.lower()
        if self.sort_by == 'size':
            key_func = lambda x: os.path.getsize(os.path.join(self.current_dir, x))
        elif self.sort_by == 'date':
            key_func = lambda x: os.path.getmtime(os.path.join(self.current_dir, x))
        return sorted(items, key=key_func, reverse=self.reverse_sort)

    def display_list_view(self, items):
        for item in items:
            full_path = os.path.join(self.current_dir, item)
            is_dir = os.path.isdir(full_path)
            size = os.path.getsize(full_path) if not is_dir else '-'
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d %H:%M')
            
            item_style = Style.BLUE if is_dir else Style.NORMAL
            select_style = Style.BACKGROUND_GREEN if item in self.selected_items else ''
            
            print(f"{select_style}{item_style}{item:<30}{Style.RESET} {size:>10} {mtime:>20}")

    def display_grid_view(self, items):
        term_width = 80
        item_width = 20
        items_per_row = term_width // item_width

        for i, item in enumerate(items):
            is_dir = os.path.isdir(os.path.join(self.current_dir, item))
            item_style = Style.BLUE if is_dir else Style.NORMAL
            select_style = Style.BACKGROUND_GREEN if item in self.selected_items else ''
            
            print(f"{select_style}{item_style}{item[:17]:<17}{Style.RESET}", end='  ')
            if (i + 1) % items_per_row == 0:
                print()
        print()

    def change_directory(self, path):
        new_dir = os.path.join(self.current_dir, path)
        if os.path.isdir(new_dir):
            self.current_dir = os.path.abspath(new_dir)
            self.selected_items.clear()
        else:
            print(f"{Style.RED}Invalid directory{Style.RESET}")

    def toggle_view_mode(self):
        self.view_mode = 'grid' if self.view_mode == 'list' else 'list'

    def change_sort(self, sort_by):
        if sort_by in ['name', 'size', 'date']:
            self.sort_by = sort_by
        else:
            print(f"{Style.RED}Invalid sort option. Use 'name', 'size', or 'date'.{Style.RESET}")

    def toggle_selection(self, item):
        if item in self.selected_items:
            self.selected_items.remove(item)
        elif item in os.listdir(self.current_dir):
            self.selected_items.add(item)
        else:
            print(f"{Style.RED}Item not found: {item}{Style.RESET}")

    def copy_selected(self):
        if not self.selected_items:
            print(f"{Style.YELLOW}No items selected{Style.RESET}")
            return
        target_dir = input("Enter target directory: ")
        if os.path.isdir(target_dir):
            for item in self.selected_items:
                src = os.path.join(self.current_dir, item)
                dst = os.path.join(target_dir, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            print(f"{Style.GREEN}Items copied successfully{Style.RESET}")
            self.selected_items.clear()
        else:
            print(f"{Style.RED}Invalid target directory{Style.RESET}")

    def move_selected(self):
        if not self.selected_items:
            print(f"{Style.YELLOW}No items selected{Style.RESET}")
            return
        target_dir = input("Enter target directory: ")
        if os.path.isdir(target_dir):
            for item in self.selected_items:
                src = os.path.join(self.current_dir, item)
                dst = os.path.join(target_dir, item)
                shutil.move(src, dst)
            print(f"{Style.GREEN}Items moved successfully{Style.RESET}")
            self.selected_items.clear()
        else:
            print(f"{Style.RED}Invalid target directory{Style.RESET}")

    def delete_selected(self):
        if not self.selected_items:
            print(f"{Style.YELLOW}No items selected{Style.RESET}")
            return
        confirm = input(f"{Style.RED}Are you sure you want to delete selected items? (y/n): {Style.RESET}").lower()
        if confirm == 'y':
            for item in self.selected_items:
                path = os.path.join(self.current_dir, item)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            print(f"{Style.GREEN}Items deleted successfully{Style.RESET}")
            self.selected_items.clear()

    def show_help(self):
        help_text = """
File Manager Help:
  cd <dir>     - Change directory
  p            - Go to parent directory
  v            - Toggle view mode (list/grid)
  s <option>   - Change sort (name/size/date)
  r            - Reverse sort order
  sel <item>   - Select/deselect item
  copy         - Copy selected items
  move         - Move selected items
  delete       - Delete selected items
  q            - Quit file manager
  help         - Show this help
"""
        print(help_text)
        input("Press Enter to continue...")

if __name__ == "__main__":
    cmd = PythonCMD()
    cmd.run()