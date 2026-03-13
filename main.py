"""
holazc_info — OSINT MEGA BOT v11.0
OSINT | Red Team | Казино | Геймификация

Установка:  pip install "python-telegram-bot[job-queue]==21.3"
Запуск:     py -3.11 holazc_bot.py
"""

import os
import asyncio, logging, sqlite3, random
from datetime import datetime, time as dtime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# ══════════════════════════════════════════════
BOT_TOKEN  = os.environ.get("BOT_TOKEN")
CHANNEL_ID = "@holazc_info"
ADMIN_IDS  = [7883913708]
# ══════════════════════════════════════════════

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

LEVELS = {
    0:("Lurker",0), 1:("Curious",150), 2:("Observer",400),
    3:("OSINT Rookie",800), 4:("Info Gatherer",1500), 5:("Recon Analyst",2500),
    6:("Footprint Hunter",4000), 7:("Digital Detective",6000), 8:("Shadow Tracker",9000),
    9:("Data Miner",13000), 10:("OSINT Analyst",18000), 11:("Intel Operator",25000),
    12:("Network Mapper",33000), 13:("Threat Analyst",43000), 14:("Red Team Recon",55000),
    15:("Ghost Hunter",70000), 16:("Phantom Tracker",88000), 17:("Dark Web Agent",110000),
    18:("Nation State",135000), 19:("APEX OSINT GOD",165000),
}

LEAGUES = [("Bronze",0),("Silver",500),("Gold",2000),("Platinum",6000),("APEX",15000)]

# ══════════════════════════════════════════════
#  OSINT — ПОЛНАЯ БАЗА ЗНАНИЙ
# ══════════════════════════════════════════════

