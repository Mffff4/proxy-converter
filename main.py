from app.account_generator import generate_account_json, remove_sec_ch_ua
from app.proxy_changer import update_proxy_settings
from app.proxy_checker import check_proxies_menu
from app.utils import print_title, print_error, custom_style, print_banner, initialize_files, clear_screen
import questionary
import sys

def main_menu():
    while True:
        try:
            clear_screen()
            print_banner()
            choice = questionary.select(
                "Выберите действие:",
                choices=[
                    "Сгенерировать accounts.json",
                    "Сменить структуру и формат прокси",
                    "Проверить прокси на работоспособность",
                    "Удалить sec_ch_ua из accounts.json",
                    "Выход"
                ],
                style=custom_style
            ).ask()
            if choice is None:
                raise KeyboardInterrupt
            if choice == "Сгенерировать accounts.json":
                generate_account_json()
            elif choice == "Сменить структуру и формат прокси":
                update_proxy_settings()
            elif choice == "Проверить прокси на работоспособность":
                check_proxies_menu()
            elif choice == "Удалить sec_ch_ua из accounts.json":
                remove_sec_ch_ua()
            else:
                clear_screen()
                print_banner()
                print_title("До свидания! 👋")
                sys.exit(0)
        except KeyboardInterrupt:
            clear_screen()
            print_banner()
            print_title("\nПрограмма завершена пользователем 👋")
            sys.exit(0)
        except Exception as e:
            print_error(f"Произошла ошибка: {str(e)}")
            if not questionary.confirm(
                "Хотите продолжить работу?",
                default=True,
                style=custom_style
            ).ask():
                clear_screen()
                print_banner()
                print_title("До свидания! 👋")
                sys.exit(1)

if __name__ == "__main__":
    try:
        clear_screen()
        initialize_files()
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print_banner()
        print_title("\nПрограмма завершена пользователем 👋")
        sys.exit(0)
    except Exception as e:
        print_error(f"Критическая ошибка: {str(e)}")
        sys.exit(1)