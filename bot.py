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
    {"name": "Budapest Tech Electrical", "country": "Венгрия", "flag": "🇭🇺", "field": "Электроника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Czech Technical University Civil", "country": "Чехия", "flag": "🇨🇿", "field": "Строительство", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Belgrade Engineering", "country": "Сербия", "flag": "🇷🇸", "field": "Энергетика", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "TU Delft Aerospace", "country": "Нидерланды", "flag": "🇳🇱", "field": "Авиация", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},

    # Образование
    {"name": "University of Vienna Education", "country": "Австрия", "flag": "🇦🇹", "field": "Педагогика", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Budapest ELTE Education", "country": "Венгрия", "flag": "🇭🇺", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Charles University Education", "country": "Чехия", "flag": "🇨🇿", "field": "Психология образования", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
]

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔍 Подобрать университеты')
    markup.add('📋 Чеклист документов')
    markup.add('❓ Задать вопрос')
    bot.send_message(message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я Admitto — твой помощник по поступлению за рубеж.\n\n"
        "Помогу найти университеты под твой профиль, собрать документы и не пропустить дедлайны.\n\n"
        "Что хочешь сделать?",
        reply_markup=markup)

# Шаг 1: гражданство
@bot.message_handler(func=lambda m: m.text == '🔍 Подобрать университеты')
def ask_citizenship(message):
    user_data[message.chat.id] = {}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇷🇺 Россия', '🇰🇿 Казахстан')
    markup.add('🇺🇿 Узбекистан', '🇺🇦 Украина')
    markup.add('🇦🇿 Азербайджан', 'Другое')
    bot.send_message(message.chat.id, "Твоё гражданство?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_main_field)

# Шаг 2: основная специальность
def ask_main_field(message):
    user_data[message.chat.id]['citizenship'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for field in FIELDS.keys():
        markup.add(field)
    bot.send_message(message.chat.id, "Какое направление тебя интересует?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_sub_field)

# Шаг 3: подкатегория
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

# Шаг 4: бюджет
def ask_budget(message):
    user_data[message.chat.id]['field'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💚 Бесплатно / стипендия')
    markup.add('💛 До €5,000 в год')
    markup.add('🧡 До €15,000 в год')
    markup.add('❤️ Бюджет не ограничен')
    bot.send_message(message.chat.id, "Какой бюджет на обучение в год?", reply_markup=markup)
    bot.register_next_step_handler(message, show_results)

# Результаты
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

    if not results:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🔍 Подобрать заново')
        bot.send_message(message.chat.id,
            "Не нашла точных совпадений 😔\n\nПопробуй расширить бюджет или выбрать другую специальность.",
            reply_markup=markup)
        return

    response = f"🎯 Нашла {len(results)} вариантов по специальности *{field}*:\n\n"
    for uni in results[:6]:
        rf_status = "✅ Принимают" if uni['rf_ok'] else "⚠️ Уточняй"
        response += (
            f"{uni['flag']} *{uni['name']}* — {uni['country']}\n"
            f"💰 {uni['cost']} · 🎓 {uni['scholarship']}\n"
            f"Граждане РФ: {rf_status}\n\n"
        )

    response += "Хочешь узнать подробнее о каком-то университете? Просто напиши его название!"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔍 Подобрать заново', '📋 Чеклист документов')
    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)

# Чеклист
@bot.message_handler(func=lambda m: m.text == '📋 Чеклист документов')
def checklist(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇩🇪 Германия', '🇳🇱 Нидерланды')
    markup.add('🇨🇦 Канада', '🇷🇸 Сербия')
    markup.add('🇭🇺 Венгрия', '🇨🇿 Чехия')
    markup.add('🇬🇪 Грузия', '🇹🇷 Турция')
    bot.send_message(message.chat.id, "Для какой страны нужен чеклист?", reply_markup=markup)
    bot.register_next_step_handler(message, show_checklist)

def show_checklist(message):
    checklists = {
        '🇩🇪 Германия': "📋 *Документы для Германии:*\n\n✅ Загранпаспорт\n✅ Аттестат + нострификация\n✅ IELTS 6.5+ или TestDaF\n✅ Мотивационное письмо\n✅ 2 рекомендательных письма\n✅ CV / резюме\n✅ Sperrkonto €11,208\n✅ Медицинская страховка\n\n⚠️ Для РФ: подача через uni-assist, срок до 8 недель",
        '🇳🇱 Нидерланды': "📋 *Документы для Нидерландов:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 6.0+\n✅ Мотивационное письмо\n✅ CV / резюме\n✅ Выписка с банковского счёта\n\n⚠️ Подача через Studielink",
        '🇷🇸 Сербия': "📋 *Документы для Сербии:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод на сербский)\n✅ Справка об отсутствии судимости\n✅ Медицинская справка\n\n✅ Виза не нужна для граждан РФ!",
        '🇭🇺 Венгрия': "📋 *Документы для Венгрии:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 5.5+\n✅ Мотивационное письмо\n✅ CV / резюме\n✅ Медицинская справка\n\n🎓 Стипендия Stipendium Hungaricum покрывает всё!",
        '🇨🇿 Чехия': "📋 *Документы для Чехии:*\n\n✅ Загранпаспорт\n✅ Аттестат (нострификация)\n✅ Чешский язык B2 (для бесплатного обучения)\n✅ Мотивационное письмо\n✅ CV / резюме\n\n⚠️ Бесплатно только на чешском языке",
        '🇬🇪 Грузия': "📋 *Документы для Грузии:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод)\n✅ IELTS 5.5+ (для англоязычных программ)\n✅ Мотивационное письмо\n\n✅ Виза не нужна для граждан РФ!",
        '🇹🇷 Турция': "📋 *Документы для Турции:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 6.0+\n✅ Мотивационное письмо\n✅ CV / резюме\n\n🎓 Стипендия Türkiye Scholarships — подай до февраля!",
    }
    text = checklists.get(message.text, "Пока нет чеклиста для этой страны. Скоро добавим!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔍 Подобрать университеты', '📋 Чеклист документов')
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

bot.infinity_polling()
