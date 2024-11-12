import json
import os
import re
from app.utils import print_title, print_error, print_info, print_success, custom_style, clear_screen
import questionary

def ensure_accounts_json_exists():
    if not os.path.exists('data/accounts.json'):
        os.makedirs('data', exist_ok=True)
        with open('data/accounts.json', 'w', encoding='utf-8') as f:
            json.dump([], f)

def parse_proxy(proxy_string):
    if not proxy_string:
        return None
    match = re.match(r'^(?:(?P<type>\w+)://)?(?:(?P<login>[^:@]+):(?P<password>[^@]+)@)?(?P<ip>[^:]+):(?P<port>\d+)$', proxy_string)
    if match:
        return match.groupdict()
    parts = proxy_string.split(':')
    if len(parts) == 4:
        if re.match(r'^[\d\.]+$', parts[0]):
            return {
                'type': None,
                'ip': parts[0],
                'port': parts[1],
                'login': parts[2],
                'password': parts[3]
            }
        else:
            return {
                'type': None,
                'login': parts[0],
                'password': parts[1],
                'ip': parts[2],
                'port': parts[3]
            }
    return None

def show_proxies(proxies):
    clear_screen()
    print_title("Текущие прокси")
    if not proxies:
        print_info("Список прокси пуст")
        return
    for i, proxy in enumerate(proxies, 1):
        print_info(f"{i}. {proxy}")

def change_proxy_port(proxies):
    if not proxies:
        print_error("Список прокси пуст")
        return proxies
    new_port = questionary.text(
        "Введите новый порт:",
        validate=lambda text: text.isdigit() and 1 <= int(text) <= 65535,
        style=custom_style
    ).ask()
    if not new_port:
        return proxies
    new_proxies = []
    for proxy in proxies:
        proxy_parts = parse_proxy(proxy)
        if proxy_parts:
            proxy_parts['port'] = new_port
            new_proxy = f"{proxy_parts['type']}://" if proxy_parts['type'] else ""
            new_proxy += f"{proxy_parts['login']}:{proxy_parts['password']}@" if proxy_parts['login'] and proxy_parts['password'] else ""
            new_proxy += f"{proxy_parts['ip']}:{proxy_parts['port']}"
            new_proxies.append(new_proxy)
        else:
            new_proxies.append(proxy)
    print_success("Порт прокси успешно изменен")
    return new_proxies

def change_proxy_type(proxies):
    if not proxies:
        print_error("Список прокси пуст")
        return proxies
    type_choice = questionary.select(
        "Выберите новый тип прокси:",
        choices=[
            "http://",
            "socks5://",
            "Без типа"
        ],
        style=custom_style
    ).ask()
    if not type_choice:
        return proxies
    new_type = '' if type_choice == "Без типа" else type_choice
    new_proxies = []
    for proxy in proxies:
        proxy_parts = parse_proxy(proxy)
        if proxy_parts:
            new_proxy = new_type
            if proxy_parts['login'] and proxy_parts['password']:
                new_proxy += f"{proxy_parts['login']}:{proxy_parts['password']}@"
            new_proxy += f"{proxy_parts['ip']}:{proxy_parts['port']}"
            new_proxies.append(new_proxy)
        else:
            new_proxies.append(proxy)
    print_success("Тип прокси успешно изменен")
    return new_proxies

def change_proxy_structure(proxies):
    if not proxies:
        print_error("Список прокси пуст")
        return proxies
    structure_choice = questionary.select(
        "Выберите новую структуру:",
        choices=[
            "login:password:ip:port",
            "ip:port:login:password",
            "type://login:password:ip:port",
            "type://login:password@ip:port"
        ],
        style=custom_style
    ).ask()
    if not structure_choice:
        return proxies
    new_proxies = []
    for proxy in proxies:
        parts = parse_proxy(proxy)
        if not parts:
            print_error(f"Не удалось разобрать прокси: {proxy}")
            new_proxies.append(proxy)
            continue
        try:
            if structure_choice == "login:password:ip:port":
                if parts.get('login') and parts.get('password'):
                    new_proxy = f"{parts['login']}:{parts['password']}:{parts['ip']}:{parts['port']}"
                else:
                    new_proxy = f":{parts['ip']}:{parts['port']}"
            elif structure_choice == "ip:port:login:password":
                if parts.get('login') and parts.get('password'):
                    new_proxy = f"{parts['ip']}:{parts['port']}:{parts['login']}:{parts['password']}"
                else:
                    new_proxy = f"{parts['ip']}:{parts['port']}::"
            elif structure_choice == "type://login:password:ip:port":
                new_proxy = f"{parts.get('type', 'http')}://"
                if parts.get('login') and parts.get('password'):
                    new_proxy += f"{parts['login']}:{parts['password']}:{parts['ip']}:{parts['port']}"
                else:
                    new_proxy += f":{parts['ip']}:{parts['port']}"
            else:
                new_proxy = f"{parts.get('type', 'http')}://"
                if parts.get('login') and parts.get('password'):
                    new_proxy += f"{parts['login']}:{parts['password']}@"
                new_proxy += f"{parts['ip']}:{parts['port']}"
            new_proxies.append(new_proxy)
            print_success(f"Преобразовано: {proxy} -> {new_proxy}")
        except Exception as e:
            print_error(f"Ошибка обработки прокси {proxy}: {str(e)}")
            new_proxies.append(proxy)
    return new_proxies