OSINT_MODULES = {

# ─── ЛЮДИ ─────────────────────────────────────────────────────
"people": {
    "name": "Разведка по людям",
    "emoji": "👤",
    "topics": {
        "person_full": {
            "name": "Полное досье на человека",
            "text": (
                "<b>Полное досье: пошаговый алгоритм</b>\n\n"
                "<b>Шаг 1 — Сбор точек входа</b>\n"
                "• ФИО / никнейм / телефон / email — что есть\n"
                "• Фото (если есть) — для reverse search\n"
                "• Известные аккаунты, город, работа\n\n"
                "<b>Шаг 2 — Поиск по имени</b>\n"
                "• Google: <code>\"Иван Иванов\" site:vk.com</code>\n"
                "• Google: <code>\"Ivan Ivanov\" -site:linkedin.com</code>\n"
                "• Yandex — лучше для СНГ целей\n"
                "• Bing — другой индекс, другие результаты\n\n"
                "<b>Шаг 3 — Социальные сети</b>\n"
                "• VK: поиск по имени, городу, школе/вузу\n"
                "• Instagram: поиск по нику, теги, геолокация\n"
                "• Facebook: Graph Search (через Maltego)\n"
                "• LinkedIn: работа, контакты, навыки\n"
                "• TikTok, Telegram, Twitter/X\n\n"
                "<b>Шаг 4 — Username hunting</b>\n"
                "• Sherlock: <code>sherlock username</code>\n"
                "• Maigret: <code>maigret username</code> (600+ сайтов)\n"
                "• WhatsMyName: веб-интерфейс\n\n"
                "<b>Шаг 5 — Фото разведка</b>\n"
                "• Google Images → Search by image\n"
                "• Yandex Images — лучший для лиц\n"
                "• TinEye — поиск оригинала фото\n"
                "• PimEyes — поиск лица по фото\n\n"
                "<b>Шаг 6 — Контакты</b>\n"
                "• Hunter.io — email по домену\n"
                "• Holehe — регистрация email на сайтах\n"
                "• PhoneInfoga — разведка по телефону\n"
                "• Truecaller — имя по номеру\n\n"
                "<b>Шаг 7 — Утечки данных</b>\n"
                "• HIBP: <code>haveibeenpwned.com</code>\n"
                "• DeHashed: поиск по email/password\n"
                "• IntelligenceX: архив утечек\n\n"
                "<b>Инструменты:</b> Maltego, SpiderFoot, Recon-ng, theHarvester"
            ),
        },
        "username": {
            "name": "Username OSINT",
            "text": (
                "<b>Username Hunting — найди все аккаунты</b>\n\n"
                "<b>Инструменты:</b>\n"
                "• <code>sherlock &lt;username&gt;</code> — 300+ сайтов, Python\n"
                "• <code>maigret &lt;username&gt;</code> — 2500+ сайтов, лучший\n"
                "• WhatsMyName.app — веб, 600+ сайтов\n"
                "• Namechk.com — соцсети и домены\n"
                "• KnowEm.com — 500+ платформ\n\n"
                "<b>Техники анализа никнеймов:</b>\n"
                "• Паттерны: user123, x_user_x, user_real\n"
                "• Замена букв: 0→o, 3→e, @→a\n"
                "• Добавление года рождения\n"
                "• Сокращения имени/фамилии\n\n"
                "<b>Связывание аккаунтов:</b>\n"
                "• Одинаковая аватарка\n"
                "• Стиль написания\n"
                "• Пересечение подписок\n"
                "• Геотеги в разных сетях\n"
                "• Wayback Machine — удалённые профили\n\n"
                "<b>Команды Maigret:</b>\n"
                "<code>pip install maigret</code>\n"
                "<code>maigret username --html</code>\n"
                "<code>maigret username -a</code> (все сайты)\n"
            ),
        },
        "phone": {
            "name": "Разведка по телефону",
            "text": (
                "<b>Phone OSINT — максимум из номера</b>\n\n"
                "<b>Базовая разведка:</b>\n"
                "• Страна / оператор по коду\n"
                "• Truecaller.com — имя владельца\n"
                "• GetContact — теги от других пользователей\n"
                "• NumLookup.com — детали оператора\n\n"
                "<b>Социальные сети:</b>\n"
                "• WhatsApp: добавь в контакты → смотри статус/фото\n"
                "• Telegram: @username через номер, поиск в группах\n"
                "• Viber: профиль при добавлении\n"
                "• VK: поиск по номеру телефона\n\n"
                "<b>PhoneInfoga:</b>\n"
                "<code>pip install phoneinfoga</code>\n"
                "<code>phoneinfoga scan -n +7XXXXXXXXXX</code>\n"
                "<code>phoneinfoga serve</code> — веб-интерфейс\n\n"
                "<b>Дополнительно:</b>\n"
                "• Google: <code>\"+7XXXXXXXXXX\"</code>\n"
                "• Yandex поиск по номеру\n"
                "• 2GIS — номер компании\n"
                "• Avito/OLX — объявления с номером\n\n"
                "<b>Телефон → Email:</b>\n"
                "• Восстановление аккаунта Gmail/VK\n"
                "• Даёт частичный email владельца\n"
            ),
        },
        "email_osint": {
            "name": "Email OSINT",
            "text": (
                "<b>Email OSINT — полная разведка</b>\n\n"
                "<b>Проверка и верификация:</b>\n"
                "• Hunter.io — верификация + формат домена\n"
                "• Emailrep.io — репутация email\n"
                "• MailTester.com — проверка существования\n"
                "• MXToolbox — почтовый сервер домена\n\n"
                "<b>Регистрации на сайтах:</b>\n"
                "• Holehe: <code>holehe email@domain.com</code>\n"
                "  Проверяет 120+ сервисов\n"
                "• GHunt (Google): <code>ghunt email email@gmail.com</code>\n"
                "  Находит: имя, фото, Google Maps отзывы, YouTube\n\n"
                "<b>Утечки данных:</b>\n"
                "• HIBP: haveibeenpwned.com\n"
                "• DeHashed.com — пароли и хеши\n"
                "• IntelligenceX.io — архивы утечек\n"
                "• Leak-Lookup.com\n\n"
                "<b>Заголовки письма:</b>\n"
                "• MXToolbox Header Analyzer\n"
                "• Google Admin Toolbox\n"
                "• Trace IP отправителя через Received:\n\n"
                "<b>Email → Соцсети:</b>\n"
                "• Gravity API (Clearbit)\n"
                "• FullContact API\n"
                "• Pipl.com\n\n"
                "<b>Автоматизация:</b>\n"
                "<code>pip install holehe ghunt</code>\n"
            ),
        },
        "face_search": {
            "name": "Поиск по лицу",
            "text": (
                "<b>Face OSINT — найди человека по фото</b>\n\n"
                "<b>Поисковики изображений:</b>\n"
                "• Yandex Images — лучший для лиц СНГ\n"
                "• Google Images → Search by image\n"
                "• TinEye.com — поиск оригинала\n"
                "• Bing Visual Search\n\n"
                "<b>Специализированные сервисы:</b>\n"
                "• PimEyes.com — поиск лица по базе\n"
                "• FaceCheck.ID — бесплатный поиск лиц\n"
                "• Social Catfish — поиск по фото\n"
                "• Clearview AI (LE only)\n\n"
                "<b>Извлечение метаданных фото:</b>\n"
                "<code>exiftool photo.jpg</code>\n"
                "Даёт: GPS, камера, дата, ПО редактирования\n\n"
                "<b>Анализ фото вручную:</b>\n"
                "• Фон: здания, вывески, транспорт\n"
                "• Растительность → климатическая зона\n"
                "• Теги на одежде, номера машин\n"
                "• Отражения в очках/стёклах\n\n"
                "<b>Дипфейк детекция:</b>\n"
                "• FotoForensics.com — анализ ELA\n"
                "• InVID — анализ видео\n"
                "• Hive Moderation — AI детектор\n"
            ),
        },
    }
},

# ─── КОМПАНИИ ─────────────────────────────────────────────────
"companies": {
    "name": "Разведка компаний",
    "emoji": "🏢",
    "topics": {
        "company_full": {
            "name": "Полная разведка компании",
            "text": (
                "<b>Company OSINT — полный алгоритм</b>\n\n"
                "<b>Шаг 1 — Базовая информация</b>\n"
                "• Юридическое название, ИНН, ОГРН\n"
                "• ЕГРЮЛ / Rusprofile.ru / Kontur.Focus\n"
                "• Crunchbase — инвесторы, финансы\n"
                "• LinkedIn Company Page\n\n"
                "<b>Шаг 2 — Сотрудники</b>\n"
                "• LinkedIn: фильтр по компании\n"
                "• Email формат: Hunter.io\n"
                "• GitHub: поиск по org/company name\n"
                "• Slack communities, корп. блоги\n\n"
                "<b>Шаг 3 — Технологии</b>\n"
                "• BuiltWith.com — технический стек\n"
                "• Wappalyzer — фронт/бэк технологии\n"
                "• Shodan: <code>org:\"Company Name\"</code>\n"
                "• Censys: SSL сертификаты\n\n"
                "<b>Шаг 4 — Инфраструктура</b>\n"
                "• SecurityTrails — история DNS\n"
                "• BGP.he.net — ASN и IP диапазоны\n"
                "• RiskIQ / PassiveTotal\n"
                "• Subfinder: <code>subfinder -d domain.com</code>\n\n"
                "<b>Шаг 5 — Утечки и документы</b>\n"
                "• Google: <code>site:domain.com filetype:pdf</code>\n"
                "• Google: <code>site:domain.com filetype:xlsx</code>\n"
                "• Pastebin / GitHub — случайные утечки\n"
                "• Glassdoor — отзывы, технологии\n"
            ),
        },
        "subdomain": {
            "name": "Поиск субдоменов",
            "text": (
                "<b>Subdomain Enumeration</b>\n\n"
                "<b>Пассивные методы (не трогаем цель):</b>\n"
                "• <code>subfinder -d target.com -o subs.txt</code>\n"
                "• <code>amass enum -passive -d target.com</code>\n"
                "• crt.sh: <code>%.target.com</code> — SSL сертификаты\n"
                "• SecurityTrails.com — история DNS\n"
                "• DNSDumpster.com — граф инфраструктуры\n"
                "• Shodan: <code>ssl.cert.subject.cn:target.com</code>\n"
                "• Censys: <code>parsed.names: target.com</code>\n\n"
                "<b>Активные методы:</b>\n"
                "• <code>gobuster dns -d target.com -w subdomains.txt</code>\n"
                "• <code>ffuf -u https://FUZZ.target.com -w list.txt</code>\n"
                "• <code>dnsrecon -d target.com -t brt</code>\n\n"
                "<b>Wordlists:</b>\n"
                "• SecLists: /Discovery/DNS/\n"
                "• all.txt (мегалист Jhaddix)\n\n"
                "<b>Автоматизация пайплайн:</b>\n"
                "<code>subfinder -d target.com | httpx | nuclei -t exposures/</code>\n\n"
                "<b>Установка:</b>\n"
                "<code>go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest</code>\n"
            ),
        },
        "github_osint": {
            "name": "GitHub OSINT",
            "text": (
                "<b>GitHub OSINT — найди секреты в коде</b>\n\n"
                "<b>Поиск по организации:</b>\n"
                "<code>github.com/org/company-name</code>\n"
                "Репозитории, сотрудники, форки\n\n"
                "<b>GitHub Dorks — поиск секретов:</b>\n"
                "• <code>org:company password</code>\n"
                "• <code>org:company api_key</code>\n"
                "• <code>org:company secret_key</code>\n"
                "• <code>org:company aws_access_key_id</code>\n"
                "• <code>org:company BEGIN PRIVATE KEY</code>\n"
                "• <code>org:company smtp</code>\n\n"
                "<b>Инструменты поиска секретов:</b>\n"
                "• TruffleHog: <code>trufflehog github --org=company</code>\n"
                "• Gitleaks: <code>gitleaks detect --source=./repo</code>\n"
                "• GitDorker: автоматизация дорков\n\n"
                "<b>История коммитов:</b>\n"
                "• git log --all --full-history\n"
                "• Удалённые файлы через git show\n"
                "• GitHub: commit history → удалённые строки\n\n"
                "<b>Email из коммитов:</b>\n"
                "<code>git log --format='%ae' | sort -u</code>\n\n"
                "<b>Автоматизация:</b>\n"
                "<code>pip install trufflehog</code>\n"
            ),
        },
    }
},

# ─── СЕТЬ ─────────────────────────────────────────────────────
"network": {
    "name": "Сетевая разведка",
    "emoji": "🌐",
    "topics": {
        "shodan_mastery": {
            "name": "Shodan — полный гайд",
            "text": (
                "<b>Shodan — поисковик по интернету устройств</b>\n\n"
                "<b>Базовые запросы:</b>\n"
                "• <code>hostname:target.com</code> — хосты домена\n"
                "• <code>org:\"Company Name\"</code> — инфраструктура\n"
                "• <code>ip:1.2.3.4</code> — конкретный IP\n"
                "• <code>net:192.168.0.0/24</code> — сеть\n\n"
                "<b>Поиск по сервисам:</b>\n"
                "• <code>port:22 country:RU</code> — SSH в России\n"
                "• <code>port:3389 os:Windows</code> — RDP\n"
                "• <code>product:nginx version:1.14</code>\n"
                "• <code>http.title:\"Admin Panel\"</code>\n"
                "• <code>http.html:\"phpMyAdmin\"</code>\n\n"
                "<b>Поиск уязвимостей:</b>\n"
                "• <code>vuln:CVE-2021-44228</code> — Log4Shell\n"
                "• <code>has_vuln:true org:\"Target\"</code>\n\n"
                "<b>Сертификаты SSL:</b>\n"
                "• <code>ssl.cert.subject.cn:target.com</code>\n"
                "• <code>ssl:\"target.com\" 200</code>\n\n"
                "<b>Shodan CLI:</b>\n"
                "<code>pip install shodan</code>\n"
                "<code>shodan init YOUR_API_KEY</code>\n"
                "<code>shodan search 'org:\"Sberbank\"'</code>\n"
                "<code>shodan host 1.2.3.4</code>\n"
                "<code>shodan domain target.com</code>\n\n"
                "<b>Shodan Dorks база:</b>\n"
                "• <code>\"default password\" port:23</code> — Telnet\n"
                "• <code>webcamxp country:RU</code> — камеры\n"
                "• <code>\"MongoDB Server Information\" port:27017</code>\n"
                "• <code>\"Elasticsearch\" port:9200</code>\n"
            ),
        },
        "dns_recon": {
            "name": "DNS разведка",
            "text": (
                "<b>DNS Reconnaissance</b>\n\n"
                "<b>Базовые запросы:</b>\n"
                "<code>dig target.com ANY</code> — все записи\n"
                "<code>dig +short target.com MX</code> — почта\n"
                "<code>dig +short target.com TXT</code> — SPF/DKIM\n"
                "<code>nslookup -type=NS target.com</code>\n\n"
                "<b>Zone Transfer (если разрешён):</b>\n"
                "<code>dig axfr @ns1.target.com target.com</code>\n"
                "<code>host -l target.com ns1.target.com</code>\n\n"
                "<b>Reverse DNS:</b>\n"
                "<code>dig -x 1.2.3.4</code>\n"
                "<code>host 1.2.3.4</code>\n\n"
                "<b>История DNS:</b>\n"
                "• SecurityTrails.com — полная история\n"
                "• ViewDNS.info — история A записей\n"
                "• DNSHistory.org\n\n"
                "<b>Автоматизация:</b>\n"
                "<code>dnsrecon -d target.com -t std</code>\n"
                "<code>dnsx -d target.com -a -cname -mx -ns</code>\n"
                "<code>fierce --domain target.com</code>\n\n"
                "<b>Wildcard DNS обнаружение:</b>\n"
                "<code>dig randomstring.target.com</code>\n"
                "Если ответил — wildcard настроен\n"
            ),
        },
        "ip_recon": {
            "name": "IP разведка",
            "text": (
                "<b>IP OSINT — всё об IP адресе</b>\n\n"
                "<b>Базовая информация:</b>\n"
                "• ipinfo.io/1.2.3.4 — владелец, ASN, город\n"
                "• ip-api.com — геолокация и ISP\n"
                "• BGP.he.net — маршрутизация, BGP\n"
                "• RIPE NCC / ARIN / APNIC — whois\n\n"
                "<b>Репутация IP:</b>\n"
                "• VirusTotal.com — malware история\n"
                "• AbuseIPDB.com — abuse репорты\n"
                "• Talos Intelligence — Cisco\n"
                "• Shodan.io — открытые порты\n\n"
                "<b>Геолокация и трасировка:</b>\n"
                "<code>traceroute 1.2.3.4</code>\n"
                "<code>mtr 1.2.3.4</code> — лучше traceroute\n"
                "• Visualtraceroute.net — карта маршрута\n\n"
                "<b>IP → Домены (Reverse IP):</b>\n"
                "• ViewDNS.info/reverseip\n"
                "• Shodan: <code>ip:1.2.3.4</code>\n"
                "• HackerTarget reverse IP API\n\n"
                "<b>Диапазон IP компании:</b>\n"
                "<code>whois -h whois.radb.net '!gAS12345'</code>\n"
                "<code>amass intel -asn 12345</code>\n"
            ),
        },
    }
},

# ─── ГЕОЛОКАЦИЯ ───────────────────────────────────────────────
"geolocation": {
    "name": "Геолокация",
    "emoji": "📍",
    "topics": {
        "geo_photo": {
            "name": "Геолокация по фото",
            "text": (
                "<b>GeoINT — определи место по фото</b>\n\n"
                "<b>Шаг 1 — Метаданные:</b>\n"
                "<code>exiftool photo.jpg | grep GPS</code>\n"
                "Если есть GPS — дело сделано.\n\n"
                "<b>Шаг 2 — Визуальный анализ:</b>\n"
                "• Архитектура → регион/страна\n"
                "• Вывески → язык и алфавит\n"
                "• Номера машин → страна/регион\n"
                "• Растения и природа → климат\n"
                "• Электросети, дорожные знаки\n"
                "• Форма розеток через окна\n\n"
                "<b>Шаг 3 — Инструменты:</b>\n"
                "• Google Street View — сравни вручную\n"
                "• Yandex Panoramas — лучше для СНГ\n"
                "• SunCalc.org — сторона света по теням\n"
                "• Overpass Turbo — поиск объектов OpenStreetMap\n"
                "• What3Words — точная геолокация\n\n"
                "<b>Шаг 4 — Обратный поиск:</b>\n"
                "• Yandex Images — лучший для зданий\n"
                "• Google Images\n"
                "• Bing Visual Search\n\n"
                "<b>Тренировка навыка:</b>\n"
                "• GeoGuessr.com\n"
                "• GeoWizard YouTube\n"
                "• Bellingcat Geolocation Guides\n\n"
                "<b>Видео геолокация:</b>\n"
                "• InVID WeVerify — анализ кадров\n"
                "• YouTube Metadata Tool\n"
            ),
        },
        "geo_live": {
            "name": "Отслеживание в реальном времени",
            "text": (
                "<b>Live Geolocation OSINT</b>\n\n"
                "<b>Самолёты:</b>\n"
                "• FlightRadar24.com — все рейсы онлайн\n"
                "• FlightAware.com — история полётов\n"
                "• ADS-B Exchange — без фильтрации военных\n"
                "• OpenSky Network — API для исследователей\n\n"
                "<b>Корабли:</b>\n"
                "• MarineTraffic.com — суда онлайн\n"
                "• VesselFinder.com\n"
                "• ShipXplorer — военные корабли\n\n"
                "<b>Автомобили и транспорт:</b>\n"
                "• Waze — пробки и инциденты\n"
                "• OpenStreetMap — live данные\n\n"
                "<b>Военная техника:</b>\n"
                "• ADS-B Exchange — военные самолёты\n"
                "• Oryx blog — документация потерь\n"
                "• LiveUAMap — конфликты\n\n"
                "<b>Спутниковые снимки:</b>\n"
                "• Google Earth — история снимков\n"
                "• Sentinel Hub — бесплатные снимки ЕКА\n"
                "• Planet.com — ежедневные обновления\n"
                "• NASA Worldview\n\n"
                "<b>Погода для геолокации:</b>\n"
                "• Windy.com — ветер и погодные данные\n"
                "• Ventusky.com\n"
            ),
        },
        "geo_social": {
            "name": "Геолокация через соцсети",
            "text": (
                "<b>Social Media Geolocation</b>\n\n"
                "<b>Instagram:</b>\n"
                "• Геотеги в постах и Stories\n"
                "• Анализ фона фотографий\n"
                "• Check-in'ы в Stories\n"
                "• Метаданные до 2012 года\n\n"
                "<b>Twitter/X:</b>\n"
                "• Координаты в старых твитах\n"
                "• Поиск по геолокации API\n"
                "• <code>geocode:55.75,37.61,10km</code>\n\n"
                "<b>VK:</b>\n"
                "• Геометки в постах\n"
                "• Check-in история\n"
                "• Фото с геотегами\n\n"
                "<b>Telegram:</b>\n"
                "• People Nearby (если включено)\n"
                "• Геолокация в сообщениях\n\n"
                "<b>Автоматизация Twitter Geo:</b>\n"
                "<code>twint -u username --geo '55.75,37.61,5km'</code>\n\n"
                "<b>Инструменты:</b>\n"
                "• Echosec Systems — соцсети по геолокации\n"
                "• Geofeedia (коммерческий)\n"
                "• OneMillionTweetMap\n"
            ),
        },
    }
},

# ─── ДАРКНЕТ ──────────────────────────────────────────────────
"darkweb": {
    "name": "Dark Web OSINT",
    "emoji": "🕶",
    "topics": {
        "darkweb_intro": {
            "name": "Dark Web — базовый гайд",
            "text": (
                "<b>Dark Web OSINT — безопасный старт</b>\n\n"
                "<b>Инструменты доступа:</b>\n"
                "• Tor Browser — основной инструмент\n"
                "• Tails OS — максимальная анонимность\n"
                "• Whonix — VM с Tor\n\n"
                "<b>Поисковики .onion:</b>\n"
                "• Ahmia.fi — безопасный поисковик\n"
                "• Torch — старейший .onion поиск\n"
                "• DuckDuckGo .onion версия\n"
                "• Not Evil\n\n"
                "<b>Мониторинг утечек:</b>\n"
                "• HIBP: haveibeenpwned.com\n"
                "• DeHashed.com — платный, очень мощный\n"
                "• IntelligenceX.io\n"
                "• Leak-Lookup.com\n"
                "• BreachDirectory.org\n\n"
                "<b>Ransomware мониторинг:</b>\n"
                "• Ransomwatch.telemetry.ltd\n"
                "• ID Ransomware\n"
                "• Darkfeed.io\n\n"
                "<b>Правила безопасности:</b>\n"
                "• Никогда не используй основной браузер\n"
                "• Не скачивай файлы\n"
                "• Используй VPN + Tor\n"
                "• Не вводи личные данные\n"
                "• Работай в изолированной VM\n"
            ),
        },
        "leak_hunting": {
            "name": "Охота за утечками",
            "text": (
                "<b>Data Breach Hunting</b>\n\n"
                "<b>Бесплатные ресурсы:</b>\n"
                "• haveibeenpwned.com — email/phone\n"
                "• BreachDirectory.org — поиск по паролю\n"
                "• Snusbase.com — база утечек\n"
                "• LeakBase.pw\n\n"
                "<b>Платные (мощные):</b>\n"
                "• DeHashed.com — лучший для исследователей\n"
                "• IntelligenceX.io — архив всего\n"
                "• Flare Systems\n\n"
                "<b>Поиск по паролю (обратный поиск):</b>\n"
                "• BreachDirectory: <code>search?term=password123</code>\n"
                "• Помогает найти другие аккаунты человека\n\n"
                "<b>Автоматизация мониторинга:</b>\n"
                "• HIBP API — уведомления об утечках\n"
                "• Have I Been Pwned API:\n"
                "<code>curl https://haveibeenpwned.com/api/v3/breachedaccount/email</code>\n\n"
                "<b>GitHub поиск утечек:</b>\n"
                "• <code>password db_password</code>\n"
                "• <code>api_key secret_key</code>\n"
                "• TruffleHog для автоматического скана\n\n"
                "<b>Паста-сайты:</b>\n"
                "• Pastebin.com\n"
                "• Ghostbin.com\n"
                "• ControlC.com\n"
            ),
        },
    }
},

# ─── SOЦСЕТИ ──────────────────────────────────────────────────
"social": {
    "name": "Соцсети OSINT",
    "emoji": "📱",
    "topics": {
        "telegram_osint": {
            "name": "Telegram OSINT",
            "text": (
                "<b>Telegram OSINT — полный гайд</b>\n\n"
                "<b>Поиск людей:</b>\n"
                "• @username — прямой поиск\n"
                "• People Nearby — если геолокация включена\n"
                "• Добавь номер → покажет username\n"
                "• Поиск в публичных группах\n\n"
                "<b>Разведка групп и каналов:</b>\n"
                "• tgstat.ru — статистика каналов\n"
                "• telemetr.io — аналитика\n"
                "• combot.org — статистика чатов\n"
                "• telegago.com — поиск по Telegram\n\n"
                "<b>Telegram OSINT Tools:</b>\n"
                "• Telepathy: поиск и анализ групп\n"
                "<code>pip install telepathy-osint</code>\n"
                "• TGScanRobot — @tgscanrobot\n"
                "• Lyzem — поисковик по Telegram\n\n"
                "<b>Боты для разведки:</b>\n"
                "• @getidsbot — ID пользователя/группы\n"
                "• @username_to_id_bot\n"
                "• @SearcheeBot — поиск по каналам\n\n"
                "<b>Архивирование:</b>\n"
                "• TelegramArchiver\n"
                "• Telethon — Python библиотека\n"
                "<code>pip install telethon</code>\n\n"
                "<b>Анализ участников группы:</b>\n"
                "Через Telethon можно выгрузить всех участников группы и их данные\n"
            ),
        },
        "vk_osint": {
            "name": "VK OSINT",
            "text": (
                "<b>VK OSINT — разведка ВКонтакте</b>\n\n"
                "<b>Поиск людей:</b>\n"
                "• Поиск по имени + город + учёба\n"
                "• Поиск по номеру телефона\n"
                "• Общие друзья — строишь граф связей\n"
                "• Группы — интересы, геолокация\n\n"
                "<b>Скрытые данные:</b>\n"
                "• vk.com/id12345 — цифровой ID\n"
                "• API: vk.com/dev/users.get\n"
                "• Удалённые посты — через кэш\n"
                "• Фото с геотегами\n\n"
                "<b>VK Tools:</b>\n"
                "• Vklyucha.gg — расширенный поиск\n"
                "• VK Parser — парсинг данных\n"
                "• Maltego VK transform\n\n"
                "<b>VK API разведка:</b>\n"
                "<code>https://api.vk.com/method/users.get?user_ids=username&fields=all&v=5.131</code>\n\n"
                "<b>Группы и сообщества:</b>\n"
                "• Подписчики → связи между людьми\n"
                "• Геолокация через посты в группах\n"
                "• Администраторы групп → реальные личности\n\n"
                "<b>Wayback Machine для VK:</b>\n"
                "• web.archive.org/web/*/vk.com/username\n"
                "• Старые аватарки и посты\n"
            ),
        },
        "twitter_osint": {
            "name": "Twitter/X OSINT",
            "text": (
                "<b>Twitter/X OSINT</b>\n\n"
                "<b>Поиск Advanced:</b>\n"
                "• from:username — посты аккаунта\n"
                "• to:username — упоминания\n"
                "• geocode:55.75,37.61,10km — геолокация\n"
                "• since:2020-01-01 until:2020-12-31\n"
                "• filter:images filter:videos\n\n"
                "<b>Twint (без API):</b>\n"
                "<code>pip install twint</code>\n"
                "<code>twint -u username --year 2022</code>\n"
                "<code>twint -s keyword --geo '55.75,37.61,5km'</code>\n"
                "<code>twint -u username --email --phone</code>\n\n"
                "<b>Twitter Advanced Search:</b>\n"
                "• twitter.com/search-advanced\n"
                "• Все фильтры без кода\n\n"
                "<b>Анализ подписок:</b>\n"
                "• Followerwonk.com — анализ подписчиков\n"
                "• Socialblade.com — рост аккаунта\n\n"
                "<b>Deleted tweets:</b>\n"
                "• Wayback Machine\n"
                "• Politwoops — удалённые у политиков\n"
                "• Cacheview Google\n\n"
                "<b>Twitter OSINT Tools:</b>\n"
                "• Tinfoleak — полный анализ аккаунта\n"
                "• TweetDeck — мониторинг в реальном времени\n"
            ),
        },
    }
},

# ─── RED TEAM ─────────────────────────────────────────────────
"redteam": {
    "name": "Red Team Recon",
    "emoji": "🔴",
    "topics": {
        "rt_recon_full": {
            "name": "Полная разведка цели",
            "text": (
                "<b>Red Team Reconnaissance — полный чеклист</b>\n\n"
                "<b>Passive Recon (не касаемся цели):</b>\n"
                "• WHOIS: <code>whois target.com</code>\n"
                "• DNS: <code>dig target.com ANY</code>\n"
                "• theHarvester: <code>theHarvester -d target.com -b all</code>\n"
                "• Shodan: <code>org:\"Target Company\"</code>\n"
                "• Censys: SSL сертификаты\n"
                "• LinkedIn: сотрудники и технологии\n"
                "• GitHub: утечки в коде\n"
                "• Google Dorks (следующий топик)\n\n"
                "<b>Active Recon (трогаем цель):</b>\n"
                "• nmap: <code>nmap -sV -sC -p- target.com</code>\n"
                "• Masscan: быстрое сканирование\n"
                "• Nikto: <code>nikto -h https://target.com</code>\n"
                "• Gobuster: поиск директорий\n"
                "• Subfinder: субдомены\n\n"
                "<b>Инфраструктура карта:</b>\n"
                "• IP диапазоны (Shodan, BGP)\n"
                "• Субдомены (Subfinder, Amass)\n"
                "• Технологии (BuiltWith, Wappalyzer)\n"
                "• Сотрудники + email формат\n"
                "• Открытые порты и сервисы\n"
            ),
        },
        "google_dorks": {
            "name": "Google Dorks — полная база",
            "text": (
                "<b>Google Dorks — поиск скрытого</b>\n\n"
                "<b>Операторы:</b>\n"
                "• <code>site:</code> — ограничить сайтом\n"
                "• <code>filetype:</code> — тип файла\n"
                "• <code>intitle:</code> — в заголовке\n"
                "• <code>inurl:</code> — в URL\n"
                "• <code>intext:</code> — в тексте\n"
                "• <code>cache:</code> — кэш Google\n\n"
                "<b>Чувствительные файлы:</b>\n"
                "• <code>site:target.com filetype:pdf</code>\n"
                "• <code>site:target.com filetype:xlsx</code>\n"
                "• <code>site:target.com filetype:sql</code>\n"
                "• <code>site:target.com filetype:env</code>\n"
                "• <code>site:target.com ext:log</code>\n\n"
                "<b>Панели управления:</b>\n"
                "• <code>intitle:\"admin panel\" site:target.com</code>\n"
                "• <code>inurl:admin site:target.com</code>\n"
                "• <code>intitle:\"phpMyAdmin\" site:target.com</code>\n\n"
                "<b>Пароли и конфиги:</b>\n"
                "• <code>site:target.com intext:password</code>\n"
                "• <code>site:github.com target.com password</code>\n"
                "• <code>site:pastebin.com target.com</code>\n\n"
                "<b>Камеры и устройства:</b>\n"
                "• <code>intitle:\"webcamXP\" inurl:8080</code>\n"
                "• <code>inurl:\"viewerframe?mode=\"</code>\n\n"
                "<b>База Google Dorks:</b>\n"
                "• exploit-db.com/google-hacking-database\n"
                "• Тысячи готовых дорков\n"
            ),
        },
        "rt_infrastructure": {
            "name": "Атака на инфраструктуру",
            "text": (
                "<b>Infrastructure Attack Chain</b>\n\n"
                "<b>1. Обнаружение внешней поверхности атаки:</b>\n"
                "<code>amass enum -d target.com -o domains.txt</code>\n"
                "<code>subfinder -d target.com | httpx -title -tech-detect</code>\n"
                "<code>nuclei -l urls.txt -t exposures/ -t cves/</code>\n\n"
                "<b>2. Сканирование портов:</b>\n"
                "<code>masscan -p1-65535 --rate=1000 -iL ips.txt</code>\n"
                "<code>nmap -sV -sC -p$(cat ports.txt) -iL ips.txt</code>\n\n"
                "<b>3. Веб-разведка:</b>\n"
                "<code>whatweb https://target.com</code>\n"
                "<code>wafw00f https://target.com</code> — WAF детекция\n"
                "<code>gowitness file -f urls.txt</code> — скриншоты\n\n"
                "<b>4. Уязвимости:</b>\n"
                "<code>nuclei -u https://target.com -t cves/ -t exposures/</code>\n"
                "<code>nikto -h https://target.com -o report.html</code>\n\n"
                "<b>5. Автоматизация (ReconFTW):</b>\n"
                "<code>./reconftw.sh -d target.com -a</code>\n"
                "Делает всё сам: субдомены, порты, вебы, скрины\n"
            ),
        },
    }
},

# ─── ИНСТРУМЕНТЫ ──────────────────────────────────────────────
"tools": {
    "name": "Инструменты OSINT",
    "emoji": "🛠",
    "topics": {
        "top_tools": {
            "name": "Топ-20 инструментов",
            "text": (
                "<b>Топ-20 OSINT инструментов</b>\n\n"
                "<b>1. Maltego</b> — граф связей, визуализация\n"
                "<b>2. SpiderFoot</b> — автоматический OSINT фреймворк\n"
                "<code>spiderfoot -l 127.0.0.1:5001</code>\n"
                "<b>3. Recon-ng</b> — модульный фреймворк\n"
                "<code>recon-ng</code>\n"
                "<b>4. theHarvester</b> — email, субдомены, IP\n"
                "<code>theHarvester -d target.com -b all</code>\n"
                "<b>5. Shodan CLI</b> — поиск устройств\n"
                "<b>6. Sherlock</b> — поиск username\n"
                "<code>python3 sherlock.py username</code>\n"
                "<b>7. Maigret</b> — расширенный Sherlock\n"
                "<code>maigret username --html</code>\n"
                "<b>8. Holehe</b> — email → сайты\n"
                "<code>holehe email@test.com</code>\n"
                "<b>9. GHunt</b> — Google OSINT\n"
                "<code>ghunt email target@gmail.com</code>\n"
                "<b>10. PhoneInfoga</b> — телефон\n"
                "<code>phoneinfoga scan -n +7XXXXXXXXXX</code>\n"
                "<b>11. Subfinder</b> — субдомены\n"
                "<b>12. Amass</b> — ASN, субдомены, граф\n"
                "<b>13. Nuclei</b> — автосканирование уязвимостей\n"
                "<b>14. HTTPX</b> — проверка живых хостов\n"
                "<b>15. ExifTool</b> — метаданные файлов\n"
                "<b>16. TruffleHog</b> — секреты в коде\n"
                "<b>17. Osmedeus</b> — полный OSINT пайплайн\n"
                "<b>18. Twint</b> — Twitter без API\n"
                "<b>19. Telepathy</b> — Telegram OSINT\n"
                "<b>20. ReconFTW</b> — автоматизация всего\n"
            ),
        },
        "osint_frameworks": {
            "name": "OSINT фреймворки",
            "text": (
                "<b>OSINT Frameworks — обзор</b>\n\n"
                "<b>SpiderFoot:</b>\n"
                "• 200+ модулей автоматически\n"
                "• Email, IP, домен, имя, телефон\n"
                "<code>pip install spiderfoot</code>\n"
                "<code>spiderfoot -l 0.0.0.0:5001</code>\n\n"
                "<b>Maltego CE (бесплатный):</b>\n"
                "• Визуальный граф связей\n"
                "• Transforms: Shodan, VirusTotal, HIBP\n"
                "• Идеален для презентации результатов\n\n"
                "<b>Recon-ng:</b>\n"
                "• Модульная архитектура\n"
                "• marketplace install all\n"
                "• Сохранение в БД\n\n"
                "<b>OSINT Framework (osintframework.com):</b>\n"
                "• Дерево всех OSINT ресурсов\n"
                "• Категории: люди, соцсети, домены, email\n\n"
                "<b>Hunchly:</b>\n"
                "• Расширение Chrome\n"
                "• Автоматическое сохранение страниц\n"
                "• Хронология расследования\n\n"
                "<b>Mitaka:</b>\n"
                "• Расширение Chrome\n"
                "• Клик → автоматический поиск в 50+ сервисах\n"
            ),
        },
        "osint_distros": {
            "name": "OSINT дистрибутивы",
            "text": (
                "<b>OSINT Linux Distros</b>\n\n"
                "<b>Kali Linux:</b>\n"
                "• Самый популярный\n"
                "• Встроен: theHarvester, Maltego, Recon-ng\n"
                "• kali.org/get-kali\n\n"
                "<b>Trace Labs OSINT VM:</b>\n"
                "• Специально для OSINT расследований\n"
                "• Предустановлено 30+ OSINT инструментов\n"
                "• tracelabs.org/initiatives/osint-vm\n\n"
                "<b>Tails OS:</b>\n"
                "• Максимальная анонимность\n"
                "• Всё через Tor\n"
                "• Не оставляет следов\n"
                "• tails.boum.org\n\n"
                "<b>Whonix:</b>\n"
                "• VM с изолированным Tor\n"
                "• Двойной шлюз\n"
                "• whonix.org\n\n"
                "<b>Parrot OS:</b>\n"
                "• Лёгкий аналог Kali\n"
                "• Встроен OSINT инструментарий\n"
                "• parrotsec.org\n\n"
                "<b>Быстрая установка всего в Ubuntu:</b>\n"
                "<code>git clone https://github.com/laramies/theHarvester</code>\n"
                "<code>pip install shodan holehe maigret ghunt</code>\n"
            ),
        },
    }
},

# ─── АНОНИМНОСТЬ ──────────────────────────────────────────────
"opsec": {
    "name": "OpSec & Анонимность",
    "emoji": "🛡",
    "topics": {
        "opsec_basics": {
            "name": "OpSec для исследователя",
            "text": (
                "<b>OpSec — защити себя при OSINT</b>\n\n"
                "<b>Базовые правила:</b>\n"
                "• Никогда не исследуй с личного аккаунта\n"
                "• Создай sock puppet аккаунты\n"
                "• Используй VPN + VM\n"
                "• Разные браузеры для разных задач\n\n"
                "<b>Изоляция инструментов:</b>\n"
                "• VM (VirtualBox / VMware) для OSINT работы\n"
                "• Snapshots — откат после сессии\n"
                "• Tails OS для максимальной анонимности\n\n"
                "<b>Sock Puppet создание:</b>\n"
                "• Отдельный телефон/SIM\n"
                "• Временный email: temp-mail.org\n"
                "• Отдельный браузер профиль\n"
                "• VPN включён при создании\n"
                "• Реалистичная история аккаунта\n\n"
                "<b>VPN выбор:</b>\n"
                "• Mullvad — без логов, оплата Monero\n"
                "• ProtonVPN — швейцарская юрисдикция\n"
                "• IVPN — минималистичный, без логов\n\n"
                "<b>Браузер для OSINT:</b>\n"
                "• Firefox + uBlock Origin + Canvas Blocker\n"
                "• Brave — встроенная защита\n"
                "• Tor Browser — максимум анонимности\n\n"
                "<b>Проверка утечек:</b>\n"
                "• ipleak.net — WebRTC утечки\n"
                "• browserleaks.com — фингерпринт\n"
            ),
        },
        "sock_puppet": {
            "name": "Создание Sock Puppet",
            "text": (
                "<b>Sock Puppet — легенда для OSINT</b>\n\n"
                "<b>Что такое sock puppet:</b>\n"
                "Фиктивный аккаунт для безопасного исследования\n"
                "без раскрытия реальной личности\n\n"
                "<b>Создание личности:</b>\n"
                "• Сгенерируй имя: fakenamegenerator.com\n"
                "• Лицо: thispersondoesnotexist.com\n"
                "• Биография: реалистичная, не привлекающая внимание\n"
                "• Дата рождения: 25-35 лет\n\n"
                "<b>Инфраструктура:</b>\n"
                "• Временный email: guerrillamail.com, temp-mail.org\n"
                "• Виртуальный номер: SMS-Activate, SMSPVA\n"
                "• VPN включён с самого начала\n"
                "• Отдельный браузер профиль\n\n"
                "<b>Прогрев аккаунта:</b>\n"
                "• Не используй сразу для разведки\n"
                "• Несколько недель активности\n"
                "• Подпишись на нейтральные аккаунты\n"
                "• Пости нейтральный контент\n\n"
                "<b>Правила использования:</b>\n"
                "• Никогда не смешивай с реальным аккаунтом\n"
                "• Отдельная VM для каждого puppet\n"
                "• Разные пароли (менеджер паролей)\n"
                "• Никогда не логинься без VPN\n"
            ),
        },
    }
},

}

