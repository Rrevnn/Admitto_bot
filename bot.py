# Admitto Bot — поступление за рубеж для СНГ
import telebot
from telebot import types
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

user_data = {}

# Специальности и подкатегории
FIELDS = {
    "💻 IT и технологии": ["Разработка", "Data Science", "AI / Machine Learning", "Кибербезопасность", "Робототехника"],
    "⚗️ Естественные науки": ["Физика", "Химия", "Биология", "Экология", "Математика", "Астрономия"],
    "💼 Бизнес и экономика": ["Менеджмент", "Финансы", "Маркетинг", "Предпринимательство", "Логистика"],
    "⚕️ Медицина и здоровье": ["Общая медицина", "Стоматология", "Фармацевтика", "Психология", "Ветеринария"],
    "🎨 Дизайн и искусство": ["Графический дизайн", "UX/UI", "Архитектура", "Мода", "Анимация", "Фотография"],
    "🌍 Социальные науки": ["Журналистика", "Дипломатия", "Политология", "Социология", "Международные отношения", "Право"],
    "📚 Гуманитарные": ["История", "Философия", "Лингвистика", "Культурология", "Антропология"],
    "⚙️ Инженерия": ["Машиностроение", "Электроника", "Строительство", "Энергетика", "Авиация"],
    "🎓 Образование": ["Педагогика", "Психология образования", "Специальное образование"],
}

