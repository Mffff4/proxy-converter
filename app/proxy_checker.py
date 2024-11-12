import aiohttp
import asyncio
from typing import List, Dict
import time
from app.utils import print_title, print_error, print_success, print_info, custom_style
import questionary
from tqdm import tqdm
import requests
from requests.auth import HTTPProxyAuth
import urllib3
from concurrent.futures import ThreadPoolExecutor
import socks
from urllib.parse import urlparse

urllib3.disable_warnings()
MAX_CONCURRENT = 300
TEST_URLS = [
    'http://ip-api.com/json',
    'https://api.ipify.org?format=json',
    'http://httpbin.org/ip'
]

def parse_proxy(proxy_str: str) -> Dict:
    try:
        proxy_str = proxy_str.strip()
        if '://' in proxy_str:
            protocol = proxy_str.split('://')[0]
            proxy_str = proxy_str.split('://')[1]
        else:
            protocol = None
        if '@' in proxy_str:
            auth, addr = proxy_str.split('@')
            if ':' in auth and ':' in addr:
                username, password = auth.split(':')
                ip, port = addr.split(':')
                return {
                    'protocol': protocol,
                    'host': ip,
                    'port': int(port),
                    'username': username,
                    'password': password
                }
        parts = proxy_str.split(':')
        if len(parts) == 4:
            if all(part.isdigit() for part in parts[0].split('.')):
                ip, port, username, password = parts
            else:
                username, password, ip, port = parts
            return {
                'protocol': protocol,
                'host': ip,
                'port': int(port),
                'username': username,
                'password': password
            }
        elif len(parts) == 2:
            ip, port = parts
            return {
                'protocol': protocol,
                'host': ip,
                'port': int(port),
                'username': None,
                'password': None
            }
        raise ValueError(f"Неподдерживаемый формат прокси: {proxy_str}")
    except Exception as e:
        raise ValueError(f"Ошибка парсинга прокси: {str(e)}")

def check_proxy(proxy: str, timeout: int = 10) -> Dict:
    try:
        proxy_info = parse_proxy(proxy)
        if not proxy_info:
            return {'working': False, 'proxy': proxy, 'error': 'Неверный формат прокси'}
        protocols_to_check = ['http', 'https', 'socks4', 'socks5'] if not proxy_info['protocol'] else [proxy_info['protocol']]
        working_protocols = []
        best_response_time = float('inf')
        best_result = None
        for protocol in protocols_to_check:
            try:
                if protocol in ['socks4', 'socks5']:
                    proxy_type = socks.PROXY_TYPE_SOCKS4 if protocol == 'socks4' else socks.PROXY_TYPE_SOCKS5
                    socks_proxy = socks.socksocket()
                    socks_proxy.set_proxy(
                        proxy_type,
                        proxy_info['host'],
                        proxy_info['port'],
                        username=proxy_info.get('username'),
                        password=proxy_info.get('password')
                    )
                    start_time = time.time()
                    socks_proxy.settimeout(timeout)
                    try:
                        socks_proxy.connect(('ip-api.com', 80))
                        response_time = round((time.time() - start_time) * 1000)
                        working_protocols.append(protocol)
                        if response_time < best_response_time:
                            best_response_time = response_time
                            best_result = {
                                'working': True,
                                'proxy': proxy,
                                'response_time': response_time,
                                'working_format': f"{protocol}://{proxy}"
                            }
                    finally:
                        socks_proxy.close()
                else:
                    proxy_url = f"{protocol}://"
                    if proxy_info.get('username') and proxy_info.get('password'):
                        proxy_url += f"{proxy_info['username']}:{proxy_info['password']}@"
                    proxy_url += f"{proxy_info['host']}:{proxy_info['port']}"
                    proxies = {
                        'http': proxy_url,
                        'https': proxy_url
                    }
                    response = requests.get(
                        'http://ip-api.com/json',
                        proxies=proxies,
                        timeout=timeout,
                        verify=False
                    )
                    if response.status_code == 200:
                        response_time = round(response.elapsed.total_seconds() * 1000)
                        working_protocols.append(protocol)
                        if response_time < best_response_time:
                            best_response_time = response_time
                            data = response.json()
                            best_result = {
                                'working': True,
                                'proxy': proxy,
                                'response_time': response_time,
                                'ip': data.get('query', 'Unknown'),
                                'country': data.get('country', 'Unknown'),
                                'city': data.get('city', 'Unknown'),
                                'isp': data.get('isp', 'Unknown'),
                                'org': data.get('org', 'Unknown'),
                                'working_format': proxy_url
                            }
            except:
                continue
        if best_result:
            best_result['working_protocols'] = working_protocols
            return best_result
        return {'working': False, 'proxy': proxy, 'error': 'Не найдено рабочих протоколов'}
    except Exception as e:
        return {'working': False, 'proxy': proxy, 'error': str(e)}

async def check_proxies_batch(proxies: List[str], timeout: int, pbar: tqdm) -> List[Dict]:
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
        futures = []
        for proxy in proxies:
            future = loop.run_in_executor(executor, check_proxy, proxy, timeout)
            futures.append(future)
        results = []
        for future in asyncio.as_completed(futures):
            result = await future
            results.append(result)
            pbar.update(1)
        return results