# ── МИССИИ (квесты с наградой) ────────────────
MISSIONS = [
    {"id":"m_person",  "name":"Person OSINT",      "module":"people",    "reward":300},
    {"id":"m_company", "name":"Company OSINT",     "module":"companies", "reward":350},
    {"id":"m_shodan",  "name":"Shodan Mastery",    "module":"network",   "reward":400},
    {"id":"m_geo",     "name":"Геолокация по фото","module":"geolocation","reward":450},
    {"id":"m_dark",    "name":"Dark Web OSINT",    "module":"darkweb",   "reward":400},
    {"id":"m_tg",      "name":"Telegram OSINT",    "module":"social",    "reward":350},
    {"id":"m_rt",      "name":"Red Team Recon",    "module":"redteam",   "reward":500},
    {"id":"m_tools",   "name":"OSINT Инструменты", "module":"tools",     "reward":300},
    {"id":"m_opsec",   "name":"OpSec Setup",       "module":"opsec",     "reward":400},
    {"id":"m_dorks",   "name":"Google Dorks",      "module":"redteam",   "reward":350},
    {"id":"m_leaks",   "name":"Leak Hunting",      "module":"darkweb",   "reward":450},
    {"id":"m_sub",     "name":"Subdomain Enum",    "module":"companies", "reward":400},
]

