import telebot
from telebot import types
import os
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
user_data = {}
WAITING_FOR_UNI_SEARCH = set()
UNIVERSITIES = [
{"name": "TU Munich", "country": "Германия", "flag": " ", "field": "Разработка", "cost":
{"name": "TU Berlin", "country": "Германия", "flag": " ", "field": "Разработка", "cost":
{"name": "KIT Karlsruhe", "country": "Германия", "flag": " ", "field": "Разработка", "co
{"name": "Czech Technical University", "country": "Чехия", "flag": " ", "field": "Разраб
{"name": "Budapest Tech BME", "country": "Венгрия", "flag": " ", "field": "Разработка",
{"name": "METU", "country": "Турция", "flag": " ", "field": "Разработка", "cost": "Беспл
{"name": "Tsinghua University", "country": "Китай", "flag": " ", "field": "Разработка",
{"name": "KAIST", "country": "Южная Корея", "flag": " {"name": "MIT", "country": "США", "flag": " ", "field": "Разработка", "cost":
", "field": "Разработка", "cost": "$57000/го
{"name": "University of Cambridge", "country": "Великобритания", "flag": " ", "field": "
{"name": "Warsaw University of Technology", "country": "Польша", "flag": " ", "field": "
{"name": "TU Delft", "country": "Нидерланды", "flag": " ", "field": "Data Science", "cos
{"name": "Eindhoven University", "country": "Нидерланды", "flag": " ", "field": "Data Sc
{"name": "Harbin Institute of Technology", "country": "Китай", "flag": " ", "field": "Da
{"name": "POSTECH", "country": "Южная Корея", "flag": " ", "field": "Data Science", "cos
{"name": "University of Tartu", "country": "Эстония", "flag": " ", "field": "Data Scienc
{"name": "University of Amsterdam", "country": "Нидерланды", "flag": " ", "field": "Data
{"name": "Budapest Tech BME DS", "country": "Венгрия", "flag": " ", "field": "Data Scien
{"name": "Charles University DS", "country": "Чехия", "flag": " ", "field": "Data Scienc
{"name": "Nazarbayev University DS", "country": "Казахстан", "flag": " {"name": "TU Munich AI", "country": "Германия", "flag": " {"name": "Bilkent University", "country": "Турция", "flag": " ", "field": "Data
", "field": "AI / Machine Lear
", "field": "AI / Machine
{"name": "Seoul National University", "country": "Южная Корея", "flag": " ", "field": "A
{"name": "KAIST AI", "country": "Южная Корея", "flag": " ", "field": "AI / Machine Learn
{"name": "Tsinghua University AI", "country": "Китай", "flag": " ", "field": "AI / Machi
{"name": "TU Berlin Security", "country": "Германия", "flag": " ", "field": "Кибербезопа
{"name": "University of Tartu Security", "country": "Эстония", "flag": " ", "field": "Ки
{"name": "Czech Technical University Cyber", "country": "Чехия", "flag": " ", "field": "
{"name": "Budapest Tech BME Cyber", "country": "Венгрия", "flag": " ", "field": "Кибербе
{"name": "KIT Karlsruhe Robotics", "country": "Германия", "flag": " ", "field": "Роботот
{"name": "KAIST Robotics", "country": "Южная Корея", "flag": " ", "field": "Робототехник
{"name": "TU Munich Robotics", "country": "Германия", "flag": " ", "field": "Робототехни
{"name": "MIT Robotics", "country": "США", "flag": " ", "field": "Робототехника", "cost"
{"name": "Heidelberg University", "country": "Германия", "flag": " ", "field": "Физика",
{"name": "LMU Munich", "country": "Германия", "flag": " ", "field": "Физика", "cost": "Б
{"name": "Charles University", "country": "Чехия", "flag": " ", "field": "Физика", "cost
{"name": "Budapest ELTE", "country": "Венгрия", "flag": " ", "field": "Физика", "cost":
{"name": "Peking University", "country": "Китай", "flag": " ", "field": "Физика", "cost"
{"name": "University of Cambridge", "country": "Великобритания", "flag": " {"name": "MIT", "country": "США", "flag": " ", "field": "
", "field": "Физика", "cost": "$57000/год",
{"name": "University of Vienna", "country": "Австрия", "flag": " ", "field": "Химия", "c
{"name": "Masaryk University", "country": "Чехия", "flag": " ", "field": "Химия", "cost"
{"name": "Koç University", "country": "Турция", "flag": " ", "field": "Химия", "cost": "
{"name": "Charles University Chemistry", "country": "Чехия", "flag": " ", "field": "Хими
{"name": "Budapest ELTE Chemistry", "country": "Венгрия", "flag": " ", "field": "Химия",
{"name": "University of Belgrade", "country": "Сербия", "flag": " ", "field": "Биология"
{"name": "University of Debrecen", "country": "Венгрия", "flag": " ", "field": "Биология
{"name": "Tbilisi State University", "country": "Грузия", "flag": " ", "field": "Биологи
{"name": "Charles University Biology", "country": "Чехия", "flag": " ", "field": "Биолог
{"name": "Peking University Biology", "country": "Китай", "flag": " ", "field": "Биологи
{"name": "University of Buenos Aires", "country": "Аргентина", "flag": " ", "field": "Эк
{"name": "University of Wroclaw", "country": "Польша", "flag": " ", "field": "Экология",
{"name": "Charles University Ecology", "country": "Чехия", "flag": " ", "field": "Эколог
{"name": "University of Vienna Ecology", "country": "Австрия", "flag": " ", "field": "Эк
{"name": "Tbilisi State University Ecology", "country": "Грузия", "flag": " ", "field":
{"name": "Budapest ELTE Math", "country": "Венгрия", "flag": " ", "field": "Математика",
{"name": "Charles University Math", "country": "Чехия", "flag": " {"name": "MIT", "country": "США", "flag": " ", "field": "Математик
", "field": "Математика", "cost": "$57000/го
{"name": "University of Vienna Math", "country": "Австрия", "flag": " ", "field": "Матем
{"name": "University of Cambridge", "country": "Великобритания", "flag": " ", "field": "
{"name": "Budapest ELTE Astronomy", "country": "Венгрия", "flag": " ", "field": "Астроно
{"name": "Charles University Astronomy", "country": "Чехия", "flag": " ", "field": "Астр
{"name": "Ankara University Astronomy", "country": "Турция", "flag": " ", "field": "Астр
{"name": "Peking University Astronomy", "country": "Китай", "flag": " ", "field": "Астро
{"name": "Seoul National University Astronomy", "country": "Южная Корея", "flag": " ", "
{"name": "University of Vienna Astronomy", "country": "Австрия", "flag": " ", "field": "
{"name": "Corvinus University", "country": "Венгрия", "flag": " ", "field": "Менеджмент"
{"name": "Prague University of Economics", "country": "Чехия", "flag": " ", "field": "Ме
{"name": "Nazarbayev University", "country": "Казахстан", "flag": " ", "field": "Менеджм
{"name": "Tbilisi Free University", "country": "Грузия", "flag": " ", "field": "Менеджме
{"name": "University of Belgrade Management", "country": "Сербия", "flag": " ", "field":
{"name": "IE University", "country": "Испания", "flag": " ", "field": "Финансы", "cost":
{"name": "Tbilisi Free University Finance", "country": "Грузия", "flag": " ", "field": "
{"name": "Corvinus University Finance", "country": "Венгрия", "flag": " ", "field": "Фин
{"name": "Prague University of Economics Finance", "country": "Чехия", "flag": " ", "fie
{"name": "American University of Armenia", "country": "Армения", "flag": " ", "field": "
{"name": "Corvinus University Marketing", "country": "Венгрия", "flag": " ", "field": "М
{"name": "Bilkent University Marketing", "country": "Турция", "flag": " ", "field": "Мар
{"name": "Tbilisi State University Marketing", "country": "Грузия", "flag": " ", "field"
{"name": "Koç University Business", "country": "Турция", "flag": " ", "field": "Предприн
{"name": "Nazarbayev University Entrepreneurship", "country": "Казахстан", "flag": " ",
{"name": "Budapest Metropolitan University Entrepreneurship", "country": "Венгрия", "flag
{"name": "Heriot-Watt Dubai", "country": "ОАЭ", "flag": " ", "field": "Логистика", "cost
{"name": "Koç University Logistics", "country": "Турция", "flag": " ", "field": "Логисти
{"name": "Corvinus University Logistics", "country": "Венгрия", "flag": " ", "field": "Л
{"name": "Warsaw University Logistics", "country": "Польша", "flag": " ", "field": "Логи
{"name": "Charles University Medicine", "country": "Чехия", "flag": " ", "field": "Общая
{"name": "Semmelweis University", "country": "Венгрия", "flag": " ", "field": "Общая мед
{"name": "Tbilisi State Medical University", "country": "Грузия", "flag": " ", "field":
{"name": "Ankara University Medicine", "country": "Турция", "flag": " ", "field": "Общая
{"name": "Yerevan State Medical University", "country": "Армения", "flag": " ", "field":
{"name": "University of Debrecen Medicine", "country": "Венгрия", "flag": " ", "field":
{"name": "Poznan University of Medicine", "country": "Польша", "flag": " ", "field": "Ст
{"name": "Tbilisi State Medical University Dentistry", "country": "Грузия", "flag": " ",
{"name": "Semmelweis University Dentistry", "country": "Венгрия", "flag": " ", "field":
{"name": "Masaryk University Pharmacy", "country": "Чехия", "flag": " ", "field": "Фарма
{"name": "Charles University Pharmacy", "country": "Чехия", "flag": " ", "field": "Фарма
{"name": "University of Belgrade Pharmacy", "country": "Сербия", "flag": " ", "field": "
{"name": "Ankara University Pharmacy", "country": "Турция", "flag": " ", "field": "Фарма
{"name": "University of Vienna Psychology", "country": "Австрия", "flag": " ", "field":
{"name": "Budapest ELTE Psychology", "country": "Венгрия", "flag": " ", "field": "Психол
{"name": "Charles University Psychology", "country": "Чехия", "flag": " ", "field": "Пси
{"name": "University of Belgrade Psychology", "country": "Сербия", "flag": " ", "field":
{"name": "University of Cambridge", "country": "Великобритания", "flag": " ", "field": "
{"name": "University of Belgrade Vet", "country": "Сербия", "flag": " ", "field": "Ветер
{"name": "Budapest University of Veterinary Medicine", "country": "Венгрия", "flag": " "
{"name": "Ankara University Veterinary", "country": "Турция", "flag": " ", "field": "Вет
{"name": "Tbilisi State University Vet", "country": "Грузия", "flag": " ", "field": "Вет
{"name": "Aalto University", "country": "Финляндия", "flag": " ", "field": "Графический
{"name": "Yildiz Technical University", "country": "Турция", "flag": " ", "field": "Граф
{"name": "Prague College", "country": "Чехия", "flag": " ", "field": "Графический дизайн
{"name": "Budapest Metropolitan University", "country": "Венгрия", "flag": " ", "field":
{"name": "Seoul National University Design", "country": "Южная Корея", "flag": " ", "fie
{"name": "Tsinghua University Design", "country": "Китай", "flag": " {"name": "Design Academy Eindhoven", "country": "Нидерланды", "flag": " {"name": "Czech Technical University UX", "country": "Чехия", "flag": " ", "field": "Графич
", "field": "UX/
", "field": "UX/
{"name": "Budapest Metropolitan University UX", "country": "Венгрия", "flag": " ", "fiel
{"name": "KAIST Design", "country": "Южная Корея", "flag": " ", "field": "UX/UI", "cost"
{"name": "Aalto University UX", "country": "Финляндия", "flag": " ", "field": "UX/UI", "
{"name": "TU Delft Architecture", "country": "Нидерланды", "flag": " ", "field": "Архите
{"name": "Academy of Fine Arts Vienna", "country": "Австрия", "flag": " ", "field": "Арх
{"name": "TU Vienna Architecture", "country": "Австрия", "flag": " ", "field": "Архитект
{"name": "Charles University Architecture", "country": "Чехия", "flag": " ", "field": "А
{"name": "Budapest University of Technology", "country": "Венгрия", "flag": " ", "field"
{"name": "Istanbul Technical University", "country": "Турция", "flag": " {"name": "MIT", "country": "США", "flag": " ", "field": "Ар
", "field": "Архитектура", "cost": "$57000/г
{"name": "University of Cambridge", "country": "Великобритания", "flag": " ", "field": "
{"name": "Tbilisi Academy of Arts", "country": "Грузия", "flag": " ", "field": "Мода", "
{"name": "Prague College Fashion", "country": "Чехия", "flag": " ", "field": "Мода", "co
{"name": "Budapest Metropolitan University Fashion", "country": "Венгрия", "flag": " ",
{"name": "Yildiz Technical University Fashion", "country": "Турция", "flag": " ", "field
{"name": "Tsinghua University Fashion", "country": "Китай", "flag": " ", "field": "Мода"
{"name": "Mimar Sinan Fine Arts University Fashion", "country": "Турция", "flag": " ", "
{"name": "Bezalel Academy", "country": "Израиль", "flag": " ", "field": "Анимация", "cos
{"name": "Prague College Animation", "country": "Чехия", "flag": " ", "field": "Анимация
{"name": "Budapest Metropolitan University Animation", "country": "Венгрия", "flag": " "
{"name": "KAIST Animation", "country": "Южная Корея", "flag": " ", "field": "Анимация",
{"name": "Tsinghua University Animation", "country": "Китай", "flag": " ", "field": "Ани
{"name": "Mimar Sinan Fine Arts University Animation", "country": "Турция", "flag": " ",
{"name": "Prague College Photography", "country": "Чехия", "flag": " ", "field": "Фотогр
{"name": "Budapest Metropolitan University Photography", "country": "Венгрия", "flag": "
{"name": "Tbilisi State Academy of Arts Photography", "country": "Грузия", "flag": " ",
{"name": "Seoul National University Photography", "country": "Южная Корея", "flag": " ",
{"name": "Mimar Sinan Fine Arts University Photography", "country": "Турция", "flag": "
{"name": "Charles University Journalism", "country": "Чехия", "flag": " ", "field": "Жур
{"name": "University of Belgrade Journalism", "country": "Сербия", "flag": " ", "field":
{"name": "Corvinus University Journalism", "country": "Венгрия", "flag": " ", "field": "
{"name": "Bilkent University Journalism", "country": "Турция", "flag": " ", "field": "Жу
{"name": "Tbilisi State University Journalism", "country": "Грузия", "flag": " ", "field
{"name": "Tbilisi State University IR", "country": "Грузия", "flag": " ", "field": "Дипл
{"name": "Corvinus University Diplomacy", "country": "Венгрия", "flag": " ", "field": "Д
{"name": "Charles University IR", "country": "Чехия", "flag": " ", "field": "Дипломатия"
{"name": "University of Vienna IR", "country": "Австрия", "flag": " ", "field": "Диплома
{"name": "Columbia University Diplomacy", "country": "США", "flag": " ", "field": "Дипло
{"name": "Peking University IR", "country": "Китай", "flag": " ", "field": "Дипломатия",
{"name": "Bilkent University IR", "country": "Турция", "flag": " ", "field": "Дипломатия
{"name": "University of Vienna Politics", "country": "Австрия", "flag": " ", "field": "П
{"name": "Budapest ELTE Politics", "country": "Венгрия", "flag": " ", "field": "Политоло
{"name": "University of Cambridge", "country": "Великобритания", "flag": " ", "field": "
{"name": "Charles University Politics", "country": "Чехия", "flag": " ", "field": "Полит
{"name": "Bilkent University Politics", "country": "Турция", "flag": " ", "field": "Поли
{"name": "Prague University Sociology", "country": "Чехия", "flag": " ", "field": "Социо
{"name": "University of Vienna Sociology", "country": "Австрия", "flag": " ", "field": "
{"name": "Budapest ELTE Sociology", "country": "Венгрия", "flag": " ", "field": "Социоло
{"name": "University of Belgrade Sociology", "country": "Сербия", "flag": " ", "field":
{"name": "Tbilisi State University Sociology", "country": "Грузия", "flag": " ", "field"
{"name": "Corvinus University IR", "country": "Венгрия", "flag": " ", "field": "Междунар
{"name": "Budapest ELTE IR", "country": "Венгрия", "flag": " ", "field": "Международные
{"name": "Charles University MO", "country": "Чехия", "flag": " ", "field": "Международн
{"name": "University of Vienna MO", "country": "Австрия", "flag": " ", "field": "Междуна
{"name": "Columbia University", "country": "США", "flag": " ", "field": "Международные о
{"name": "Seoul National University IR", "country": "Южная Корея", "flag": " ", "field":
{"name": "Peking University MO", "country": "Китай", "flag": " ", "field": "Международны
{"name": "University of Cambridge", "country": "Великобритания", "flag": " ", "field": "
{"name": "American University of Armenia Law", "country": "Армения", "flag": " ", "field
{"name": "University of Belgrade Law", "country": "Сербия", "flag": " ", "field": "Право
{"name": "University of Cambridge", "country": "Великобритания", "flag": " ", "field": "
{"name": "Charles University Law", "country": "Чехия", "flag": " ", "field": "Право", "c
{"name": "Corvinus University Law", "country": "Венгрия", "flag": " ", "field": "Право",
{"name": "University of Vienna History", "country": "Австрия", "flag": " ", "field": "Ис
{"name": "University of Cambridge", "country": "Великобритания", "flag": " ", "field": "
{"name": "Charles University History", "country": "Чехия", "flag": " ", "field": "Истори
{"name": "Budapest ELTE History", "country": "Венгрия", "flag": " ", "field": "История",
{"name": "University of Belgrade History", "country": "Сербия", "flag": " ", "field": "И
{"name": "Charles University Philosophy", "country": "Чехия", "flag": " ", "field": "Фил
{"name": "University of Cambridge", "country": "Великобритания", "flag": " ", "field": "
{"name": "University of Vienna Philosophy", "country": "Австрия", "flag": " ", "field":
{"name": "Budapest ELTE Philosophy", "country": "Венгрия", "flag": " ", "field": "Филосо
{"name": "University of Belgrade Philosophy", "country": "Сербия", "flag": " ", "field":
{"name": "Budapest ELTE Linguistics", "country": "Венгрия", "flag": " ", "field": "Лингв
{"name": "University of Cambridge", "country": "Великобритания", "flag": " ", "field": "
{"name": "Charles University Linguistics", "country": "Чехия", "flag": " ", "field": "Ли
{"name": "University of Vienna Linguistics", "country": "Австрия", "flag": " ", "field":
{"name": "Tbilisi State University Culture", "country": "Грузия", "flag": " ", "field":
{"name": "Charles University Cultural Studies", "country": "Чехия", "flag": " ", "field"
{"name": "University of Vienna Cultural Studies", "country": "Австрия", "flag": " ", "fi
{"name": "Budapest ELTE Cultural Studies", "country": "Венгрия", "flag": " ", "field": "
{"name": "Charles University Anthropology", "country": "Чехия", "flag": " ", "field": "А
{"name": "University of Vienna Anthropology", "country": "Австрия", "flag": " ", "field"
{"name": "Budapest ELTE Anthropology", "country": "Венгрия", "flag": " ", "field": "Антр
{"name": "University of Belgrade Anthropology", "country": "Сербия", "flag": " ", "field
{"name": "Peking University Anthropology", "country": "Китай", "flag": " ", "field": "Ан
{"name": "TU Munich Engineering", "country": "Германия", "flag": " ", "field": "Машиност
{"name": "KIT Karlsruhe Engineering", "country": "Германия", "flag": " {"name": "MIT", "country": "США", "flag": " ", "field": "Машиностроение", "cost": ", "field": "Маши
"$5700
{"name": "Budapest Tech BME Engineering", "country": "Венгрия", "flag": " ", "field": "М
{"name": "Czech Technical University Engineering", "country": "Чехия", "flag": " ", "fie
{"name": "Budapest Tech Electrical", "country": "Венгрия", "flag": " ", "field": "Электр
{"name": "TU Munich Electrical", "country": "Германия", "flag": " ", "field": "Электрони
{"name": "KIT Karlsruhe Electrical", "country": "Германия", "flag": " ", "field": "Элект
{"name": "Eindhoven University Electrical", "country": "Нидерланды", "flag": " ", "field
{"name": "METU Electrical", "country": "Турция", "flag": " ", "field": "Электроника", "c
{"name": "Czech Technical University Civil", "country": "Чехия", "flag": " ", "field": "
{"name": "TU Munich Civil", "country": "Германия", "flag": " ", "field": "Строительство"
{"name": "Budapest Tech BME Civil", "country": "Венгрия", "flag": " ", "field": "Строите
{"name": "Warsaw University of Technology Civil", "country": "Польша", "flag": " ", "fie
{"name": "University of Belgrade Engineering Energy", "country": "Сербия", "flag": " ",
{"name": "TU Munich Energy", "country": "Германия", "flag": " ", "field": "Энергетика",
{"name": "KIT Karlsruhe Energy", "country": "Германия", "flag": " ", "field": "Энергетик
{"name": "Eindhoven University Energy", "country": "Нидерланды", "flag": " ", "field": "
{"name": "Budapest Tech BME Energy", "country": "Венгрия", "flag": " ", "field": "Энерге
{"name": "TU Delft Aerospace", "country": "Нидерланды", "flag": " {"name": "MIT", "country": "США", "flag": " ", "field": "Авиация",
", "field": "Авиация", "cost": "$57000/год",
{"name": "TU Munich Aerospace", "country": "Германия", "flag": " ", "field": "Авиация",
{"name": "KIT Karlsruhe Aerospace", "country": "Германия", "flag": " ", "field": "Авиаци
{"name": "Budapest Tech BME Aerospace", "country": "Венгрия", "flag": " ", "field": "Ави
{"name": "University of Vienna Education", "country": "Австрия", "flag": " ", "field": "
{"name": "Budapest ELTE Education", "country": "Венгрия", "flag": " ", "field": "Педагог
{"name": "Ankara University Education", "country": "Турция", "flag": " ", "field": "Педа
{"name": "Nazarbayev University Education", "country": "Казахстан", "flag": " ", "field"
{"name": "Peking University Education", "country": "Китай", "flag": " ", "field": "Педаг
{"name": "University of Belgrade Education", "country": "Сербия", "flag": " ", "field":
{"name": "Tbilisi State University Education", "country": "Грузия", "flag": " ", "field"
{"name": "University of Cambridge", "country": "Великобритания", "flag": " ", "field": "
{"name": "Charles University Education", "country": "Чехия", "flag": " ", "field": "Псих
{"name": "University of Vienna Educational Psychology", "country": "Австрия", "flag": "
{"name": "Budapest ELTE Educational Psychology", "country": "Венгрия", "flag": " ", "fie
{"name": "Nazarbayev University Educational Psychology", "country": "Казахстан", "flag":
{"name": "Charles University Special Education", "country": "Чехия", "flag": " ", "field
{"name": "University of Vienna Special Education", "country": "Австрия", "flag": " ", "f
{"name": "Budapest ELTE Special Education", "country": "Венгрия", "flag": " ", "field":
{"name": "University of Belgrade Special Education", "country": "Сербия", "flag": " ", "
]
import telebot
from telebot import types
import os
import json
import datetime
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
user_data = {}
WAITING_FOR_UNI_SEARCH = set()
try:
import gspread
from google.oauth2.service_account import Credentials
SHEETS_AVAILABLE = True
except ImportError:
SHEETS_AVAILABLE = False
def get_sheets_client():
if not SHEETS_AVAILABLE:
return None
try:
creds_json = os.environ.get('GOOGLE_SHEETS_CREDS')
if not creds_json:
return None
creds_dict = json.loads(creds_json)
scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/d
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
return gspread.authorize(creds)
except Exception as e:
print(f"Sheets error: {e}")
return None
def log_to_sheets(chat_id, name="", citizenship="", field="", completed=False):
try:
client = get_sheets_client()
if not client:
return
sheet_id = os.environ.get('GOOGLE_SHEET_ID')
if not sheet_id:
return
sheet = client.open_by_key(sheet_id).sheet1
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
sheet.append_row([now, str(chat_id), name, citizenship, field, "да" if completed else
except Exception as e:
print(f"Sheets log error: {e}")
STATS = {
"total_users": set(),
"completed": 0,
"citizenships": {},
"fields": {},
"started_today": set(),
"today": datetime.date.today().isoformat(),
}
def update_stats(chat_id, citizenship="", field="", completed=False):
today = datetime.date.today().isoformat()
if STATS["today"] != today:
STATS["today"] = today
STATS["started_today"] = set()
STATS["total_users"].add(chat_id)
STATS["started_today"].add(chat_id)
if citizenship:
STATS["citizenships"][citizenship] = STATS["citizenships"].get(citizenship, 0) if field:
STATS["fields"][field] = STATS["fields"].get(field, 0) + 1
if completed:
STATS["completed"] += 1
+ 1
def normalize(text):
if not text:
return ""
return " ".join(text.split()).strip().lower()
def clean_field(text):
if not text:
return text
text = text.strip()
parts = text.split(" ", 1)
if len(parts) > 1 and len(parts[0]) >= 1 and ord(parts[0][0]) > 127:
return parts[1].strip()
return text
def analyze_achievements(text):
t = text.lower()
results = []
if any(w in t for w in ["олимпиад"]):
if any(w in t for w in ["международн", "international"]):
results.append(" *Международная олимпиада* — сильное достижение! Повышает шансы
else:
results.append(" *Олимпиада* — хорошее достижение. Упомяни в мотивационном пись
if any(w in t for w in ["волонтёр", "волонтер", "volunteer"]):
results.append(" *Волонтёрство* — плюс для социальных наук и дипломатии")
if any(w in t for w in ["хакатон", "hackathon"]):
results.append(" *Хакатон* — отличное tech-достижение!")
if any(w in t for w in ["публикац", "статья", "научн", "research"]):
results.append(" *Научная работа* — очень ценно для PhD")
if any(w in t for w in ["стартап", "startup", "бизнес", "основал"]):
results.append(" *Предпринимательский опыт* — выделит в бизнес-школах")
if any(w in t for w in ["проект", "разработ", "создал"]):
results.append(" *Проект/разработка* — практический опыт ценится в IT")
if any(w in t for w in ["работ", "стажировк", "intern"]):
results.append(" *Опыт работы/стажировка* — особенно ценится в магистратуре")
if not results:
results.append(" Упомяни все достижения в мотивационном письме — любой опыт важен!"
return results
def get_time_to_enroll(data):
g = data.get("age_or_grade", "")
s = data.get("status", "")
if "8 класс" in g: return "lots", "4+ года"
if "9 класс" in g: return "lots", "3+ года"
if "10 класс" in g: return "medium", "2 года"
if "11 класс" in g: return "urgent", "1 год"
if "Студент" in s: return "medium", "1-3 года"
if "Выпускник" in s or "Работаю" in s: return "urgent", "Сейчас"
return "medium", "1-2 года"
def get_admission_plan(uni, data):
country = uni.get("country", "")
citizenship = data.get("citizenship", "")
certificate = data.get("certificate", "")
other_language = data.get("other_language", "")
scholarship = uni.get("scholarship", "")
is_rf = "Россия" in citizenship
time_type, _ = get_time_to_enroll(data)
plan = f" *План поступления в {uni['name']}*\n\n"
if time_type == "lots":
plan += "У тебя много времени — готовься основательно! \n\n*Прямо сейчас:*\n"
plan += "☐ Начни учить английский — цель IELTS 6.5+\n"
if country in ["Германия", "Австрия"] and "Немецкий" not in other_language:
plan += "☐ Начни учить немецкий — откроет бесплатное обучение\n"
plan += "☐ Участвуй в олимпиадах\n\n*За 2 года:*\n"
plan += "☐ Сдай IELTS\n"
if scholarship and "Нет" not in scholarship:
plan += f"☐ Изучи условия стипендии {scholarship}\n"
plan += "\n*За 1 год:*\n"
elif time_type == "medium":
plan += "Времени достаточно! \n\n*Прямо сейчас:*\n"
if "Нет" in certificate or "Планирую" in certificate:
plan += "☐ Запишись на IELTS\n"
plan += "☐ Оформи загранпаспорт если нет\n\n*За 6 месяцев:*\n"
else:
plan += "Действуй быстро! \n\n*Срочно:*\n"
if "Нет" in certificate or "Планирую" in certificate:
plan += "☐ СРОЧНО запишись на IELTS!\n"
plan += "\n*В ближайшие месяцы:*\n"
country_plans = {
"Германия": "☐ Нострификация аттестата\n☐ Мотивационное письмо\n☐ 2 рекомендательных
"Венгрия": "☐ Мотивационное письмо\n☐ Аттестат + апостиль\n" + ("☐ Stipendium Hungari
"Чехия": "☐ Нострификация аттестата\n☐ Мотивационное письмо\n\n*После зачисления:*\n☐
"Сербия": "☐ Перевод аттестата на сербский\n☐ Справка об отсутствии судимости\n" + ("
"Грузия": "☐ Перевод аттестата\n☐ Мотивационное письмо\n" + ("\n *Виза не нужна для
"Турция": "☐ Аттестат + апостиль\n☐ Мотивационное письмо\n" + ("☐ Türkiye Scholarship
"Китай": "☐ Аттестат + апостиль\n☐ Медицинская справка\n☐ Мотивационное письмо\n" + (
"Южная Корея": "☐ Аттестат + апостиль\n☐ Мотивационное письмо\n" + ("☐ GKS стипендия
"Нидерланды": "☐ Аттестат + апостиль\n☐ Мотивационное письмо\n☐ Подача через Studieli
"Великобритания": "☐ Аттестат + апостиль\n☐ Personal Statement\n☐ 2 рекомендательных
"США": "☐ SAT/GRE если нужно\n☐ Personal Statement\n☐ 3 рекомендательных письма\n\n*П
}
plan += country_plans.get(country, "☐ Уточни требования на сайте\n☐ Аттестат + апостиль\n
plan += f"\n _Дедлайн: {uni['deadline']}_\n\n Сохрани этот план!"
return plan
EMPLOYMENT_BY_COUNTRY = {
"Германия": {"score": " "Нидерланды": {"score": " "Чехия": {"score": " "Венгрия": {"score": " "Австрия": {"score": " "Сербия": {"score": " "Грузия": {"score": " "Турция": {"score": " "Китай": {"score": " "Южная Корея": {"score": " "США": {"score": " "Великобритания": {"score": " "Польша": {"score": " "Финляндия": {"score": " "Эстония": {"score": " "Казахстан": {"score": " "Армения": {"score": " "ОАЭ": {"score": " "Израиль": {"score": " "Испания": {"score": " ", "visa": "Blue Card — лёгкий путь к ПМЖ", "salary": "
", "visa": "Orientation Year Visa — 1 год", "salary":
", "visa": "Рабочая виза ЕС", "salary": "€20,000–35,000/год"
", "visa": "Рабочая виза ЕС", "salary": "€15,000–25,000/год"
", "visa": "Красно-бело-красная карта", "salary": "€35,0
", "visa": "Рабочая виза (не ЕС)", "salary": "€10,000–20,000/
", "visa": "Без визы для РФ", "salary": "€8,000–15,000/год",
", "visa": "Рабочий ВНЖ", "salary": "€12,000–25,000/год", "
", "visa": "Рабочая виза Z", "salary": "€15,000–40,000/год",
", "visa": "D-10 после учёбы", "salary": "€20,000–45,0
", "visa": "OPT — 1-3 года после учёбы", "salary": "$60,000–
", "visa": "Graduate Route — 2 года", "salary": "
", "visa": "Рабочая виза ЕС", "salary": "€15,000–25,000/год",
", "visa": "Job-seeker visa — 1 год", "salary": "€30,000
", "visa": "Job-seeker visa", "salary": "€20,000–40,000/го
", "visa": "Не нужна для СНГ", "salary": "€10,000–20,000/г
", "visa": "Без визы для РФ", "salary": "€8,000–18,000/год",
", "visa": "Рабочая виза", "salary": "$40,000–100,000/год (б
", "visa": "Рабочая виза", "salary": "$30,000–80,000/год",
", "visa": "EU Blue Card", "salary": "€20,000–40,000/год",
}
def get_match_reasons(uni, data):
reasons = []
country = uni.get("country", "")
other_language = data.get("other_language", "")
hobbies = data.get("hobbies", "")
career = data.get("career", "")
goal = data.get("goal", "")
priority = data.get("priority", "")
achievements = data.get("achievements", "")
scholarship = uni.get("scholarship", "Нет")
community = uni.get("community", "")
if "Немецкий" in other_language and country in ["Германия", "Австрия"]:
reasons.append(" Знаешь немецкий — можешь учиться бесплатно")
if "Турецкий" in other_language and country == "Турция":
reasons.append(" Знаешь турецкий — больше программ")
if "Китайский" in other_language and country == "Китай":
reasons.append(" Знаешь китайский — доступны все программы")
if "Корейский" in other_language and country == "Южная Корея":
reasons.append(" Знаешь корейский — доступны все программы")
if "Технологии" in hobbies and country in ["Германия", "Нидерланды", "Южная Корея"]:
reasons.append(" Страна с сильной tech-индустрией")
if "Искусство" in hobbies and country in ["Австрия", "Чехия", "Грузия"]:
reasons.append(" Богатая культурная среда")
if ("IT" in career or "Стартап" in career) and country in ["Германия", "Нидерланды", "Эст
reasons.append(" Один из лучших рынков для IT-карьеры")
if "Наука" in career and country in ["Германия", "Великобритания", "США"]:
reasons.append(" Мировой центр научных исследований")
if "Остаться" in goal and country in ["Германия", "Нидерланды", "Эстония"]:
reasons.append(" Хорошие возможности для эмиграции")
if "Вернуться" in goal and country in ["Сербия", "Грузия", "Армения"]:
reasons.append(" Близко к дому")
if scholarship and "Нет" not in scholarship and ("Международные" in achievements or "Наци
reasons.append(f" Твои достижения повышают шансы на {scholarship}")
if "Стоимость" in priority and uni.get("cost") == "Бесплатно":
reasons.append(" Бесплатное обучение")
if "Безопасность" in priority and country in ["Германия", "Австрия", "Нидерланды"]:
reasons.append(" Одна из самых безопасных стран")
if "Большое СНГ" in community or "Активное СНГ" in community:
reasons.append(" Большое СНГ-комьюнити")
if country in ["Сербия", "Грузия"] and "Россия" in data.get("citizenship", ""):
reasons.append(" Виза не нужна")
return reasons
def score_university(uni, data):
score = 0
hobbies = data.get("hobbies", "")
personality = data.get("personality", "")
career = data.get("career", "")
goal = data.get("goal", "")
other_language = data.get("other_language", "")
achievements = data.get("achievements", "")
priority = data.get("priority", "")
country = uni.get("country", "")
community = uni.get("community", "")
scholarship = uni.get("scholarship", "Нет")
if "Немецкий" in other_language and country in ["Германия", "Австрия"]: score += 3
if "Турецкий" in other_language and country == "Турция": score += 3
if "Китайский" in other_language and country == "Китай": score += 3
if "Корейский" in other_language and country == "Южная Корея": score += 3
if "Сербский" in other_language and country == "Сербия": score += 3
if "Чешский" in other_language and country == "Чехия": score += 3
if "Венгерский" in other_language and country == "Венгрия": score += 3
if "Технологии" in hobbies and country in ["Германия", "Нидерланды", "Южная Корея"]: scor
if "Искусство" in hobbies and country in ["Австрия", "Чехия", "Грузия"]: score += 2
if "Бизнес" in hobbies and country in ["ОАЭ", "Турция", "США"]: score += 2
if "Волонтёрство" in hobbies and country in ["Германия", "Нидерланды", "Австрия"]: score
if ("IT" in career or "Стартап" in career) and country in ["Германия", "Нидерланды", "Эст
if "Наука" in career and country in ["Германия", "Великобритания", "США", "Китай"]: score
if "Своё дело" in career and country in ["ОАЭ", "Турция", "Эстония"]: score += 2
if "Корпорация" in career and country in ["Германия", "США", "Великобритания"]: score +=
if "Социальные" in career and country in ["Германия", "Нидерланды", "Австрия"]: score +=
if "Остаться" in goal and country in ["Германия", "Нидерланды", "Эстония"]: score += 2
if "Вернуться" in goal and country in ["Сербия", "Грузия", "Армения", "Казахстан"]: score
if "Международные" in achievements and scholarship != "Нет": score += 3
if "Национальные" in achievements and scholarship != "Нет": score += 2
if "Интроверт" in personality and country in ["Германия", "Чехия", "Венгрия"]: score += 1
if "Экстраверт" in personality and country in ["Турция", "ОАЭ", "США"]: score += 1
if "Рейтинг" in priority and country in ["США", "Великобритания", "Германия"]: score += 2
if "Стоимость" in priority and uni.get("cost") == "Бесплатно": score += 3
if "Безопасность" in priority and country in ["Германия", "Австрия", "Нидерланды", if "Трудоустройство" in priority and country in ["Германия", "США", "Нидерланды"]: if "Большое СНГ" in community or "Активное СНГ" in community: score += 1
return score
"Чехия
score
FIELDS = {
" IT и технологии": ["Разработка", "Data Science", "AI / Machine Learning", "Кибербезоп
" Естественные науки": ["Физика", "Химия", "Биология", "Экология", "Математика", "Астро
" Бизнес и экономика": ["Менеджмент", "Финансы", "Маркетинг", "Предпринимательство", "Л
"⚕ Медицина и здоровье": ["Общая медицина", "Стоматология", "Фармацевтика", "Психология"
" Дизайн и искусство": ["Графический дизайн", "UX/UI", "Архитектура", "Мода", "Анимация
" Социальные науки": ["Журналистика", "Дипломатия", "Политология", "Социология", "Между
" Гуманитарные": ["История", "Философия", "Лингвистика", "Культурология", "Антропология
" Инженерия": ["Машиностроение", "Электроника", "Строительство", "Энергетика", "Авиация
" Образование": ["Педагогика", "Психология образования", "Специальное образование"],
}
SUBFIELDS = {
"Разработка": [" Мобильная разработка", " Веб-разработка", " Gamedev", " Облачны
"Data Science": [" Анализ данных", " Машинное обучение", " Бизнес-аналитика", "
"AI / Machine Learning": [" Нейросети", " Компьютерное зрение", " Обработка языка"
"Кибербезопасность": [" Защита сетей", " Криптография", " Этичный хакинг", " Без
"Робототехника": [" Промышленные роботы", " Автономные системы", " Медицинская роб
"Физика": [" Ядерная физика", " Астрофизика", " Оптика и фотоника", " Физика мат
"Химия": [" Фармацевтическая химия", " Органическая химия", " Аналитическая химия"
"Биология": [" Молекулярная биология", " Экология", " Микробиология", " Биотехно
"Экология": [" Охрана окружающей среды", " Устойчивое развитие", " Морская экологи
"Математика": [" Чистая математика", " Вычислительная математика", " Статистика",
"Астрономия": [" Астрофизика", " Наблюдательная астрономия", " Планетология", "
"Менеджмент": [" Международный менеджмент", " Управление проектами", " Корпоративн
"Финансы": [" Инвестиции и рынки", " Банковское дело", " Корпоративные финансы", "
"Маркетинг": [" Digital-маркетинг", " Бренд-менеджмент", " Аналитика и данные"],
"Предпринимательство": [" Стартапы", " Инновации", " Социальное предпринимательств
"Логистика": [" Международная логистика", " Управление цепочками поставок", " "Общая медицина": [" Научная / исследовательская", " Клиническая практика", " Авиал
Глоб
"Стоматология": [" Общая стоматология", " Хирургическая стоматология", " Детская с
"Фармацевтика": [" Клиническая фармация", " Фармацевтические исследования", " Промы
"Психология": [" Клиническая психология", " Организационная психология", " Нейропси
"Ветеринария": [" Мелкие животные", " Крупные животные", " Ветеринарные исследовани
"Графический дизайн": [" Визуальная коммуникация", " Брендинг и упаковка", " Моушн
"UX/UI": [" Мобильный дизайн", " Веб-дизайн", " UX-исследования", " Игровой инте
"Архитектура": [" Современная и городская среда", " Историческая и реставрация", "
"Мода": [" Дизайн одежды", " Устойчивая мода", " Управление модным брендом"],
"Анимация": [" 2D анимация", " 3D и геймдев", " Стоп-моушн", " Спецэффекты"],
"Фотография": [" Документальная", " Художественная", " Фотожурналистика", " Комм
"Журналистика": [" Печатная журналистика", " ТВ и видео", " Digital-медиа", " Ра
"Дипломатия": [" Международные отношения", " Переговоры и медиация", " Публичная ди
"Политология": [" Сравнительная политика", " Международная политика", " Политически
"Социология": [" Социальные исследования", " Городская социология", " Количественны
"Международные отношения": [" Глобальная политика", " Международная торговля", " Ми
"Право": [" Международное право", " Корпоративное право", " Права человека", " У
"История": [" Древняя история", " Современная история", " Архивное дело"],
"Философия": [" Аналитическая философия", " Политическая философия", " Этика"],
"Лингвистика": [" Прикладная лингвистика", " Компьютерная лингвистика", " Социолин
"Культурология": [" Культура и медиа", " Межкультурная коммуникация", " Культурное
"Антропология": [" Культурная антропология", " Физическая антропология", " Археоло
"Машиностроение": [" Автомобильная инженерия", " Аэрокосмическая", " Промышленная"
"Электроника": [" Силовая электроника", " Телекоммуникации", " Встраиваемые системы
"Строительство": [" Гражданское строительство", " Мосты и конструкции", " Зелёное
"Энергетика": [" Возобновляемая энергия", " Энергосистемы", " Ветроэнергетика"],
"Авиация": [" Аэронавтика", " Космические системы", " Беспилотники"],
"Педагогика": [" Дошкольное образование", " Школьное образование", " Международное
"Психология образования": [" Когнитивное развитие", " Образовательные исследования"],
"Специальное образование": [" Инклюзивное образование", " Работа с особыми потребност
}
SKIP_TEXTS = [
" Подобрать университеты", " Подобрать заново", " Чеклист документов",
" Быстрый поиск", " Сменить специальность", " Сменить направление",
" Расширить бюджет", " Начать заново", " В главное меню",
" Сравнить с другим", " Очистить сравнение", " Чат для поступающих",
]
def main_menu_markup():
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Подобрать университеты")
markup.add(" Быстрый поиск")
markup.add(" Чеклист документов")
markup.add(" Чат для поступающих")
return markup
@bot.message_handler(commands=["start"])
def start(message):
bot.clear_step_handler_by_chat_id(message.chat.id)
user_data[message.chat.id] = {}
WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
update_stats(message.chat.id)
log_to_sheets(message.chat.id, name=message.from_user.first_name or "")
bot.send_message(message.chat.id,
f"Привет, {message.from_user.first_name}! \n\n"
"Я Viamo — твой помощник по поступлению за рубеж.\n\n"
"Помогу найти университеты под твой профиль, собрать документы и не пропустить "Что хочешь сделать?",
reply_markup=main_menu_markup())
дедлай
@bot.message_handler(commands=["stop"])
def stop_cmd(message):
bot.clear_step_handler_by_chat_id(message.chat.id)
user_data[message.chat.id] = {}
WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
bot.send_message(message.chat.id, "Остановлено. Возвращаю в главное меню!", reply_markup=
@bot.message_handler(commands=["stats"])
def show_stats(message):
total = len(STATS["total_users"])
today = len(STATS["started_today"])
completed = STATS["completed"]
top_c = sorted(STATS["citizenships"].items(), key=lambda x: x[1], reverse=True)[:5]
top_f = sorted(STATS["fields"].items(), key=lambda x: x[1], reverse=True)[:5]
response = f" *Статистика Viamo*\n\n Всего: *{total}*\n Сегодня: *{today}*\n Зав
if top_c:
response += "* Топ гражданств:*\n" + "\n".join(f" {c}: {n}" for c, n in top_c) + "
if top_f:
response += "* Топ направлений:*\n" + "\n".join(f" {f}: {n}" for f, n in top_f)
response += "\n\n _Сбрасывается при перезапуске. Постоянные данные — в Google Sheets._"
bot.send_message(message.chat.id, response, parse_mode="Markdown")
@bot.message_handler(func=lambda m: m.text in [" Подобрать университеты", " def ask_name(message):
bot.clear_step_handler_by_chat_id(message.chat.id)
user_data[message.chat.id] = {}
WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
bot.send_message(message.chat.id, "Отлично! Давай познакомимся bot.register_next_step_handler(message, ask_age)
Подобрать зан
\n\nКак тебя зовут?")
def ask_age(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["name"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add("До 18", "18–22"); markup.add("23–27", "28+")
bot.send_message(message.chat.id, f"Приятно познакомиться, {message.text}! \n\nСколько
bot.register_next_step_handler(message, ask_grade_or_status)
def ask_grade_or_status(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["age"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
if message.text == "До 18":
markup.add("8 класс", "9 класс"); markup.add("10 класс", "11 класс"); markup.add("Дру
bot.send_message(message.chat.id, "В каком классе ты сейчас?", reply_markup=markup)
else:
markup.add(" Студент", " Выпускник"); markup.add(" Работаю", "Другое")
bot.send_message(message.chat.id, "Кто ты сейчас?", reply_markup=markup)
bot.register_next_step_handler(message, ask_citizenship)
def ask_citizenship(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["age_or_grade"] = message.text
user_data[message.chat.id]["status"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Россия", " Казахстан"); markup.add(" Узбекистан", " Украина")
markup.add(" Азербайджан", " Беларусь"); markup.add(" Грузия", "Другое")
bot.send_message(message.chat.id, "Твоё гражданство?", reply_markup=markup)
bot.register_next_step_handler(message, ask_gpa)
def ask_gpa(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["citizenship"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Отлично (4.5–5)"); markup.add(" Хорошо (3.5–4.5)"); mark
bot.send_message(message.chat.id, "Твой средний балл?", reply_markup=markup)
bot.register_next_step_handler(message, ask_achievements)
def ask_achievements(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["gpa"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Международные олимпиады"); markup.add(" Национальные олимпиады")
markup.add(" Школьные / университетские"); markup.add(" Пока нет")
bot.send_message(message.chat.id, "Есть ли у тебя академические достижения?", reply_marku
bot.register_next_step_handler(message, ask_achievements_detail)
def ask_achievements_detail(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["achievements"] = message.text
if " " in message.text:
user_data[message.chat.id]["achievements_detail"] = ""
ask_english(message)
return
bot.send_message(message.chat.id,
"Расскажи подробнее — напиши свои достижения через запятую \n\n"
"_Например: призёр олимпиады по математике, победитель хакатона_",
parse_mode="Markdown")
bot.register_next_step_handler(message, process_achievements_detail)
def process_achievements_detail(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["achievements_detail"] = message.text
analysis = analyze_achievements(message.text)
response = " *Анализ твоих достижений:*\n\n" + "\n\n".join(analysis) + "\n\n _Упомяни
bot.send_message(message.chat.id, response, parse_mode="Markdown")
ask_english(message)
def ask_english(message):
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" A1–A2", " B1–B2"); markup.add(" C1", " C2")
bot.send_message(message.chat.id, "Уровень английского?", reply_markup=markup)
bot.register_next_step_handler(message, ask_certificate)
def ask_certificate(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["english"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" IELTS", " TOEFL"); markup.add(" Goethe / TestDaF", " DELF / DALF")
markup.add(" Планирую сдать", " Нет")
bot.send_message(message.chat.id, "Языковые сертификаты?", reply_markup=markup)
bot.register_next_step_handler(message, ask_other_language)
def ask_other_language(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["certificate"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Немецкий", " Французский"); markup.add(" Турецкий", " Китайский")
markup.add(" Корейский", " Сербский"); markup.add(" Чешский", " Венгерский")
markup.add(" Только английский / русский")
bot.send_message(message.chat.id, "Знаешь ли ты другие языки?\n\n Во многих странах мож
bot.register_next_step_handler(message, ask_other_language_level)
def ask_other_language_level(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["other_language"] = message.text
if " " in message.text:
user_data[message.chat.id]["other_language_level"] = "Нет"
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Есть, действующий"); markup.add(" Скоро истечёт"); markup.add(" Н
bot.send_message(message.chat.id, "Загранпаспорт?", reply_markup=markup)
bot.register_next_step_handler(message, ask_visa)
return
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Начинающий (A1–A2)", " Средний (B1–B2)"); markup.add(" Продвинутый (C
bot.send_message(message.chat.id, f"Какой уровень {message.text}?", reply_markup=markup)
bot.register_next_step_handler(message, ask_passport)
def ask_passport(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["other_language_level"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Есть, действующий"); markup.add(" Скоро истечёт"); markup.add(" bot.send_message(message.chat.id, "Загранпаспорт?", reply_markup=markup)
bot.register_next_step_handler(message, ask_visa)
Нет")
def ask_visa(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["passport"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Нет опыта", " Туристические"); markup.add(" Студенческие", " bot.send_message(message.chat.id, "Опыт получения виз?", reply_markup=markup)
bot.register_next_step_handler(message, ask_hobbies)
Были о
def ask_hobbies(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["visa"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Спорт", " Музыка"); markup.add(" Технологии", " Искусство")
markup.add(" Наука / чтение", " Волонтёрство"); markup.add(" Бизнес", " Путешест
bot.send_message(message.chat.id, "Твои главные увлечения?", reply_markup=markup)
bot.register_next_step_handler(message, ask_personality)
def ask_personality(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["hobbies"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Интроверт"); markup.add(" Экстраверт"); markup.add(" Посередине")
bot.send_message(message.chat.id, "Как бы ты описал себя?", reply_markup=markup)
bot.register_next_step_handler(message, ask_stress)
def ask_stress(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["personality"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Ищу решение", " Прошу помощи"); markup.add(" Отвлекаюсь", " Замыкаю
bot.send_message(message.chat.id, "Как реагируешь на стресс?", reply_markup=markup)
bot.register_next_step_handler(message, ask_leadership)
def ask_leadership(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["stress"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Беру инициативу"); markup.add(" Поддерживаю команду"); markup.add(" Р
bot.send_message(message.chat.id, "В команде ты чаще...", reply_markup=markup)
bot.register_next_step_handler(message, ask_goal)
def ask_goal(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["leadership"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Остаться за рубежом"); markup.add(" Вернуться домой"); markup.add(" П
bot.send_message(message.chat.id, "Что планируешь после учёбы?", reply_markup=markup)
bot.register_next_step_handler(message, ask_career)
def ask_career(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["goal"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" IT / Стартап", " Корпорация"); markup.add(" Своё дело", " Наука");
bot.send_message(message.chat.id, "Карьерная цель?", reply_markup=markup)
bot.register_next_step_handler(message, ask_priority)
def ask_priority(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["career"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Рейтинг вуза", " Стоимость"); markup.add(" Страна", " Трудоустройст
markup.add(" Город и жизнь", " Безопасность")
bot.send_message(message.chat.id, "Что важнее при выборе университета?", reply_markup=mar
bot.register_next_step_handler(message, ask_main_field)
def ask_main_field(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
user_data[message.chat.id]["priority"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
for f in FIELDS.keys():
markup.add(f)
bot.send_message(message.chat.id, "Почти готово! \n\nВыбери направление учёбы:", bot.register_next_step_handler(message, ask_sub_field)
reply_
def ask_sub_field(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
main_field = message.text
if main_field not in FIELDS:
bot.send_message(message.chat.id, "Пожалуйста выбери направление из списка")
bot.register_next_step_handler(message, ask_sub_field)
return
user_data[message.chat.id]["main_field"] = main_field
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
for sub in FIELDS[main_field]:
markup.add(sub)
bot.send_message(message.chat.id, "Уточни специальность:", reply_markup=markup)
bot.register_next_step_handler(message, ask_sub_subfield)
def ask_sub_subfield(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
sub_field = message.text
user_data[message.chat.id]["field"] = sub_field
cf = clean_field(sub_field)
subfields = SUBFIELDS.get(cf, [])
if subfields:
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
for s in subfields:
markup.add(s)
markup.add(" Любое направление")
bot.send_message(message.chat.id, f"Уточни направление в рамках {cf}:", reply_markup=
bot.register_next_step_handler(message, ask_budget)
else:
ask_budget(message)
def ask_budget(message):
if message.text and message.text.startswith("/"): bot.clear_step_handler_by_chat_id(messa
if "subfield" not in user_data[message.chat.id]:
user_data[message.chat.id]["subfield"] = message.text
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Бесплатно / стипендия"); markup.add(" До €5,000 в год")
markup.add(" До €15,000 в год"); markup.add(" Бюджет не ограничен")
bot.send_message(message.chat.id, "Бюджет на обучение в год?", reply_markup=markup)
bot.register_next_step_handler(message, show_results)
def get_profile_type(data):
hobbies = data.get("hobbies", "")
career = data.get("career", "")
if "Технологии" in hobbies or "IT" in career:
return " Технологический лидер", "Аналитический ум, любишь решать сложные задачи, н
elif "Наука" in hobbies or "Наука" in career:
return " Исследователь", "Глубокое мышление, любишь докапываться до сути"
elif "Бизнес" in hobbies or "Своё дело" in career:
return " Предприниматель", "Амбициозный, видишь возможности там где другие видят пр
elif "Искусство" in hobbies:
return " Творческая личность", "Мыслишь образами, создаёшь красоту, видишь мир инач
elif "Волонтёрство" in hobbies or "Социальные" in career:
return " Созидатель", "Хочешь менять мир к лучшему"
else:
return " Искатель возможностей", "Открыт к новому, гибкий, найдёшь себя в любой сре
def get_missing_requirements(data, budget):
missing = []
if "A1" in data.get("english", "") or "A2" in data.get("english", ""):
missing.append(" Подтяни английский до B2")
if " Нет" in data.get("certificate", ""):
missing.append(" Сдай IELTS или TOEFL")
if "Планирую" in data.get("certificate", ""):
missing.append(" Запишись на IELTS — подготовка 3-6 месяцев")
if " Нет" in data.get("passport", ""):
missing.append(" Оформи загранпаспорт")
if " " in data.get("passport", ""):
missing.append(" Продли загранпаспорт")
if "Удовл" in data.get("gpa", ""):
missing.append(" Подними средний балл")
if "Бесплатно" in budget:
missing.append(" Расширь бюджет или активно ищи стипендии")
return missing
def show_results(message):
if message.text and message.text.startswith("/"):
bot.clear_step_handler_by_chat_id(message.chat.id)
start(message)
return
data = user_data.get(message.chat.id, {})
citizenship = data.get("citizenship", "")
field = data.get("field", "")
budget = message.text
is_rf = "Россия" in citizenship
cf = clean_field(field)
bot.send_message(message.chat.id, " Анализирую твой профиль...")
update_stats(message.chat.id, citizenship=citizenship, field=cf, completed=True)
log_to_sheets(message.chat.id, name=data.get("name", ""), citizenship=citizenship, field=
results = []
for uni in UNIVERSITIES:
if not uni["name"]: continue
if is_rf and not uni["rf_ok"]: continue
if normalize(uni["field"]) != normalize(cf): continue
if "Бесплатно" in budget and uni["cost"] != "Бесплатно": continue
uni_copy = dict(uni)
uni_copy["score"] = score_university(uni, data)
results.append(uni_copy)
results.sort(key=lambda x: x["score"], reverse=True)
name = data.get("name", "")
profile_type, profile_desc = get_profile_type(data)
subfield = data.get("subfield", "")
time_type, time_label = get_time_to_enroll(data)
bot.send_message(message.chat.id,
f" *Твой профиль готов, {name}!*\n\n{profile_type}\n_{profile_desc}_\n\n До посту
parse_mode="Markdown")
if not results:
missing = get_missing_requirements(data, budget)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Сменить специальность", " Сменить направление")
markup.add(" Расширить бюджет", " Начать заново")
msg = f" Не нашла университетов по *{cf}* с твоими критериями.\n\n"
if missing:
msg += " *Что стоит подготовить:*\n" + "\n".join(missing) + "\n\n"
msg += "Что изменим?"
bot.send_message(message.chat.id, msg, parse_mode="Markdown", reply_markup=markup)
return
subfield_text = f" · {subfield}" if subfield and " " not in subfield else ""
response = f" *Топ для тебя — {cf}{subfield_text}:*\n\n"
for uni in results[:6]:
rf_status = " " if uni["rf_ok"] else " "
stars = " " * min(uni["score"], 5) if uni["score"] > 0 else ""
reasons = get_match_reasons(uni, data)
reason_text = f"\n_{reasons[0]}_" if reasons else ""
response += f"{uni['flag']} *{uni['name']}* — {uni['country']} {stars}\n {uni['cost
response += " Напиши название университета чтобы узнать подробнее!\n\n"
response += " _Хочешь обсудить варианты? [Чат поступающих](https://t.me/Cvoi_Abroad)_\n
response += " _Данные актуальны на 2025 год._"
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Подобрать заново", " Чеклист документов")
bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=markup)
WAITING_FOR_UNI_SEARCH.add(message.chat.id)
@bot.message_handler(func=lambda m: m.text == " def change_speciality(message):
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
Сменить специальность")
for f in FIELDS.keys():
markup.add(f)
bot.send_message(message.chat.id, "Выбери новое направление:", reply_markup=markup)
bot.register_next_step_handler(message, ask_sub_field)
@bot.message_handler(func=lambda m: m.text == " Сменить направление")
def change_direction(message):
main_field = user_data.get(message.chat.id, {}).get("main_field", "")
if main_field and main_field in FIELDS:
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
for sub in FIELDS[main_field]:
markup.add(sub)
bot.send_message(message.chat.id, "Выбери другое направление:", reply_markup=markup)
bot.register_next_step_handler(message, ask_sub_subfield)
else:
change_speciality(message)
@bot.message_handler(func=lambda m: m.text == " Расширить бюджет")
def expand_budget(message):
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" До €5,000 в год"); markup.add(" До €15,000 в год"); markup.add(" bot.send_message(message.chat.id, "Выбери новый бюджет:", reply_markup=markup)
bot.register_next_step_handler(message, show_results)
Бюдж
@bot.message_handler(func=lambda m: m.text == " Чат для поступающих")
def show_community_chat(message):
bot.send_message(message.chat.id,
" *Сообщество поступающих за рубеж*\n\n"
"Присоединяйся к чату где собрались такие же как ты!\n\n"
"Там можно:\n"
"— найти единомышленников\n"
"— задать вопросы тем кто уже учится\n"
"— поделиться своим опытом\n"
"— получить поддержку\n\n"
" [Присоединиться к чату](https://t.me/Cvoi_Abroad)",
parse_mode="Markdown",
reply_markup=main_menu_markup())
@bot.message_handler(func=lambda m: m.text == " Быстрый поиск")
def quick_search(message):
WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" По направлению", " По стране")
markup.add(" Бесплатные", " Со стипендией")
markup.add(" В главное меню")
bot.send_message(message.chat.id, "Как хочешь искать?", reply_markup=markup)
bot.register_next_step_handler(message, quick_search_filter)
def quick_search_filter(message):
if message.text == " По направлению":
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
for f in FIELDS.keys():
markup.add(f)
bot.send_message(message.chat.id, "Выбери направление:", reply_markup=markup)
bot.register_next_step_handler(message, quick_search_by_main_field)
elif message.text == " По стране":
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Германия", " Нидерланды"); markup.add(" Венгрия", " Чехия")
markup.add(" Сербия", " Грузия"); markup.add(" Турция", " Китай")
markup.add(" Южная Корея", " США"); markup.add(" Великобритания", " Армения"
markup.add(" Австрия", " Казахстан")
bot.send_message(message.chat.id, "Выбери страну:", reply_markup=markup)
bot.register_next_step_handler(message, quick_search_by_country)
elif message.text == " Бесплатные":
quick_show_filtered(message.chat.id, cost_filter="Бесплатно")
elif message.text == " Со стипендией":
quick_show_filtered(message.chat.id, scholarship_filter=True)
else:
start(message)
def quick_search_by_main_field(message):
main_field = message.text
if main_field not in FIELDS:
start(message)
return
user_data[message.chat.id]["quick_main_field"] = main_field
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
for sub in FIELDS[main_field]:
markup.add(sub)
markup.add(" Все специальности")
bot.send_message(message.chat.id, "Уточни специальность:", reply_markup=markup)
bot.register_next_step_handler(message, quick_search_by_sub_field)
def quick_search_by_sub_field(message):
main_field = user_data.get(message.chat.id, {}).get("quick_main_field", "")
if " " in message.text:
quick_show_filtered(message.chat.id, main_field=main_field)
else:
quick_show_filtered(message.chat.id, field_filter=message.text)
def quick_search_by_country(message):
text = message.text
parts = text.split(" ", 1)
country = parts[1].strip() if len(parts) > 1 else text.strip()
quick_show_filtered(message.chat.id, country_filter=country)
def quick_show_filtered(chat_id, field_filter=None, main_field=None, country_filter=None, cos
cf = clean_field(field_filter) if field_filter else None
cf_norm = normalize(cf) if cf else None
main_field_subs_norm = []
if main_field and main_field in FIELDS:
for s in FIELDS[main_field]:
main_field_subs_norm.append(normalize(clean_field(s)))
results = []
for uni in UNIVERSITIES:
if not uni["name"]: continue
uni_field_norm = normalize(uni["field"])
if cf_norm:
if cf_norm != uni_field_norm: continue
elif main_field_subs_norm:
if uni_field_norm not in main_field_subs_norm: continue
if country_filter and normalize(country_filter) not in normalize(uni["country"]): con
if cost_filter and normalize(uni["cost"]) != normalize(cost_filter): continue
if scholarship_filter and (not uni["scholarship"].strip() or uni["scholarship"].strip
results.append(uni)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Быстрый поиск", " Подобрать университеты")
if not results:
label = cf or country_filter or ("бесплатные" if cost_filter else "со стипендией")
bot.send_message(chat_id, f"Не нашла университетов по *{label}* \n\nПопробуй return
другой
label = cf or country_filter or ("бесплатные" if cost_filter else "со стипендией")
*{label} — найдено {len(results)}:*\n\n"
response = f" for uni in results[:8]:
rf_status = " " if uni["rf_ok"] else " "
response += f"{uni['flag']} *{uni['name']}* — {uni['country']}\n if len(results) > 8:
{uni['cost']} · {u
response += f"_...и ещё {len(results) - 8}. Используй полный подбор для точных response += " Напиши название университета чтобы узнать подробнее!"
резуль
bot.send_message(chat_id, response, parse_mode="Markdown", reply_markup=markup)
WAITING_FOR_UNI_SEARCH.add(chat_id)
@bot.message_handler(func=lambda m: m.text == " def checklist(message):
WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
Чеклист документов")
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Германия", " Нидерланды"); markup.add(" Венгрия", " Чехия")
markup.add(" Сербия", " Грузия"); markup.add(" Турция", " Китай")
bot.send_message(message.chat.id, "Для какой страны нужен чеклист?", reply_markup=markup)
bot.register_next_step_handler(message, show_checklist)
def show_checklist(message):
checklists = {
" Германия": " *Германия:*\n\n Загранпаспорт\n Аттестат + нострификация\n
" Нидерланды": " *Нидерланды:*\n\n Загранпаспорт\n Аттестат (перевод + апост
" Венгрия": " *Венгрия:*\n\n Загранпаспорт\n Аттестат (перевод + апостиль)\n
" Чехия": " *Чехия:*\n\n Загранпаспорт\n Аттестат (нострификация)\n Чешски
" Сербия": " *Сербия:*\n\n Загранпаспорт\n Аттестат (перевод на сербский)\n
" Грузия": " *Грузия:*\n\n Загранпаспорт\n Аттестат (перевод)\n IELTS 5.5+
" Турция": " *Турция:*\n\n Загранпаспорт\n Аттестат (перевод + апостиль)\n
" Китай": " *Китай:*\n\n Загранпаспорт\n Аттестат (перевод + апостиль)\n М
}
text = checklists.get(message.text, "Пока нет чеклиста для этой страны. Скоро добавим!")
bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu_mar
@bot.message_handler(func=lambda m: m.text and m.text.startswith(" def show_admission_plan(message):
data = user_data.get(message.chat.id, {})
uni = data.get("last_uni")
if not uni:
План поступления"))
bot.send_message(message.chat.id, "Сначала выбери университет из списка!")
return
plan = get_admission_plan(uni, data)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Подобрать заново", " Чеклист документов")
bot.send_message(message.chat.id, plan, parse_mode="Markdown", reply_markup=markup)
@bot.message_handler(func=lambda m: m.text == " Сравнить с другим")
def start_compare(message):
uni = user_data.get(message.chat.id, {}).get("last_uni")
if not uni:
bot.send_message(message.chat.id, "Сначала открой карточку университета!")
return
compare_list = user_data[message.chat.id].get("compare_list", [])
if not any(u["name"] == uni["name"] for u in compare_list):
compare_list.append(uni)
user_data[message.chat.id]["compare_list"] = compare_list
if len(compare_list) < 2:
bot.send_message(message.chat.id,
f" *{uni['name']}* добавлен к сравнению!\n\nТеперь найди второй университет и н
parse_mode="Markdown")
else:
show_comparison(message)
def show_comparison(message):
compare_list = user_data.get(message.chat.id, {}).get("compare_list", [])
if len(compare_list) < 2:
bot.send_message(message.chat.id, "Добавь минимум 2 университета!")
return
unis = compare_list[:3]
response = " *Сравнение университетов:*\n\n"
fields_to_compare = [
(" Страна", "country"), (" Стоимость", "cost"), (" Стипендия", "scholarship"),
(" Язык", "language"), (" IELTS", "ielts"), (" Дедлайн", "deadline"),
(" Длительность", "duration"), (" Жильё", "housing"), (" Экзамены", "exams"),
]
for label, key in fields_to_compare:
response += f"\n{label}:\n"
for uni in unis:
response += f" {uni['flag']} {uni['name'][:20]}: {uni.get(key, '—')[:30]}\n"
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Очистить сравнение")
markup.add(" Подобрать заново", " Чеклист документов")
user_data[message.chat.id]["compare_list"] = []
bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=markup)
@bot.message_handler(func=lambda m: m.text == " Очистить сравнение")
def clear_comparison(message):
user_data[message.chat.id]["compare_list"] = []
bot.send_message(message.chat.id, "Список сравнения очищен!", reply_markup=main_menu_mark
@bot.message_handler(func=lambda m: m.chat.id in WAITING_FOR_UNI_SEARCH and m.text and def handle_university_search(message):
query = message.text.lower()
found = [u for u in UNIVERSITIES if query in u["name"].lower()]
if not found:
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(" Подобрать университеты", " Чеклист документов")
bot.send_message(message.chat.id, "Не нашла такой университет return
\n\nПроверь название
uni = found[0]
rf_status = " Принимают" if uni["rf_ok"] else " data = user_data.get(message.chat.id, {})
reasons = get_match_reasons(uni, data)
emp = EMPLOYMENT_BY_COUNTRY.get(uni["country"], {})
emp_text = ""
if emp:
Уточняй на сайте"
emp_text = (f"\n *Трудоустройство* {emp.get('score', '')}\n"
f"Рынок: {emp.get('market', '')}\n"
not m.
f"Зарплата: {emp.get('salary', '')}\n"
f"Виза: {emp.get('visa', '')}\n"
f"Остаться: {emp.get('stay', '')}\n")
response = (
f"{uni['flag']} *{uni['name']}*\n"
f" {uni['country']} · {uni['field']}\n\n"
f" *Финансы*\nОбучение: {uni['cost']}\nСтипендия: {uni['scholarship']}\nРабота: {un
f" *Поступление*\nЯзык обучения: {uni['language']}\nВступительные экзамены: {uni['e
f"IELTS: {uni['ielts']}\nДедлайн: {uni['deadline']}\nДлительность: {uni['duration']}\
f" *Сильные стороны*\n{uni['strengths']}\n\n"
f" *Жизнь*\nЖильё: {uni['housing']}\nСНГ-комьюнити: {uni['community']}\n\n"
f" *Для граждан РФ:* {rf_status}"
+ emp_text
)
if reasons:
response += "\n *Почему подходит тебе:*\n" + "\n".join(f"• {r}" for r in reasons[:3
response += "\n\n _Данные актуальны на 2025 год._"
uni_name_short = uni["name"][:20]
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(f" План поступления в {uni_name_short}")
markup.add(f" Чеклист для {uni['country']}")
markup.add(" Сравнить с другим")
markup.add(" Подобрать заново")
user_data[message.chat.id]["last_uni"] = uni
if "compare_list" not in user_data[message.chat.id]:
user_data[message.chat.id]["compare_list"] = []
bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=markup)
bot.infinity_polling()
