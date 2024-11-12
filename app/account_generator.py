import json
import random
import os
from app.agents import generate_random_user_agent
import questionary
from app.utils import print_title, print_error, print_info, print_success, custom_style, console, clear_screen

def create_required_directories():
    directories = ['sessions', 'data']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print_info(f"Создана директория {directory}")

def read_proxies(file_path='proxies.txt'):
    try:
        if not os.path.exists(file_path):
            print_info(f"Файл {file_path} не найден. Создаем пустой файл.")
            with open(file_path, 'w', encoding='utf-8') as f:
                pass
            return []
        with open(file_path, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print_success(f"Загружено {len(proxies)} прокси из {file_path}")
            return proxies
    except Exception as e:
        print_error(f"Ошибка при чтении файла прокси: {str(e)}")
        return []

def get_session_files(sessions_dir='sessions'):
    try:
        if not os.path.exists(sessions_dir):
            os.makedirs(sessions_dir)
            print_info(f"Создана директория {sessions_dir}")
        session_files = [name for name in os.listdir(sessions_dir) if name.endswith('.session')]
        if not session_files:
            print_error(f"В папке {sessions_dir} не найдено .session файлов")
            print_info("Поместите файлы сессий в папку sessions и попробуйте снова")
        return session_files
    except Exception as e:
        print_error(f"Ошибка при получении списка сессий: {str(e)}")
        return []

def save_accounts(accounts, filename='accounts.json'):
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        filepath = os.path.join('data', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(accounts, f, indent=4, ensure_ascii=False)
        print_success(f"Данные успешно сохранены в {filepath}")
        return True
    except Exception as e:
        print_error(f"Ошибка при сохранении файла {filename}: {str(e)}")
        return False

def generate_account_json():
    clear_screen()
    print_title("Генерация accounts.json")
    create_required_directories()
    session_files = get_session_files()
    if not session_files:
        input("\nНажмите Enter для продолжения...")
        return False
    total_sessions = len(session_files)
    print_info(f"Найдено {total_sessions} .session файлов")
    proxies = read_proxies()
    if not proxies:
        if not questionary.confirm("Прокси не найдены. Продолжить без прокси?", default=False, style=custom_style).ask():
            return False
    try:
        choice = questionary.select(
            "Выберите действие:",
            choices=[
                "Привязать все сессии",
                "Выбрать количество сессий",
                "Назад"
            ],
            style=custom_style
        ).ask()
    except Exception:
        print_error("Операция отменена пользователем")
        return False
    if choice == "Назад":
        return False
    if choice == "Привязать все сессии":
        num_accounts = total_sessions
    else:
        try:
            num_accounts = questionary.text(
                f"Сколько аккаунтов сгенерировать? (максимум {total_sessions})",
                validate=lambda text: text.isdigit() and 0 < int(text) <= total_sessions,
                style=custom_style
            ).ask()
            num_accounts = int(num_accounts)
        except Exception:
            print_error("Операция отменена пользователем")
            return False
    with console.status("[bold green]Генерация аккаунтов...") as status:
        accounts = []
        for i in range(num_accounts):
            try:
                user_agent, sec_ch_ua = generate_random_user_agent()
                proxy = random.choice(proxies) if proxies else ""
                account = {
                    "session_name": os.path.splitext(session_files[i])[0],
                    "user_agent": user_agent,
                    "sec_ch_ua": sec_ch_ua,
                    "proxy": proxy
                }
                accounts.append(account)
                status.update(f"[bold green]Генерация аккаунта {i+1}/{num_accounts}")
            except Exception as e:
                print_error(f"Ошибка при генерации аккаунта {i+1}: {str(e)}")
                if not questionary.confirm("Продолжить генерацию?", default=True).ask():
                    break
    if accounts:
        if save_accounts(accounts):
            print_success(f"Сгенерировано {len(accounts)} аккаунтов")
            input("\nНажмите Enter для продолжения...")
            return True
    else:
        print_error("Не удалось сгенерировать аккаунты")
        input("\nНажмите Enter для продолжения...")
    return False

def remove_sec_ch_ua():
    clear_screen()
    print_title("Удаление sec_ch_ua из accounts.json")
    try:
        with open('data/accounts.json', 'r', encoding='utf-8') as f:
            accounts = json.load(f)
        modified = False
        for account in accounts:
            if 'sec_ch_ua' in account:
                del account['sec_ch_ua']
                modified = True
        if modified:
            with open('data/accounts.json', 'w', encoding='utf-8') as f:
                json.dump(accounts, f, indent=4, ensure_ascii=False)
            print_success("Поле 'sec_ch_ua' успешно удалено из accounts.json")
        else:
            print_info("Поле 'sec_ch_ua' не найдено в accounts.json")
    except FileNotFoundError:
        print_error("Файл accounts.json не найден")
    except Exception as e:
        print_error(f"Ошибка при обработке файла: {str(e)}")
    input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    try:
        generate_account_json()
    except KeyboardInterrupt:
        print_error("\nОперация прервана пользователем")
    except Exception as e:
        print_error(f"Неожиданная ошибка: {str(e)}")