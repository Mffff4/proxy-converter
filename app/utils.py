from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
import questionary
from questionary import Style
import os
import json

console = Console()

custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),
    ('question', 'bold'),
    ('answer', 'fg:#f44336 bold'),
    ('pointer', 'fg:#ff69b4 bold'),
    ('highlighted', 'fg:#32cd32 bold'),
    ('selected', 'fg:#ff69b4'),
    ('separator', 'fg:#673ab7'),
    ('instruction', 'fg:#535353'),
])

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title(title: str):
    text = Text(title, style="bold magenta")
    console.print(Panel(text, box=box.DOUBLE_EDGE, padding=(1, 2)))

def print_success(message: str):
    console.print(f"[green]✓[/green] {message}")

def print_error(message: str):
    console.print(f"[red]✗[/red] {message}")

def print_info(message: str):
    console.print(f"[blue]ℹ[/blue] {message}")

def confirm_action(message: str) -> bool:
    return questionary.confirm(message, default=True, style=custom_style).ask()

def print_banner():
    banner = """
    ███╗   ███╗ █████╗ ██╗███╗   ██╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗
    ████╗ ████║██╔══██╗██║████╗  ██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
    ██╔████╔██║███████║██║██╔██╗ ██║█████╗  ██║     ██║   ██║██║  ██║█████╗  
    ██║╚██╔╝██║██╔══██║██║██║╚██╗██║██╔══╝  ██║     ██║   ██║██║  ██║██╔══╝  
    ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║███████╗╚██████╗╚██████╔╝██████╔╝███████╗
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
                                                                              
    Telegram Channel: @mainecode
    """
    console.print(Panel(banner, style="bold magenta"))

def get_file_path(filename: str, create_if_missing: bool = False) -> str:
    if os.path.exists(filename):
        return filename
    print_error(f"Файл {filename} не найден")
    file_path = questionary.text("Введите путь к файлу:", style=custom_style).ask()
    if not file_path:
        return filename
    if not os.path.exists(file_path):
        if create_if_missing:
            try:
                with open(file_path, 'w') as f:
                    if filename.endswith('.json'):
                        json.dump([], f)
                print_success(f"Создан новый файл: {file_path}")
            except Exception as e:
                print_error(f"Ошибка создания файла: {str(e)}")
                return filename
    return file_path

def initialize_files():
    required_files = {
        'data/accounts.json': '[]',
        'proxies.txt': '',
    }
    required_dirs = ['sessions', 'data']
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print_success(f"Создана директория {directory}")
    for filename, default_content in required_files.items():
        if not os.path.exists(filename):
            try:
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(default_content)
                print_success(f"Создан файл {filename}")
            except Exception as e:
                print_error(f"Ошибка при создании {filename}: {str(e)}")