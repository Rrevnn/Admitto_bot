import telebot
from telebot import types
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
user_data = {}

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

UNIVERSITIES = [
    {"name": "TU Munich", "country": "Германия", "flag": "🇩🇪", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD €800/мес"},
    {"name": "TU Berlin", "country": "Германия", "flag": "🇩🇪", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "KIT Karlsruhe", "country": "Германия", "flag": "🇩🇪", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "Czech Technical University", "country": "Чехия", "flag": "🇨🇿", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest Tech BME", "country": "Венгрия", "flag": "🇭🇺", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "METU", "country": "Турция", "flag": "🇹🇷", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Tsinghua University", "country": "Китай", "flag": "🇨🇳", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "KAIST", "country": "Южная Корея", "flag": "🇰🇷", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "TU Delft", "country": "Нидерланды", "flag": "🇳🇱", "field": "Data Science", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "Eindhoven University", "country": "Нидерланды", "flag": "🇳🇱", "field": "Data Science", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "Harbin Institute of Technology", "country": "Китай", "flag": "🇨🇳", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "POSTECH", "country": "Южная Корея", "flag": "🇰🇷", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "University of Tartu", "country": "Эстония", "flag": "🇪🇪", "field": "Data Science", "cost": "€1,660/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "TU Munich AI", "country": "Германия", "flag": "🇩🇪", "field": "AI / Machine Learning", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "Bilkent University", "country": "Турция", "flag": "🇹🇷", "field": "AI / Machine Learning", "cost": "$6,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Seoul National University", "country": "Южная Корея", "flag": "🇰🇷", "field": "AI / Machine Learning", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "TU Berlin Security", "country": "Германия", "flag": "🇩🇪", "field": "Кибербезопасность", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "University of Tartu Security", "country": "Эстония", "flag": "🇪🇪", "field": "Кибербезопасность", "cost": "€1,660/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "KIT Karlsruhe Robotics", "country": "Германия", "flag": "🇩🇪", "field": "Робототехника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "KAIST Robotics", "country": "Южная Корея", "flag": "🇰🇷", "field": "Робототехника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
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
    {"name": "Budapest ELTE Astronomy", "country": "Венгрия", "flag": "🇭🇺", "field": "Астрономия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Charles University Astronomy", "country": "Чехия", "flag": "🇨🇿", "field": "Астрономия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Ankara University Astronomy", "country": "Турция", "flag": "🇹🇷", "field": "Астрономия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Peking University Astronomy", "country": "Китай", "flag": "🇨🇳", "field": "Астрономия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "Seoul National University Astronomy", "country": "Южная Корея", "flag": "🇰🇷", "field": "Астрономия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "Corvinus University", "country": "Венгрия", "flag": "🇭🇺", "field": "Менеджмент", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Prague University of Economics", "country": "Чехия", "flag": "🇨🇿", "field": "Менеджмент", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Nazarbayev University", "country": "Казахстан", "flag": "🇰🇿", "field": "Менеджмент", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Полная стипендия"},
    {"name": "IE University", "country": "Испания", "flag": "🇪🇸", "field": "Финансы", "cost": "$15,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Tbilisi Free University", "country": "Грузия", "flag": "🇬🇪", "field": "Финансы", "cost": "€3,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "American University of Armenia", "country": "Армения", "flag": "🇦🇲", "field": "Маркетинг", "cost": "$5,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Koç University Business", "country": "Турция", "flag": "🇹🇷", "field": "Предпринимательство", "cost": "$9,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Heriot-Watt Dubai", "country": "ОАЭ", "flag": "🇦🇪", "field": "Логистика", "cost": "$12,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
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
    {"name": "Aalto University", "country": "Финляндия", "flag": "🇫🇮", "field": "Графический дизайн", "cost": "€5,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Yildiz Technical University", "country": "Турция", "flag": "🇹🇷", "field": "Графический дизайн", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Design Academy Eindhoven", "country": "Нидерланды", "flag": "🇳🇱", "field": "UX/UI", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "TU Delft Architecture", "country": "Нидерланды", "flag": "🇳🇱", "field": "Архитектура", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "Academy of Fine Arts Vienna", "country": "Австрия", "flag": "🇦🇹", "field": "Архитектура", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Tbilisi Academy of Arts", "country": "Грузия", "flag": "🇬🇪", "field": "Мода", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Bezalel Academy", "country": "Израиль", "flag": "🇮🇱", "field": "Анимация", "cost": "$8,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Charles University Journalism", "country": "Чехия", "flag": "🇨🇿", "field": "Журналистика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Vienna Politics", "country": "Австрия", "flag": "🇦🇹", "field": "Политология", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Budapest ELTE Politics", "country": "Венгрия", "flag": "🇭🇺", "field": "Политология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "American University of Armenia Law", "country": "Армения", "flag": "🇦🇲", "field": "Право", "cost": "$5,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "University of Belgrade Law", "country": "Сербия", "flag": "🇷🇸", "field": "Право", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Corvinus University IR", "country": "Венгрия", "flag": "🇭🇺", "field": "Международные отношения", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Tbilisi State University IR", "country": "Грузия", "flag": "🇬🇪", "field": "Дипломатия", "cost": "€1,200/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Prague University Sociology", "country": "Чехия", "flag": "🇨🇿", "field": "Социология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Vienna History", "country": "Австрия", "flag": "🇦🇹", "field": "История", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Charles University Philosophy", "country": "Чехия", "flag": "🇨🇿", "field": "Философия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest ELTE Linguistics", "country": "Венгрия", "flag": "🇭🇺", "field": "Лингвистика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Tbilisi State University Culture", "country": "Грузия", "flag": "🇬🇪", "field": "Культурология", "cost": "€1,200/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "TU Munich Engineering", "country": "Германия", "flag": "🇩🇪", "field": "Машиностроение", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "KIT Karlsruhe Engineering", "country": "Германия", "flag": "🇩🇪", "field": "Машиностроение", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "Budapest Tech Electrical", "country": "Венгрия", "flag": "🇭🇺", "field": "Электроника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Czech Technical University Civil", "country": "Чехия", "flag": "🇨🇿", "field": "Строительство", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Belgrade Engineering", "country": "Сербия", "flag": "🇷🇸", "field": "Энергетика", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "TU Delft Aerospace", "country": "Нидерланды", "flag": "🇳🇱", "field": "Авиация", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "University of Vienna Education", "country": "Австрия", "flag": "🇦🇹", "field": "Педагогика", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Budapest ELTE Education", "country": "Венгрия", "flag": "🇭🇺", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Charles University Education", "country": "Чехия", "flag": "🇨🇿", "field": "Психология образования", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
]

@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔍 Подобрать университеты')
    markup.add('📋 Чеклист документов')
    markup.add('❓ Задать вопрос')
    bot.send_message(message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я Viamo — твой помощник по поступлению за рубеж.\n\n"
        "Помогу найти университеты под твой профиль, собрать документы и не пропустить дедлайны.\n\n"
        "Что хочешь сделать?",
        reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '🔍 Подобрать университеты')
def ask_name(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id,
        "Отлично! Давай познакомимся поближе — это займёт пару минут, зато подборка будет точной 🎯\n\nКак тебя зовут?")
    bot.register_next_step_handler(message, ask_age)

def ask_age(message):
    user_data[message.chat.id]['name'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('До 18', '18–22')
    markup.add('23–27', '28+')
    bot.send_message(message.chat.id, f"Приятно познакомиться, {message.text}! 👋\n\nСколько тебе лет?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_citizenship)

def ask_citizenship(message):
    user_data[message.chat.id]['age'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇷🇺 Россия', '🇰🇿 Казахстан')
    markup.add('🇺🇿 Узбекистан', '🇺🇦 Украина')
    markup.add('🇦🇿 Азербайджан', '🇧🇾 Беларусь')
    markup.add('🇬🇪 Грузия', 'Другое')
    bot.send_message(message.chat.id, "Твоё гражданство?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_status)

def ask_status(message):
    user_data[message.chat.id]['citizenship'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🎒 Школьник', '🎓 Студент')
    markup.add('📄 Выпускник', '💼 Работаю')
    bot.send_message(message.chat.id, "Кто ты сейчас?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_gpa)

def ask_gpa(message):
    user_data[message.chat.id]['status'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('⭐⭐⭐⭐⭐ Отлично (4.5–5)')
    markup.add('⭐⭐⭐⭐ Хорошо (3.5–4.5)')
    markup.add('⭐⭐⭐ Удовлетворительно')
    bot.send_message(message.chat.id, "Твой средний балл?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_achievements)

def ask_achievements(message):
    user_data[message.chat.id]['gpa'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🏆 Международные олимпиады')
    markup.add('🥇 Национальные олимпиады')
    markup.add('📚 Школьные / университетские')
    markup.add('➖ Пока нет')
    bot.send_message(message.chat.id, "Есть ли у тебя академические достижения?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_english)

def ask_english(message):
    user_data[message.chat.id]['achievements'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔴 A1–A2', '🟡 B1–B2')
    markup.add('🟢 C1', '⭐ C2')
    bot.send_message(message.chat.id, "Уровень английского?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_certificate)

def ask_certificate(message):
    user_data[message.chat.id]['english'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('✅ IELTS', '✅ TOEFL')
    markup.add('✅ Goethe / TestDaF', '✅ DELF / DALF')
    markup.add('📅 Планирую сдать', '➖ Нет')
    bot.send_message(message.chat.id, "Языковые сертификаты?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_passport)

def ask_passport(message):
    user_data[message.chat.id]['certificate'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('✅ Есть, действующий')
    markup.add('⚠️ Скоро истечёт')
    markup.add('❌ Нет')
    bot.send_message(message.chat.id, "Загранпаспорт?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_visa)

def ask_visa(message):
    user_data[message.chat.id]['passport'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('➖ Нет опыта', '✈️ Туристические')
    markup.add('🎓 Студенческие', '⚠️ Были отказы')
    bot.send_message(message.chat.id, "Опыт получения виз?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_hobbies)

def ask_hobbies(message):
    user_data[message.chat.id]['visa'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('⚽ Спорт', '🎵 Музыка')
    markup.add('💻 Технологии', '🎨 Искусство')
    markup.add('📚 Наука / чтение', '🤝 Волонтёрство')
    markup.add('💼 Бизнес', '✈️ Путешествия')
    bot.send_message(message.chat.id, "Твои главные увлечения?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_personality)

def ask_personality(message):
    user_data[message.chat.id]['hobbies'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🧩 Интроверт')
    markup.add('🌟 Экстраверт')
    markup.add('⚖️ Посередине')
    bot.send_message(message.chat.id, "Как бы ты описал себя?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_stress)

def ask_stress(message):
    user_data[message.chat.id]['personality'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💡 Ищу решение', '🤝 Прошу помощи')
    markup.add('🎮 Отвлекаюсь', '🔒 Замыкаюсь')
    bot.send_message(message.chat.id, "Как реагируешь на стресс?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_leadership)

def ask_leadership(message):
    user_data[message.chat.id]['stress'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🦁 Беру инициативу')
    markup.add('🤝 Поддерживаю команду')
    markup.add('🎯 Работаю самостоятельно')
    bot.send_message(message.chat.id, "В команде ты чаще...", reply_markup=markup)
    bot.register_next_step_handler(message, ask_goal)

def ask_goal(message):
    user_data[message.chat.id]['leadership'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🌍 Остаться за рубежом')
    markup.add('🏠 Вернуться домой')
    markup.add('🤷 Пока не знаю')
    bot.send_message(message.chat.id, "Что планируешь после учёбы?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_career)

def ask_career(message):
    user_data[message.chat.id]['goal'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💻 IT / Стартап', '🏢 Корпорация')
    markup.add('🚀 Своё дело', '🔬 Наука')
    markup.add('🌱 Социальные проекты')
    bot.send_message(message.chat.id, "Карьерная цель?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_priority)

def ask_priority(message):
    user_data[message.chat.id]['career'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🏆 Рейтинг вуза', '💰 Стоимость')
    markup.add('🌍 Страна', '💼 Трудоустройство')
    markup.add('🏙️ Город и жизнь', '🔒 Безопасность')
    bot.send_message(message.chat.id, "Что важнее при выборе университета?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_main_field)

def ask_main_field(message):
    user_data[message.chat.id]['priority'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for field in FIELDS.keys():
        markup.add(field)
    bot.send_message(message.chat.id,
        "Почти готово! 🎯\n\nВыбери направление учёбы:",
        reply_markup=markup)
    bot.register_next_step_handler(message, ask_sub_field)

def ask_sub_field(message):
    main_field = message.text
    if main_field not in FIELDS:
        bot.send_message(message.chat.id, "Пожалуйста выбери направление из списка")
        bot.register_next_step_handler(message, ask_sub_field)
        return
    user_data[message.chat.id]['main_field'] = main_field
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for sub in FIELDS[main_field]:
        markup.add(sub)
    bot.send_message(message.chat.id, "Уточни специальность:", reply_markup=markup)
    bot.register_next_step_handler(message, ask_budget)

def ask_budget(message):
    user_data[message.chat.id]['field'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💚 Бесплатно / стипендия')
    markup.add('💛 До €5,000 в год')
    markup.add('🧡 До €15,000 в год')
    markup.add('❤️ Бюджет не ограничен')
    bot.send_message(message.chat.id, "Бюджет на обучение в год?", reply_markup=markup)
    bot.register_next_step_handler(message, show_results)

def get_profile_type(data):
    hobbies = data.get('hobbies', '')
    career = data.get('career', '')
    if 'Технологии' in hobbies or 'IT' in career:
        return "🚀 Технологический лидер", "Аналитический ум, любишь решать сложные задачи, нацелен на tech-карьеру"
    elif 'Наука' in hobbies or 'Наука' in career:
        return "🔬 Исследователь", "Глубокое мышление, любишь докапываться до сути, создан для науки"
    elif 'Бизнес' in hobbies or 'Своё дело' in career:
        return "💼 Предприниматель", "Амбициозный, видишь возможности там где другие видят проблемы"
    elif 'Искусство' in hobbies:
        return "🎨 Творческая личность", "Мыслишь образами, создаёшь красоту, видишь мир иначе"
    elif 'Волонтёрство' in hobbies or 'Социальные' in career:
        return "🌱 Созидатель", "Хочешь менять мир к лучшему, люди для тебя важнее денег"
    else:
        return "🌍 Искатель возможностей", "Открыт к новому, гибкий, найдёшь себя в любой среде"

def show_results(message):
    data = user_data.get(message.chat.id, {})
    citizenship = data.get('citizenship', '')
    field = data.get('field', '')
    budget = message.text
    is_rf = 'Россия' in citizenship
    results = []

    for uni in UNIVERSITIES:
        if is_rf and not uni['rf_ok']:
            continue
        if uni['field'] != field:
            continue
        if 'Бесплатно' in budget and uni['cost'] != 'Бесплатно':
            continue
        results.append(uni)

    name = data.get('name', '')
    profile_type, profile_desc = get_profile_type(data)

    profile_msg = (
        f"✨ *Твой профиль готов, {name}!*\n\n"
        f"{profile_type}\n"
        f"_{profile_desc}_\n\n"
    )
    bot.send_message(message.chat.id, profile_msg, parse_mode='Markdown')

    if not results:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🔍 Подобрать заново')
        bot.send_message(message.chat.id,
            "Не нашла точных совпадений 😔\n\nПопробуй расширить бюджет или выбрать другую специальность.",
            reply_markup=markup)
        return

    response = f"🎯 *Нашла {len(results)} вариантов по специальности {field}:*\n\n"
    for uni in results[:6]:
        rf_status = "✅ Принимают" if uni['rf_ok'] else "⚠️ Уточняй"
        response += (
            f"{uni['flag']} *{uni['name']}* — {uni['country']}\n"
            f"💰 {uni['cost']} · 🎓 {uni['scholarship']}\n"
            f"Граждане РФ: {rf_status}\n\n"
        )
    response += "📌 Напиши название университета чтобы узнать подробнее!\n\n⚠️ Данные актуальны на 2025 год. Всегда проверяй информацию на официальном сайте университета перед подачей документов."

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔍 Подобрать заново', '📋 Чеклист документов')
    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '📋 Чеклист документов')
def checklist(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇩🇪 Германия', '🇳🇱 Нидерланды')
    markup.add('🇭🇺 Венгрия', '🇨🇿 Чехия')
    markup.add('🇷🇸 Сербия', '🇬🇪 Грузия')
    markup.add('🇹🇷 Турция', '🇨🇳 Китай')
    bot.send_message(message.chat.id, "Для какой страны нужен чеклист?", reply_markup=markup)
    bot.register_next_step_handler(message, show_checklist)

def show_checklist(message):
    checklists = {
        '🇩🇪 Германия': "📋 *Документы для Германии:*\n\n✅ Загранпаспорт\n✅ Аттестат + нострификация\n✅ IELTS 6.5+ или TestDaF\n✅ Мотивационное письмо\n✅ 2 рекомендательных письма\n✅ CV / резюме\n✅ Sperrkonto €11,208\n✅ Медицинская страховка\n\n⚠️ Для РФ: подача через uni-assist, срок до 8 недель",
        '🇳🇱 Нидерланды': "📋 *Документы для Нидерландов:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 6.0+\n✅ Мотивационное письмо\n✅ CV / резюме\n✅ Выписка с банковского счёта\n\n⚠️ Подача через Studielink",
        '🇭🇺 Венгрия': "📋 *Документы для Венгрии:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 5.5+\n✅ Мотивационное письмо\n✅ CV / резюме\n✅ Медицинская справка\n\n🎓 Stipendium Hungaricum покрывает всё!",
        '🇨🇿 Чехия': "📋 *Документы для Чехии:*\n\n✅ Загранпаспорт\n✅ Аттестат (нострификация)\n✅ Чешский язык B2 (для бесплатного)\n✅ Мотивационное письмо\n✅ CV / резюме\n\n⚠️ Бесплатно только на чешском языке",
        '🇷🇸 Сербия': "📋 *Документы для Сербии:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод на сербский)\n✅ Справка об отсутствии судимости\n✅ Медицинская справка\n\n✅ Виза не нужна для граждан РФ!",
        '🇬🇪 Грузия': "📋 *Документы для Грузии:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод)\n✅ IELTS 5.5+ (для англоязычных)\n✅ Мотивационное письмо\n\n✅ Виза не нужна для граждан РФ!",
        '🇹🇷 Турция': "📋 *Документы для Турции:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 6.0+\n✅ Мотивационное письмо\n✅ CV / резюме\n\n🎓 Türkiye Scholarships — подай до февраля!",
        '🇨🇳 Китай': "📋 *Документы для Китая:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ Медицинская справка\n✅ Мотивационное письмо\n✅ CV / резюме\n\n🎓 Стипендия CSC покрывает обучение и проживание!",
    }
    text = checklists.get(message.text, "Пока нет чеклиста для этой страны. Скоро добавим!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔍 Подобрать университеты', '📋 Чеклист документов')
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_university_search(message):
    query = message.text.lower()
    found = []
    for uni in UNIVERSITIES:
        if query in uni['name'].lower():
            found.append(uni)
    if not found:
        bot.send_message(message.chat.id,
            "Не нашла такой университет 😔\n\nПроверь название или напиши /start чтобы начать заново.")
        return

    uni = found[0]
    rf_status = "✅ Принимают без ограничений" if uni['rf_ok'] else "⚠️ Уточняй на сайте"

    details = {
        "Разработка": {"ielts": "6.5+", "deadline": "15 января / 15 июля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-чат и встречи"},
        "Data Science": {"ielts": "6.5+", "deadline": "1 февраля / 1 сентября", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €350/мес", "community": "Есть международное комьюнити"},
        "AI / Machine Learning": {"ielts": "7.0+", "deadline": "15 января", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Активное tech-комьюнити"},
        "Физика": {"ielts": "6.0+", "deadline": "15 января / 1 июля", "duration": "3 года (бакалавр) / 2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Небольшое СНГ-комьюнити"},
        "Химия": {"ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Есть русскоязычные студенты"},
        "Биология": {"ielts": "6.0+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €200/мес", "community": "Небольшое"},
        "Математика": {"ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Есть"},
        "Астрономия": {"ielts": "6.0+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Небольшое"},
        "Общая медицина": {"ielts": "6.5+", "deadline": "1 марта", "duration": "6 лет", "work": "Ограниченно", "housing": "Общежитие от €200/мес", "community": "Большое СНГ-комьюнити"},
        "Менеджмент": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Активное бизнес-комьюнити"},
        "Финансы": {"ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Есть"},
        "Архитектура": {"ielts": "6.0+", "deadline": "1 марта", "duration": "4 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Творческое комьюнити"},
        "Политология": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Есть"},
        "Право": {"ielts": "6.5+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €200/мес", "community": "Небольшое"},
    }

    d = details.get(uni['field'], {
        "ielts": "Уточняй на сайте",
        "deadline": "Уточняй на сайте",
        "duration": "Уточняй на сайте",
        "work": "До 20 часов в неделю",
        "housing": "Уточняй на сайте",
        "community": "Уточняй в местных чатах"
    })

    response = (
        f"{uni['flag']} *{uni['name']}*\n"
        f"📍 {uni['country']} · {uni['field']}\n\n"
        f"💰 *Финансы*\n"
        f"Обучение: {uni['cost']}\n"
        f"Стипендия: {uni['scholarship']}\n"
        f"Работа во время учёбы: {d['work']}\n\n"
        f"📋 *Поступление*\n"
        f"IELTS: {d['ielts']}\n"
        f"Дедлайн подачи: {d['deadline']}\n"
        f"Длительность программы: {d['duration']}\n\n"
        f"🏠 *Жизнь*\n"
        f"Жильё: {d['housing']}\n"
        f"СНГ-комьюнити: {d['community']}\n\n"
        f"🇷🇺 *Для граждан РФ:* {rf_status}\n\n"
        f"📌 Нужен чеклист документов для {uni['country']}? Нажми кнопку ниже!"
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(f"📋 Чеклист для {uni['country']}")
    markup.add('🔍 Подобрать заново')
    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)

bot.infinity_polling()