def load_proxies(filename: str = 'proxies.txt') -> List[str]:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            proxies = []
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '://' in line:
                    line = line.split('://', 1)[1]
                if '@' in line:
                    auth, addr = line.split('@')
                    if ':' in auth and ':' in addr:
                        proxies.append(line)
                        continue
                parts = line.split(':')
                if len(parts) == 4:
                    login, password, ip, port = parts
                    proxy = f"{login}:{password}@{ip}:{port}"
                    proxies.append(proxy)
                    continue
                if len(parts) == 4:
                    ip, port, login, password = parts
                    proxy = f"{login}:{password}@{ip}:{port}"
                    proxies.append(proxy)
                    continue
                if len(parts) == 2:
                    proxies.append(line)
                    continue
                print_error(f"Неверный формат прокси: {line}")
            return proxies
    except FileNotFoundError:
        print_error(f"Файл {filename} не найден")
        return []
    except Exception as e:
        print_error(f"Ошибка при чтении файла: {str(e)}")
        return []

def save_working_proxies(results: List[Dict], filename: str = 'working_proxies.txt'):
    working_proxies = [r['working_format'] for r in results if r['working']]
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(working_proxies))
        print_success(f"Рабочие прокси сохранены в {filename}")
    except Exception as e:
        print_error(f"Ошибка при сохранении файла: {str(e)}")

def check_proxies_menu():
    print_title("Проверка прокси")
    proxies = load_proxies()
    if not proxies:
        input("\nНажмите Enter для продолжения...")
        return
    print_info(f"Загружено {len(proxies)} прокси")
    timeout = questionary.text(
        "Введите таймаут в секундах (по умолчанию 10):",
        default="10",
        validate=lambda text: text.isdigit() and 1 <= int(text) <= 60,
        style=custom_style
    ).ask()
    timeout = int(timeout)
    print_info("Начинаем проверку прокси...")
    print_info("Проверяем все протоколы (HTTP, HTTPS, SOCKS4, SOCKS5)...")
    with tqdm(
        total=len(proxies),
        desc="Проверка прокси",
        unit="proxy",
        ncols=80,
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'
    ) as pbar:
        results = asyncio.run(check_proxies_batch(proxies, timeout, pbar))
    working = [r for r in results if r['working']]
    print_success(f"\nРабочих прокси: {len(working)} из {len(proxies)}")
    if working:
        if questionary.confirm(
            "Показать рабочие прокси?",
            default=True,
            style=custom_style
        ).ask():
            working.sort(key=lambda x: x['response_time'])
            for result in working:
                location_info = []
                if result.get('country'):
                    location_info.append(result['country'])
                if result.get('city'):
                    location_info.append(result['city'])
                location = f"[{' - '.join(location_info)}]" if location_info else ""
                print_success(
                    f"✓ {result['proxy']} - {result['response_time']}ms {location}\n"
                    f"IP: {result.get('ip', 'Unknown')}\n"
                    f"Провайдер: {result.get('isp', 'Unknown')}\n"
                    f"Организация: {result.get('org', 'Unknown')}\n"
                    f"Рабочий формат: {result['working_format']}\n"
                    f"Работает с протоколами: {', '.join(result['working_protocols'])}"
                )
        if questionary.confirm(
            "Сохранить рабочие прокси в отдельный файл?",
            default=True,
            style=custom_style
        ).ask():
            save_format = questionary.select(
                "Выберите формат сохранения:",
                choices=[
                    "Только прокси",
                    "Прокси с информацией",
                    "Оба варианта"
                ],
                style=custom_style
            ).ask()
            if save_format == "Только прокси":
                save_working_proxies(results)
            elif save_format == "Прокси с информацией":
                try:
                    with open('working_proxies_info.txt', 'w', encoding='utf-8') as f:
                        for r in working:
                            location_info = []
                            if r.get('country'):
                                location_info.append(r['country'])
                            if r.get('city'):
                                location_info.append(r['city'])
                            location = f"[{' - '.join(location_info)}]" if location_info else ""
                            f.write(f"{r['working_format']} - {r['response_time']}ms {location}\n")
                            f.write(f"IP: {r.get('ip', 'Unknown')}\n")
                            f.write(f"Провайдер: {r.get('isp', 'Unknown')}\n")
                            f.write(f"Организация: {r.get('org', 'Unknown')}\n")
                            f.write(f"Протоколы: {', '.join(r['working_protocols'])}\n")
                            f.write("-" * 50 + "\n")
                    print_success("Информация о прокси сохранена в working_proxies_info.txt")
                except Exception as e:
                    print_error(f"Ошибка при сохранении информации: {str(e)}")
            else:
                save_working_proxies(results)
                try:
                    with open('working_proxies_info.txt', 'w', encoding='utf-8') as f:
                        for r in working:
                            location_info = []
                            if r.get('country'):
                                location_info.append(r['country'])
                            if r.get('city'):
                                location_info.append(r['city'])
                            location = f"[{' - '.join(location_info)}]" if location_info else ""
                            f.write(f"{r['working_format']} - {r['response_time']}ms {location}\n")
                            f.write(f"IP: {r.get('ip', 'Unknown')}\n")
                            f.write(f"Провайдер: {r.get('isp', 'Unknown')}\n")
                            f.write(f"Организация: {r.get('org', 'Unknown')}\n")
                            f.write(f"Протоколы: {', '.join(r['working_protocols'])}\n")
                            f.write("-" * 50 + "\n")
                    print_success("Информация о прокси сохранена в working_proxies_info.txt")
                except Exception as e:
                    print_error(f"Ошибка при сохранении информации: {str(e)}")
    failed = [r for r in results if not r['working']]
    if failed and questionary.confirm(
        "Показать нерабочие прокси?",
        default=False,
        style=custom_style
    ).ask():
        for result in failed:
            print_error(f"✗ {result['proxy']} - {result.get('error', 'Неизвестная ошибка')}")
    input("\nНажмите Enter для продолжения...")