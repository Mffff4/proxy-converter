# 🚀 Account Generator & Proxy Manager

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](https://github.com/yourusername/yourrepository/graphs/commit-activity)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Made with Love](https://img.shields.io/badge/Made%20with-❤-red.svg)](https://github.com/yourusername)

<div align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/main/icons/python.svg" width="100" />
  
  <h3>🛠 Мощный инструмент для генерации аккаунтов и управления прокси</h3>
</div>

<div align="center">
  <img src="assets/preview.png" alt="Preview" width="800" />
</div>

---

## 📋 Содержание

- [✨ Особенности](#-особенности)
- [📦 Установка](#-установка)
- [🚀 Использование](#-использование)
- [📁 Структура проекта](#-структура-проекта)
- [📄 Лицензия](#-лицензия)

## ✨ Особенности

- 🔄 Автоматическая генерация аккаунтов
- 🌐 Поддержка различных типов прокси (HTTP, SOCKS4, SOCKS5)
- ✅ Встроенный чекер прокси
- 🛡️ Гибкая настройка User-Agent
- 💾 Сохранение в JSON формате
- 🎨 Красивый интерактивный интерфейс

## 📦 Установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

## 🚀 Использование

1. **Запустите приложение:**
```bash
python main.py
```

2. **Выберите нужную опцию в интерактивном меню:**
   - 📝 Генерация accounts.json
   - 🔄 Управление прокси
   - ✅ Проверка прокси
   - 🗑️ Удаление sec_ch_ua

## 📁 Структура проекта

```
📦 account-generator
 ┣ 📜 main.py              # Главный файл приложения
 ┣ 📜 account_generator.py # Генератор аккаунтов
 ┣ 📜 agents.py           # Генерация User-Agent
 ┣ 📜 proxy_changer.py    # Управление прокси
 ┣ 📜 proxy_checker.py    # Проверка прокси
 ┣ 📜 utils.py            # Вспомогательные функции
 ┣ 📜 requirements.txt    # Зависимости проекта
 ┣ 📜 proxies.txt         # Список прокси
 ┗ 📂 data                # Директория с данными
```

## ⚙️ Конфигурация

### Формат прокси в proxies.txt:
```plaintext
http://username:password@ip:port
socks5://username:password@ip:port
ip:port:username:password
```

### Основные зависимости:
```plaintext
aiohttp==3.10.10
requests==2.32.3
rich==13.9.4
tqdm==4.67.0
```

## 🤝 Вклад в проект

Мы приветствуем ваш вклад в развитие проекта! Вот как вы можете помочь:

1. 🍴 Форкните репозиторий
2. 🔧 Создайте ветку для ваших изменений
3. ✨ Внесите изменения
4. 📝 Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

---

<div align="center">
  <sub>Built with ❤️ by @yourusername</sub>
</div>