def proxy_menu(proxies):
    original_proxies = proxies.copy()
    while True:
        clear_screen()
        show_proxies(proxies)
        choice = questionary.select(
            "Выберите действие:",
            choices=[
                "Сменить порт прокси",
                "Сменить тип прокси",
                "Поменять структуру прокси",
                "Показать мои прокси",
                "Сохранить изменения",
                "Отменить изменения"
            ],
            style=custom_style
        ).ask()
        if choice == "Сменить порт прокси":
            proxies = change_proxy_port(proxies)
        elif choice == "Сменить тип прокси":
            proxies = change_proxy_type(proxies)
        elif choice == "Поменять структуру прокси":
            proxies = change_proxy_structure(proxies)
        elif choice == "Показать мои прокси":
            show_proxies(proxies)
            input("\nНажмите Enter для продолжения...")
        elif choice == "Сохранить изменения":
            if questionary.confirm("Сохранить изменения?", default=True).ask():
                return proxies
        else:
            if questionary.confirm("Отменить все изменения?", default=True).ask():
                return original_proxies

def update_accounts_json():
    ensure_accounts_json_exists()
    try:
        with open('data/accounts.json', 'r', encoding='utf-8') as f:
            accounts = json.load(f)
    except Exception as e:
        print_error(f"Ошибка чтения data/accounts.json: {str(e)}")
        return
    proxies = [account['proxy'] for account in accounts if 'proxy' in account and account['proxy']]
    if not proxies:
        print_error("В data/accounts.json нет прокси")
        return
    new_proxies = proxy_menu(proxies)
    if new_proxies:
        for account, new_proxy in zip(accounts, new_proxies):
            if 'proxy' in account:
                account['proxy'] = new_proxy
        try:
            with open('data/accounts.json', 'w', encoding='utf-8') as f:
                json.dump(accounts, f, indent=4, ensure_ascii=False)
            print_success("Прокси успешно обновлены в data/accounts.json")
        except Exception as e:
            print_error(f"Ошибка сохранения data/accounts.json: {str(e)}")

def update_proxies_txt():
    if not os.path.exists('proxies.txt'):
        print_error("Файл proxies.txt не найден")
        return
    try:
        with open('proxies.txt', 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except Exception as e:
        print_error(f"Ошибка чтения proxies.txt: {str(e)}")
        return
    if not proxies:
        print_error("Файл proxies.txt пуст")
        return
    new_proxies = proxy_menu(proxies)
    if new_proxies:
        try:
            with open('proxies.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_proxies))
            print_success("Прокси успешно обновлены в proxies.txt")
        except Exception as e:
            print_error(f"Ошибка сохранения proxies.txt: {str(e)}")

def update_proxy_settings():
    clear_screen()
    print_title("Настройка прокси")
    choice = questionary.select(
        "Где изменить настройки прокси?",
        choices=[
            "В файле accounts.json",
            "В файле proxies.txt",
            "Назад"
        ],
        style=custom_style
    ).ask()
    if choice == "В файле accounts.json":
        update_accounts_json()
    elif choice == "В файле proxies.txt":
        update_proxies_txt()

if __name__ == "__main__":
    try:
        update_proxy_settings()
    except KeyboardInterrupt:
        print_error("\nОперация прервана пользователем")
    except Exception as e:
        print_error(f"Неожиданная ошибка: {str(e)}")