# База университетов
UNIVERSITIES = [
    # IT — Разработка
    {"name": "TU Munich", "country": "Германия", "flag": "🇩🇪", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD €800/мес"},
    {"name": "TU Berlin", "country": "Германия", "flag": "🇩🇪", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "KIT Karlsruhe", "country": "Германия", "flag": "🇩🇪", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "Czech Technical University", "country": "Чехия", "flag": "🇨🇿", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest Tech BME", "country": "Венгрия", "flag": "🇭🇺", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "METU", "country": "Турция", "flag": "🇹🇷", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Tsinghua University", "country": "Китай", "flag": "🇨🇳", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "KAIST", "country": "Южная Корея", "flag": "🇰🇷", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},

    # IT — Data Science
    {"name": "TU Delft", "country": "Нидерланды", "flag": "🇳🇱", "field": "Data Science", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "Eindhoven University", "country": "Нидерланды", "flag": "🇳🇱", "field": "Data Science", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "Harbin Institute of Technology", "country": "Китай", "flag": "🇨🇳", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "POSTECH", "country": "Южная Корея", "flag": "🇰🇷", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "University of Tartu", "country": "Эстония", "flag": "🇪🇪", "field": "Data Science", "cost": "€1,660/год", "rf_ok": True, "scholarship": "Частичные гранты"},

    # IT — AI
    {"name": "TU Munich AI", "country": "Германия", "flag": "🇩🇪", "field": "AI / Machine Learning", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "Bilkent University", "country": "Турция", "flag": "🇹🇷", "field": "AI / Machine Learning", "cost": "$6,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Seoul National University", "country": "Южная Корея", "flag": "🇰🇷", "field": "AI / Machine Learning", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},

    # IT — Кибербезопасность
    {"name": "TU Berlin Security", "country": "Германия", "flag": "🇩🇪", "field": "Кибербезопасность", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "University of Tartu Security", "country": "Эстония", "flag": "🇪🇪", "field": "Кибербезопасность", "cost": "€1,660/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Innopolis University Dubai", "country": "ОАЭ", "flag": "🇦🇪", "field": "Кибербезопасность", "cost": "$10,000/год", "rf_ok": True, "scholarship": "Нет"},

    # IT — Робототехника
    {"name": "KIT Karlsruhe Robotics", "country": "Германия", "flag": "🇩🇪", "field": "Робототехника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "KAIST Robotics", "country": "Южная Корея", "flag": "🇰🇷", "field": "Робототехника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "Warsaw University of Technology", "country": "Польша", "flag": "🇵🇱", "field": "Робототехника", "cost": "€2,000/год", "rf_ok": True, "scholarship": "Нет"},

    # Естественные науки
    {"name": "Heidelberg University", "country": "Германия", "flag": "🇩🇪", "field": "Физика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "LMU Munich", "country": "Германия", "flag": "🇩🇪", "field": "Физика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "Charles University", "country": "Чехия", "flag": "🇨🇿", "field": "Физика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest ELTE", "country": "Венгрия", "flag": "🇭🇺", "field": "Физика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Peking University", "country": "Китай", "flag": "🇨🇳", "field": "Физика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "University of Vienna", "country": "Австрия", "flag": "🇦🇹", "field": "Химия", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Masaryk University", "country": "Чехия", "flag": "🇨🇿", "field": "Химия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Koç University", "country": "Турция", "flag": "🇹🇷", "field": "Химия", "cost": "$5,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "University of Belgrade", "country": "Сербия", "flag": "🇷🇸", "field": "Биология", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Debrecen", "country": "Венгрия", "flag": "🇭🇺", "field": "Биология", "cost": "€2,000/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Tbilisi State University", "country": "Грузия", "flag": "🇬🇪", "field": "Биология", "cost": "€1,200/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Buenos Aires", "country": "Аргентина", "flag": "🇦🇷", "field": "Экология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Wroclaw", "country": "Польша", "flag": "🇵🇱", "field": "Экология", "cost": "€2,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest ELTE Math", "country": "Венгрия", "flag": "🇭🇺", "field": "Математика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Charles University Math", "country": "Чехия", "flag": "🇨🇿", "field": "Математика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},

    # Бизнес
    {"name": "Corvinus University", "country": "Венгрия", "flag": "🇭🇺", "field": "Менеджмент", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Prague University of Economics", "country": "Чехия", "flag": "🇨🇿", "field": "Менеджмент", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Nazarbayev University", "country": "Казахстан", "flag": "🇰🇿", "field": "Менеджмент", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Полная стипендия"},
    {"name": "IE University", "country": "Испания", "flag": "🇪🇸", "field": "Финансы", "cost": "$15,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Tbilisi Free University", "country": "Грузия", "flag": "🇬🇪", "field": "Финансы", "cost": "€3,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "American University of Armenia", "country": "Армения", "flag": "🇦🇲", "field": "Маркетинг", "cost": "$5,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Koç University Business", "country": "Турция", "flag": "🇹🇷", "field": "Предпринимательство", "cost": "$9,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Heriot-Watt Dubai", "country": "ОАЭ", "flag": "🇦🇪", "field": "Логистика", "cost": "$12,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},

    # Медицина
    {"name": "Charles University Medicine", "country": "Чехия", "flag": "🇨🇿", "field": "Общая медицина", "cost": "€8,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Semmelweis University", "country": "Венгрия", "flag": "🇭🇺", "field": "Общая медицина", "cost": "€9,000/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Tbilisi State Medical University", "country": "Грузия", "flag": "🇬🇪", "field": "Общая медицина", "cost": "$5,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Ankara University Medicine", "country": "Турция", "flag": "🇹🇷", "field": "Общая медицина", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Yerevan State Medical University", "country": "Армения", "flag": "🇦🇲", "field": "Общая медицина", "cost": "$4,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Debrecen Medicine", "country": "Венгрия", "flag": "🇭🇺", "field": "Стоматология", "cost": "€9,000/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Poznan University of Medicine", "country": "Польша", "flag": "🇵🇱", "field": "Стоматология", "cost": "€6,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Masaryk University Pharmacy", "country": "Чехия", "flag": "🇨🇿", "field": "Фармацевтика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Vienna Psychology", "country": "Австрия", "flag": "🇦🇹", "field": "Психология", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Budapest ELTE Psychology", "country": "Венгрия", "flag": "🇭🇺", "field": "Психология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "University of Belgrade Vet", "country": "Сербия", "flag": "🇷🇸", "field": "Ветеринария", "cost": "€2,000/год", "rf_ok": True, "scholarship": "Нет"},

    # Дизайн
    {"name": "Aalto University", "country": "Финляндия", "flag": "🇫🇮", "field": "Графический дизайн", "cost": "€5,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Yildiz Technical University", "country": "Турция", "flag": "🇹🇷", "field": "Графический дизайн", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Design Academy Eindhoven", "country": "Нидерланды", "flag": "🇳🇱", "field": "UX/UI", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "TU Delft Architecture", "country": "Нидерланды", "flag": "🇳🇱", "field": "Архитектура", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "Academy of Fine Arts Vienna", "country": "Австрия", "flag": "🇦🇹", "field": "Архитектура", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Tbilisi Academy of Arts", "country": "Грузия", "flag": "🇬🇪", "field": "Мода", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Bezalel Academy", "country": "Израиль", "flag": "🇮🇱", "field": "Анимация", "cost": "$8,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},

    # Социальные науки
    {"name": "Charles University Journalism", "country": "Чехия", "flag": "🇨🇿", "field": "Журналистика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Vienna Politics", "country": "Австрия", "flag": "🇦🇹", "field": "Политология", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Budapest ELTE Politics", "country": "Венгрия", "flag": "🇭🇺", "field": "Политология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "American University of Armenia Law", "country": "Армения", "flag": "🇦🇲", "field": "Право", "cost": "$5,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "University of Belgrade Law", "country": "Сербия", "flag": "🇷🇸", "field": "Право", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Corvinus University IR", "country": "Венгрия", "flag": "🇭🇺", "field": "Международные отношения", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Tbilisi State University IR", "country": "Грузия", "flag": "🇬🇪", "field": "Дипломатия", "cost": "€1,200/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Prague University Sociology", "country": "Чехия", "flag": "🇨🇿", "field": "Социология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},

    # Гуманитарные
    {"name": "University of Vienna History", "country": "Австрия", "flag": "🇦🇹", "field": "История", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Charles University Philosophy", "country": "Чехия", "flag": "🇨🇿", "field": "Философия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest ELTE Linguistics", "country": "Венгрия", "flag": "🇭🇺", "field": "Лингвистика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Tbilisi State University Culture", "country": "Грузия", "flag": "🇬🇪", "field": "Культурология", "cost": "€1,200/год", "rf_ok": True, "scholarship": "Нет"},

    # Инженерия
    {"name": "TU Munich Engineering", "country": "Германия", "flag": "🇩🇪", "field": "Машиностроение", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "KIT Karlsruhe Engineering", "country": "Германия", "flag": "🇩🇪", "field": "Машиностроение", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "Budapest Tech Electrical", "country": "Венгрия", "flag": "🇭🇺", "field": "Электроника", "cost":
