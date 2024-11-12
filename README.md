# 🚀 Proxy manager

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Поддержка-да-brightgreen.svg)](https://github.com/Mffff4/proxy-manager/graphs/commit-activity)
[![PRs Welcome](https://img.shields.io/badge/PRs-приветствуются-brightgreen.svg)](http://makeapullrequest.com)
[![С любовью](https://img.shields.io/badge/С%20любовью-❤-red.svg)](https://github.com/Mffff4)
[![Telegram](https://img.shields.io/badge/Telegram-канал-blue.svg)](https://t.me/mainecode)
[![Звезды на GitHub](https://img.shields.io/github/stars/Mffff4/proxy-manager?style=social)](https://github.com/Mffff4/proxy-manager)
[![Мои проекты](https://img.shields.io/badge/Мои%20проекты-🔗-blue)](https://github.com/Mffff4)

<div align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/main/icons/python.svg" width="100" />
  
  <h3>🛠 Инструмент для генерации аккаунтов и управления прокси</h3>
</div>

<div align="center">
  <img src="assets/preview.png" alt="Preview" width="800" />
</div>

---

## 📋 Содержание

- [✨ Особенности](#-особенности)
- [📦 Установка](#-установка)
- [🚀 Использование](#-использование)
- [⚙️ Конфигурация](#-конфигурация)
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
git clone https://github.com/Mffff4/proxy-manager.git
cd proxy-manager
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
  <sub>Built with ❤️ by @Mffff4</sub>
</div>


