🌐 Доступно на: [English](README.md) | [فارسی](README_FA.md) | [Русский](README_ru.md) | [中文](README_zh.md)

# 🌍 ConfigForge V2Ray

**ConfigForge V2Ray** — это современный open-source проект, который собирает и оптимизирует V2Ray-конфигурации из разных источников.  
Сервис автоматически определяет вашу страну и предлагает **самые быстрые конфигурации**, проверенные через **API Check-Host**, чтобы обеспечить максимальную скорость и стабильность.

---

## 🌐 Веб-интерфейс

### Быстрые подписки для России (прямые ссылки)
Используйте эти ссылки в любом клиенте, поддерживающем V2Ray (v2rayNG, V2RayN, Shadowrocket и др.).  
Просто скопируйте ссылку и вставьте её в раздел **Subscriptions**.

| Файл | Описание | Ссылка |
|---|---|---|
| `all.txt` | Полный список серверов для России (по средней задержке) | [Открыть](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ru/all.txt) · [Зеркало](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ru/all.txt) |
| `light.txt` | Топ-30 быстрых серверов | [Открыть](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ru/light.txt) · [Зеркало](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ru/light.txt) |
| `vless.txt` | Только VLESS | [Открыть](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ru/vless.txt) · [Зеркало](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ru/vless.txt) |
| `vmess.txt` | Только VMess | [Открыть](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ru/vmess.txt) · [Зеркало](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ru/vmess.txt) |
| `shadowsocks.txt` | Только Shadowsocks | [Открыть](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ru/shadowsocks.txt) · [Зеркало](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ru/shadowsocks.txt) |
| `trojan.txt` | Только Trojan | [Открыть](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ru/trojan.txt) · [Зеркало](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ru/trojan.txt) |
| `unknown.txt` | Другие/неизвестные протоколы | [Открыть](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ru/unknown.txt) · [Зеркало](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ru/unknown.txt) |

---

## 🚀 Почему ConfigForge?
В отличие от простых репозиториев, **ConfigForge V2Ray**:
- ✅ Постоянно загружает конфигурации из разных источников  
- ✅ Тестирует задержку для каждой страны с помощью [Check-Host API](https://check-host.net/)  
- ✅ Предлагает только самые быстрые серверы для вашего региона  
- ✅ Делит конфиги на отдельные списки (VLESS, VMess, Shadowsocks, Trojan)  
- ✅ Работает полностью автоматически через GitHub Actions — без сервера!

---

## ✨ Возможности
- 🌍 Выбор по стране — автоопределение или ручной выбор  
- 🔍 Рекомендации только протестированных серверов  
- 🌐 Мультиязычный интерфейс  
- 📂 Подписки в удобных файлах:  
  - `all.txt` → Полный список  
  - `light.txt` → 30 лучших  
  - Отдельные файлы для VLESS, VMess, Shadowsocks, Trojan  
- 🔄 Автообновления через GitHub Actions  
- ⚡ Максимальная простота и скорость  
- 🛠 Легко расширять и дополнять

---

## 🛠 Как использовать

### ✅ Вариант 1: запуск локально
Клонируйте репозиторий:
```bash
git clone https://github.com/Alibodama/ConfigForge.git
cd ConfigForge
```

Установите зависимости:
```bash
pip install -r source/requirements.txt
```

Запуск:
```bash
python source/main.py
```

### ✅ Вариант 2: автоматический запуск на GitHub
Просто сделайте **Fork** репозитория, настройте GitHub Actions и всё будет работать само!  

---

## ⭐ Популярность проекта
![Stargazers over time](https://starchart.cc/Alibodama/ConfigForge-V2Ray.svg?variant=adaptive)

---
Этот проект распространяется под лицензией **GPL-3.0**.  