REMINDER_TEXTS = [
    "Новый пост на @holazc_info. Зайди.",
    "Казино открыто. Испытай удачу.",
    "Новые OSINT техники в боте. Изучи.",
    "Твой стрик под угрозой. Зайди сегодня.",
    "Миссии ждут. Выполни и прокачайся.",
]

GATE_TEXTS = [
    "<b>СТОП.</b>\n\nТолько для подписчиков @holazc_info.\nПодпишись — потом заходи.",
    "<b>ДОСТУП ЗАКРЫТ.</b>\n\nПодпишись на @holazc_info.",
    "<b>АВТОРИЗАЦИЯ ПРОВАЛЕНА.</b>\n\nТолько подписчики @holazc_info имеют доступ.",
]

# ── БАЗА ──────────────────────────────────────

def init_db():
    with sqlite3.connect("promo.db") as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id       INTEGER PRIMARY KEY,
            username      TEXT, first_name TEXT,
            referred_by   INTEGER, joined_at TIMESTAMP,
            points        INTEGER DEFAULT 0,
            active        INTEGER DEFAULT 1,
            vip           INTEGER DEFAULT 0,
            level         INTEGER DEFAULT 0,
            streak        INTEGER DEFAULT 0,
            last_visit    TIMESTAMP,
            last_daily    TIMESTAMP,
            daily_bonus   INTEGER DEFAULT 1,
            last_wheel    TIMESTAMP,
            wheel_count   INTEGER DEFAULT 0,
            casino_games  INTEGER DEFAULT 0,
            casino_wins   INTEGER DEFAULT 0,
            casino_profit INTEGER DEFAULT 0,
            missions_done TEXT DEFAULT '',
            custom_title  TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY, value TEXT
        )""")
        c.execute("INSERT OR IGNORE INTO settings VALUES ('last_post_id','0')")
        c.commit()

def D(): return sqlite3.connect("promo.db")
def get_user(uid):
    with D() as c: return c.execute("SELECT * FROM users WHERE user_id=?", (uid,)).fetchone()

def add_user(uid, username, first_name, referred_by=None):
    with D() as c:
        c.execute(
            "INSERT OR IGNORE INTO users (user_id,username,first_name,referred_by,joined_at,daily_bonus) VALUES(?,?,?,?,?,1)",
            (uid, username, first_name, referred_by, datetime.now())
        )
        c.commit()

def upd(uid, **kw):
    if not kw: return
    s = ", ".join(f"{k}=?" for k in kw)
    with D() as c:
        c.execute(f"UPDATE users SET {s} WHERE user_id=?", list(kw.values())+[uid])
        c.commit()

def add_pts(uid, amount):
    with D() as c:
        c.execute("UPDATE users SET points=points+? WHERE user_id=?", (amount, uid))
        c.commit()
    check_level_up(uid)

def get_ref_count(uid):
    with D() as c: return c.execute("SELECT COUNT(*) FROM users WHERE referred_by=?", (uid,)).fetchone()[0]

def get_all_active():
    with D() as c: return [r[0] for r in c.execute("SELECT user_id FROM users WHERE active=1").fetchall()]

def get_total():
    with D() as c: return c.execute("SELECT COUNT(*) FROM users").fetchone()[0]

def get_setting(key):
    with D() as c:
        r = c.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return r[0] if r else "0"

def set_setting(key, val):
    with D() as c:
        c.execute("INSERT OR REPLACE INTO settings VALUES(?,?)", (key, str(val)))
        c.commit()

def mark_inactive(uid):
    with D() as c:
        c.execute("UPDATE users SET active=0 WHERE user_id=?", (uid,))
        c.commit()

def get_level(pts):
    lvl = 0
    for l,(n,req) in LEVELS.items():
        if pts >= req: lvl = l
    return lvl

def get_league(pts):
    lg = LEAGUES[0][0]
    for name,req in LEAGUES:
        if pts >= req: lg = name
    return lg

def check_level_up(uid):
    row = get_user(uid)
    if not row: return None
    new = get_level(row[5])
    if new > row[8]:
        upd(uid, level=new)
        return new
    return None

def update_streak(uid):
    row = get_user(uid)
    if not row: return 0, 0
    now    = datetime.now()
    last   = row[10]; streak = row[9]
    if last:
        diff = (now - datetime.fromisoformat(str(last))).total_seconds()
        if 86400 <= diff < 172800: streak += 1
        elif diff >= 172800: streak = 1
    else: streak = 1
    daily_earned = 0
    last_d = row[11]; daily = int(row[12] or 1)
    if not last_d or (now - datetime.fromisoformat(str(last_d))).total_seconds() >= 86400:
        daily_earned = min(daily * 10, 500)
        add_pts(uid, daily_earned)
        upd(uid, streak=streak, last_visit=now, daily_bonus=min(daily+1,50), last_daily=now)
    else:
        upd(uid, streak=streak, last_visit=now)
    return streak, daily_earned

def get_missions_done(uid):
    row = get_user(uid)
    if not row or not row[18]: return []
    return [m for m in row[18].split(",") if m]

def get_top_pts(n=10):
    with D() as c:
        return c.execute("SELECT first_name,username,points FROM users ORDER BY points DESC LIMIT ?", (n,)).fetchall()

def get_top_refs(n=10):
    with D() as c:
        return c.execute("""
            SELECT u.first_name,u.username,COUNT(*) cnt
            FROM users u2 JOIN users u ON u.user_id=u2.referred_by
            WHERE u2.referred_by IS NOT NULL
            GROUP BY u2.referred_by ORDER BY cnt DESC LIMIT ?
        """, (n,)).fetchall()

# ── ПОДПИСКА ──────────────────────────────────

async def is_subbed(uid, ctx):
    if uid in ADMIN_IDS: return True
    try:
        m = await ctx.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=uid)
        return m.status in ["member","administrator","creator","restricted"]
    except Exception: return False

def sub_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("ПОДПИСАТЬСЯ", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}")],
        [InlineKeyboardButton("Я подписался ✓", callback_data="check_sub")]
    ])

def home_kb(vip=False):
    kb = [
        [InlineKeyboardButton("Профиль",      callback_data="profile"),
         InlineKeyboardButton("Рейтинг",      callback_data="top_menu")],
        [InlineKeyboardButton("Казино",        callback_data="casino_menu"),
         InlineKeyboardButton("Колесо удачи", callback_data="wheel")],
        [InlineKeyboardButton("Дн. бонус",    callback_data="daily"),
         InlineKeyboardButton("Пригласить",   callback_data="ref")],
        [InlineKeyboardButton("OSINT база",    callback_data="osint_cats"),
         InlineKeyboardButton("Миссии",       callback_data="missions")],
    ]
    if vip: kb.append([InlineKeyboardButton("VIP РАЗДЕЛ", callback_data="vip")])
    return InlineKeyboardMarkup(kb)

BK = InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="home")]])

# ── START ─────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        user = update.callback_query.from_user
        send = update.callback_query.edit_message_text
    else:
        user = update.effective_user
        send = update.message.reply_text

    if not get_user(user.id):
        ref_id = None
        if context.args and context.args[0].isdigit() and int(context.args[0]) != user.id:
            ref_id = int(context.args[0])
        add_user(user.id, user.username, user.first_name, ref_id)
        if ref_id:
            add_pts(ref_id, 150)
            refs = get_ref_count(ref_id)
            if refs >= 5: upd(ref_id, vip=1)
            try: await context.bot.send_message(ref_id, f"Новый реферал — {user.first_name}. +150. Всего: {refs}")
            except Exception: pass

    streak, daily = update_streak(user.id)
    if not await is_subbed(user.id, context):
        await send(random.choice(GATE_TEXTS), parse_mode=ParseMode.HTML, reply_markup=sub_kb())
        return

    row    = get_user(user.id)
    lvl    = row[8]; pts = row[5]
    title  = row[19] or LEVELS[min(lvl,19)][0]
    league = get_league(pts)
    d_txt  = f"  +{daily} бонус!" if daily else ""
    s_icon = " 🔥" if streak >= 7 else ""

    await send(
        f"<b>{title}</b> | {league}\n"
        f"Ур.{lvl}/19 | {pts} pts{d_txt}\n"
        f"Стрик: {streak} дн.{s_icon} | Агентов: {get_total()}\n\n"
        f"Выбери действие:",
        parse_mode=ParseMode.HTML, reply_markup=home_kb(bool(row[7]))
    )

# ── CALLBACKS ─────────────────────────────────

async def cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid   = query.from_user.id
    data  = query.data

    if data == "check_sub":
        if await is_subbed(uid, context):
            await query.answer("Доступ разрешён.")
            await start(update, context)
        else:
            await query.answer("Подпишись на @holazc_info и нажми снова.", show_alert=True)
        return

    if not await is_subbed(uid, context):
        await query.answer("Сначала подпишись на @holazc_info", show_alert=True)
        return

    await query.answer()
    row = get_user(uid)
    if not row: return

    # ── ПРОФИЛЬ ──────────────────────────────
    if data == "profile":
        refs   = get_ref_count(uid); lvl = row[8]; pts = row[5]
        nxt    = LEVELS[min(lvl+1,19)][1]; cur = LEVELS[min(lvl,19)][1]
        prog   = int((pts-cur)/max(nxt-cur,1)*10)
        bar    = "█"*prog+"░"*(10-prog)
        done   = len(get_missions_done(uid))
        profit = row[17] or 0
        psign  = "+" if profit >= 0 else ""
        await query.edit_message_text(
            f"<b>[ ПРОФИЛЬ ]</b>\n\n"
            f"Титул: <b>{row[19] or LEVELS[min(lvl,19)][0]}</b>\n"
            f"Уровень: <b>{LEVELS[min(lvl,19)][0]}</b> [{lvl}/19]\n"
            f"[{bar}] {pts}/{nxt}\n"
            f"Лига: <b>{get_league(pts)}</b>\n"
            f"Баллы: <b>{pts}</b> | Рефералы: <b>{refs}</b>\n"
            f"Стрик: <b>{row[9]} дн.</b>\n"
            f"Миссии: <b>{done}/{len(MISSIONS)}</b>\n"
            f"Казино: <b>{row[15]} игр</b> | профит: <b>{psign}{profit}</b>",
            parse_mode=ParseMode.HTML, reply_markup=BK
        )

    # ── РЕЙТИНГ ──────────────────────────────
    elif data == "top_menu":
        await query.edit_message_text("<b>[ РЕЙТИНГ ]</b>", parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("По баллам",    callback_data="top_pts"),
                 InlineKeyboardButton("По рефералам", callback_data="top_refs")],
                [InlineKeyboardButton("Назад", callback_data="home")]
            ])
        )
    elif data in ("top_pts","top_refs"):
        if data == "top_pts":
            rows = get_top_pts(10); t = "ТОП БАЛЛЫ"
            lines = [f"{i}. {'@'+u if u else n} — {c}pts" for i,(n,u,c) in enumerate(rows,1)]
        else:
            rows = get_top_refs(10); t = "ТОП РЕФЕРАЛЫ"
            lines = [f"{i}. {'@'+u if u else n} — {c}" for i,(n,u,c) in enumerate(rows,1)]
        await query.edit_message_text(
            f"<b>[ {t} ]</b>\n\n" + ("\n".join(lines) or "Пока пусто."),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="top_menu")]])
        )

    # ── КАЗИНО ───────────────────────────────
    elif data == "casino_menu":
        await query.edit_message_text(
            f"<b>[ КАЗИНО ]</b>\n\nТвои баллы: <b>{row[5]}</b>\n\nВыбери игру:",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🪙 Монетка  x1.5 или -ставка", callback_data="casino_coin")],
                [InlineKeyboardButton("🎲 Кубик    x2 или -ставка",   callback_data="casino_dice")],
                [InlineKeyboardButton("🎰 Слоты    до x10 джекпот",   callback_data="casino_slots")],
                [InlineKeyboardButton("🃏 Блэкджек  x2 или -ставка",  callback_data="casino_bj")],
                [InlineKeyboardButton("Назад", callback_data="home")]
            ])
        )
    elif data in ("casino_coin","casino_dice","casino_slots","casino_bj"):
        bets = [b for b in [10,25,50,100,250,500,1000] if b <= row[5]]
        if not bets:
            await query.answer("Недостаточно баллов. Минимум 10.", show_alert=True)
            return
        context.user_data["cg"] = data
        gnames = {"casino_coin":"🪙 МОНЕТКА","casino_dice":"🎲 КУБИК","casino_slots":"🎰 СЛОТЫ","casino_bj":"🃏 БЛЭКДЖЕК"}
        kb = [[InlineKeyboardButton(f"Ставка {b}", callback_data=f"cbet_{b}")] for b in bets]
        kb.append([InlineKeyboardButton("Назад", callback_data="casino_menu")])
        await query.edit_message_text(
            f"<b>[ {gnames[data]} ]</b>\n\nБаллы: <b>{row[5]}</b>\n\nВыбери ставку:",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb)
        )
    elif data.startswith("cbet_"):
        bet  = int(data.split("_")[1]); game = context.user_data.get("cg","casino_coin"); pts = row[5]
        if pts < bet:
            await query.answer("Недостаточно баллов.", show_alert=True); return
        upd(uid, casino_games=(row[15] or 0)+1)
        result = ""
        if game == "casino_coin":
            if random.random() < 0.45:
                gain = int(bet*0.5); add_pts(uid, gain)
                upd(uid, casino_wins=(row[16] or 0)+1, casino_profit=(row[17] or 0)+gain)
                result = f"🪙 ОРЁЛ!\n\nСтавка: {bet}\n<b>+{gain} (x1.5)</b>\nБаланс: {pts+gain}"
            else:
                add_pts(uid, -bet); upd(uid, casino_profit=(row[17] or 0)-bet)
                result = f"🪙 РЕШКА.\n\nСтавка: {bet}\n<b>-{bet}</b>\nБаланс: {pts-bet}"
        elif game == "casino_dice":
            y = random.randint(1,6); h = random.randint(1,6)
            if y > h:
                add_pts(uid, bet); upd(uid, casino_wins=(row[16] or 0)+1, casino_profit=(row[17] or 0)+bet)
                result = f"🎲 Ты:{y} Казино:{h}\n\n<b>ПОБЕДА! +{bet}</b>\nБаланс: {pts+bet}"
            elif y == h:
                result = f"🎲 Ты:{y} Казино:{h}\n\nНИЧЬЯ.\nБаланс: {pts}"
            else:
                add_pts(uid, -bet); upd(uid, casino_profit=(row[17] or 0)-bet)
                result = f"🎲 Ты:{y} Казино:{h}\n\n<b>ПРОИГРЫШ. -{bet}</b>\nБаланс: {pts-bet}"
        elif game == "casino_slots":
            sy = ["7️⃣","💎","🔔","⭐","🍋","🍒","🍊","🎯"]
            s1,s2,s3 = random.choice(sy),random.choice(sy),random.choice(sy)
            if s1==s2==s3=="7️⃣":
                gain=bet*10; add_pts(uid,gain); upd(uid,casino_wins=(row[16] or 0)+1,casino_profit=(row[17] or 0)+gain)
                result=f"🎰 {s1}{s2}{s3}\n\n<b>ДЖЕКПОТ!!! x10\n+{gain}</b>\nБаланс:{pts+gain}"
            elif s1==s2==s3:
                gain=bet*5; add_pts(uid,gain); upd(uid,casino_wins=(row[16] or 0)+1,casino_profit=(row[17] or 0)+gain)
                result=f"🎰 {s1}{s2}{s3}\n\n<b>ТРИ В РЯД! x5\n+{gain}</b>\nБаланс:{pts+gain}"
            elif s1==s2 or s2==s3 or s1==s3:
                gain=int(bet*0.5); add_pts(uid,gain)
                result=f"🎰 {s1}{s2}{s3}\n\nДва в ряд. x1.5\n+{gain}\nБаланс:{pts+gain}"
            else:
                add_pts(uid,-bet); upd(uid,casino_profit=(row[17] or 0)-bet)
                result=f"🎰 {s1}{s2}{s3}\n\nМимо.\n-{bet}\nБаланс:{pts-bet}"
        elif game == "casino_bj":
            def hnd():
                c = [random.randint(2,11),random.randint(2,11)]
                while sum(c)<16: c.append(random.randint(2,11))
                return c
            yc=hnd(); hc=hnd(); ys=sum(yc); hs=sum(hc)
            if ys>21:
                add_pts(uid,-bet); upd(uid,casino_profit=(row[17] or 0)-bet)
                result=f"🃏 Твои:{yc}={ys}\n\n<b>ПЕРЕБОР! -{bet}</b>\nБаланс:{pts-bet}"
            elif hs>21 or ys>hs:
                add_pts(uid,bet); upd(uid,casino_wins=(row[16] or 0)+1,casino_profit=(row[17] or 0)+bet)
                result=f"🃏 Ты:{yc}={ys} Казино:{hc}={hs}\n\n<b>ПОБЕДА! +{bet}</b>\nБаланс:{pts+bet}"
            elif ys==hs:
                result=f"🃏 Ты:{yc}={ys} Казино:{hc}={hs}\n\nНИЧЬЯ.\nБаланс:{pts}"
            else:
                add_pts(uid,-bet); upd(uid,casino_profit=(row[17] or 0)-bet)
                result=f"🃏 Ты:{yc}={ys} Казино:{hc}={hs}\n\n<b>Проигрыш. -{bet}</b>\nБаланс:{pts-bet}"
        new_lvl = check_level_up(uid)
        lvl_txt = f"\n\n<b>НОВЫЙ УРОВЕНЬ: {LEVELS[new_lvl][0]}!</b>" if new_lvl else ""
        await query.edit_message_text(
            f"<b>[ КАЗИНО ]</b>\n\n{result}{lvl_txt}",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Играть ещё", callback_data=game),
                 InlineKeyboardButton("Назад",      callback_data="casino_menu")]
            ])
        )

    # ── КОЛЕСО ───────────────────────────────
    elif data == "wheel":
        now = datetime.now(); last = row[13]
        if last and (now - datetime.fromisoformat(str(last))).total_seconds() < 3600:
            secs = 3600 - int((now - datetime.fromisoformat(str(last))).total_seconds())
            await query.answer(f"Через {secs//60}м {secs%60}с", show_alert=True); return
        prizes = [(50,500),(200,200),(300,100),(400,75),(350,50),(500,30),(250,150),(600,25)]
        win = random.choices(prizes, weights=[w[0] for w in prizes])[0][1]
        add_pts(uid, win); upd(uid, last_wheel=now, wheel_count=(row[14] or 0)+1)
        new_lvl = check_level_up(uid)
        lvl_txt = f"\n<b>НОВЫЙ УРОВЕНЬ: {LEVELS[new_lvl][0]}!</b>" if new_lvl else ""
        await query.edit_message_text(
            f"<b>[ КОЛЕСО УДАЧИ ]</b>\n\n<b>+{win} баллов!</b>{lvl_txt}\n\nСнова через час.",
            parse_mode=ParseMode.HTML, reply_markup=BK
        )

    # ── ДНЕВНОЙ БОНУС ────────────────────────
    elif data == "daily":
        now = datetime.now(); last_d = row[11]; daily = int(row[12] or 1)
        if last_d and (now - datetime.fromisoformat(str(last_d))).total_seconds() < 86400:
            secs = 86400 - int((now - datetime.fromisoformat(str(last_d))).total_seconds())
            await query.answer(f"Через {secs//3600}ч {(secs%3600)//60}мин.", show_alert=True); return
        earned = min(daily*10, 500)
        add_pts(uid, earned); upd(uid, daily_bonus=min(daily+1,50), last_daily=now)
        await query.edit_message_text(
            f"<b>[ ЕЖЕДНЕВНЫЙ БОНУС ]</b>\n\n<b>+{earned} баллов!</b>\nДень {daily}/50\n\nЗавтра: +{min((daily+1)*10,500)}",
            parse_mode=ParseMode.HTML, reply_markup=BK
        )

    # ── РЕФЕРАЛ ──────────────────────────────
    elif data == "ref":
        bot_name = (await context.bot.get_me()).username
        link = f"https://t.me/{bot_name}?start={uid}"
        refs = get_ref_count(uid)
        await query.edit_message_text(
            f"<b>[ ПРИГЛАШЕНИЕ ]</b>\n\nЗа каждого — <b>150 pts</b>\n5 рефов → <b>VIP</b>\n\n"
            f"Приглашено: <b>{refs}</b> | До VIP: <b>{max(0,5-refs)}</b>\n\n<code>{link}</code>",
            parse_mode=ParseMode.HTML, reply_markup=BK
        )

    # ── OSINT КАТЕГОРИИ ──────────────────────
    elif data == "osint_cats":
        kb = [[InlineKeyboardButton(f"{v['emoji']} {v['name']}", callback_data=f"ocat_{k}")]
              for k,v in OSINT_MODULES.items()]
        kb.append([InlineKeyboardButton("Назад", callback_data="home")])
        await query.edit_message_text(
            "<b>[ OSINT БАЗА ЗНАНИЙ ]</b>\n\nВыбери раздел:",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb)
        )

    elif data.startswith("ocat_"):
        cat = data[5:]
        mod = OSINT_MODULES.get(cat)
        if not mod:
            await query.edit_message_text("Не найдено.", reply_markup=BK); return
        kb = [[InlineKeyboardButton(t["name"], callback_data=f"otopic_{cat}_{tid}")]
              for tid,t in mod["topics"].items()]
        kb.append([InlineKeyboardButton("Назад", callback_data="osint_cats")])
        await query.edit_message_text(
            f"<b>[ {mod['emoji']} {mod['name'].upper()} ]</b>\n\nВыбери тему:",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb)
        )

    elif data.startswith("otopic_"):
        parts = data[7:].split("_", 1)
        cat = parts[0]; tid = parts[1]
        mod = OSINT_MODULES.get(cat)
        if not mod or tid not in mod["topics"]:
            await query.edit_message_text("Не найдено.", reply_markup=BK); return
        topic = mod["topics"][tid]
        await query.edit_message_text(
            topic["text"],
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data=f"ocat_{cat}")]])
        )

    # ── МИССИИ ───────────────────────────────
    elif data == "missions":
        done = get_missions_done(uid)
        kb = []
        for m in MISSIONS:
            status = "✓ " if m["id"] in done else ""
            kb.append([InlineKeyboardButton(f"{status}{m['name']} +{m['reward']}pts",
                                            callback_data=f"mission_{m['id']}")])
        kb.append([InlineKeyboardButton("Назад", callback_data="home")])
        cnt = sum(1 for m in MISSIONS if m["id"] in done)
        await query.edit_message_text(
            f"<b>[ МИССИИ ]</b>\n\nВыполнено: {cnt}/{len(MISSIONS)}\n\nВыбери миссию:",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb)
        )

    elif data.startswith("mission_"):
        mid  = data[8:]
        m    = next((x for x in MISSIONS if x["id"] == mid), None)
        if not m:
            await query.edit_message_text("Не найдено.", reply_markup=BK); return
        done = get_missions_done(uid)
        cat  = m["module"]; mod = OSINT_MODULES.get(cat, {})
        topics_list = "\n".join([f"• {t['name']}" for t in mod.get("topics", {}).values()])
        status = "✓ ВЫПОЛНЕНО" if mid in done else f"Награда: {m['reward']} pts"
        kb = []
        if mid not in done:
            kb.append([InlineKeyboardButton(f"Выполнить (+{m['reward']} pts)", callback_data=f"complete_{mid}")])
        kb.append([InlineKeyboardButton("Открыть раздел", callback_data=f"ocat_{cat}")])
        kb.append([InlineKeyboardButton("Назад", callback_data="missions")])
        await query.edit_message_text(
            f"<b>[ {m['name']} ]</b>\n{status}\n\n"
            f"Изучи раздел и выполни миссию.\n\n"
            f"<b>Темы раздела:</b>\n{topics_list}",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(kb)
        )

    elif data.startswith("complete_"):
        mid  = data[9:]
        done = get_missions_done(uid)
        if mid in done:
            await query.answer("Уже выполнено.", show_alert=True); return
        m = next((x for x in MISSIONS if x["id"] == mid), None)
        if not m: return
        done.append(mid)
        upd(uid, missions_done=",".join(done))
        add_pts(uid, m["reward"])
        new_lvl = check_level_up(uid)
        lvl_txt = f"\n<b>НОВЫЙ УРОВЕНЬ: {LEVELS[new_lvl][0]}!</b>" if new_lvl else ""
        await query.edit_message_text(
            f"<b>МИССИЯ ВЫПОЛНЕНА</b>\n\n{m['name']}\n<b>+{m['reward']} pts</b>{lvl_txt}",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="missions")]])
        )

    # ── VIP ──────────────────────────────────
    elif data == "vip":
        if not row[7]:
            await query.answer("VIP не активен. Пригласи 5 человек.", show_alert=True); return
        await query.edit_message_text(
            "<b>[ VIP РАЗДЕЛ ]</b>\n\nКанал: @holazc_info\nЗакрытые материалы только для своих.",
            parse_mode=ParseMode.HTML, reply_markup=BK
        )

    elif data == "home":
        await start(update, context)

# ── АВТОМАТИКА ────────────────────────────────

async def auto_repost(bot):
    try:
        last_id = int(get_setting("last_post_id"))
        users   = get_all_active()
        for mid in range(last_id+1, last_id+15):
            sent = 0
            for uid in users:
                try:
                    await bot.forward_message(chat_id=uid, from_chat_id=CHANNEL_ID, message_id=mid)
                    sent += 1; await asyncio.sleep(0.05)
                except Exception: pass
            if sent > 0: set_setting("last_post_id", mid); break
    except Exception as e: logging.error(f"repost: {e}")

async def send_reminder(bot):
    for uid in get_all_active():
        try:
            await bot.send_message(uid, random.choice(REMINDER_TEXTS))
            await asyncio.sleep(0.05)
        except Exception: mark_inactive(uid)

async def j_repost(ctx): await auto_repost(ctx.bot)
async def j_remind(ctx): await send_reminder(ctx.bot)

# ── АДМИН ────────────────────────────────────

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    tp = get_top_pts(3); tr = get_top_refs(3)
    p_txt = "\n".join([f"  {'@'+u if u else n}—{c}pts" for n,u,c in tp]) or "  —"
    r_txt = "\n".join([f"  {'@'+u if u else n}—{c}" for n,u,c in tr]) or "  —"
    await update.message.reply_text(f"СТАТИСТИКА\n\nВсего: {get_total()}\n\nТоп баллы:\n{p_txt}\n\nТоп рефы:\n{r_txt}")

async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    if not context.args:
        await update.message.reply_text("/broadcast текст"); return
    msg = " ".join(context.args); sent = 0
    for uid in get_all_active():
        try:
            await context.bot.send_message(uid, f"ОПОВЕЩЕНИЕ\n\n{msg}")
            sent += 1; await asyncio.sleep(0.05)
        except Exception: mark_inactive(uid)
    await update.message.reply_text(f"Отправлено: {sent}")

async def give_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    if len(context.args) < 2:
        await update.message.reply_text("/give user_id сумма"); return
    try:
        add_pts(int(context.args[0]), int(context.args[1]))
        await update.message.reply_text("Выдано.")
    except Exception as e: await update.message.reply_text(str(e))

async def post_init(app: Application):
    jq = app.job_queue
    jq.run_repeating(j_repost, interval=14400, first=30)
    jq.run_daily(j_remind, time=dtime(hour=11, minute=0))
    jq.run_daily(j_remind, time=dtime(hour=20, minute=0))
    logging.info("Планировщик запущен.")

def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start",     start))
    app.add_handler(CommandHandler("stats",     stats_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast_cmd))
    app.add_handler(CommandHandler("give",      give_cmd))
    app.add_handler(CallbackQueryHandler(cb))
    print("holazc_info OSINT bot v11.0 — online")
    app.run_polling()

if __name__ == "__main__":
    main()
