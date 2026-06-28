import telebot
from telebot import types
import os
import requests

TOKEN = os.environ.get('BOT_TOKEN')
AIRTABLE_TOKEN = os.environ.get('AIRTABLE_TOKEN')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID')
AIRTABLE_TABLE = 'Universities'

bot = telebot.TeleBot(TOKEN)
user_data = {}

def get_universities():
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE}"
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}
    all_records = []
    offset = None
    while True:
        params = {"pageSize": 100}
        if offset:
            params["offset"] = offset
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        records = data.get("records", [])
        for record in records:
            fields = record.get("fields", {})
            all_records.append({
                "name": fields.get("name", ""),
                "country": fields.get("country", ""),
                "flag": fields.get("flag", ""),
                "field": fields.get("field", ""),
                "cost": fields.get("cost", "Уточняй на сайте"),
                "rf_ok": fields.get("rf_ok", False),
                "scholarship": fields.get("scholarship", "Нет"),
                "ielts": fields.get("ielts", "Уточняй на сайте"),
                "deadline": fields.get("deadline", "Уточняй на сайте"),
                "duration": fields.get("duration", "Уточняй на сайте"),
                "housing": fields.get("housing", "Уточняй на сайте"),
                "community": fields.get("community", "Уточняй на сайте"),
                "strengths": fields.get("strengths", "Уточняй на официальном сайте"),
                "work": fields.get("work", "До 20 часов в неделю"),
                "language": fields.get("language", "Уточняй на сайте"),
            })
        offset = data.get("offset")
        if not offset:
            break
    return all_records

def score_university(uni, data):
    score = 0
    hobbies = data.get('hobbies', '')
    personality = data.get('personality', '')
    career = data.get('career', '')
    goal = data.get('goal', '')
    other_language = data.get('other_language', '')
    achievements = data.get('achievements', '')
    priority = data.get('priority', '')
    country = uni.get('country', '')
    community = uni.get('community', '')
    scholarship = uni.get('scholarship', 'Нет')

    # Язык → бонус за знание местного языка
    if 'Немецкий' in other_language and country == 'Германия':
        score += 3
    if 'Немецкий' in other_language and country == 'Австрия':
        score += 3
    if 'Турецкий' in other_language and country == 'Турция':
        score += 3
    if 'Китайский' in other_language and country == 'Китай':
        score += 3
    if 'Корейский' in other_language and country == 'Южная Корея':
        score += 3
    if 'Сербский' in other_language and country == 'Сербия':
        score += 3
    if 'Чешский' in other_language and country == 'Чехия':
        score += 3
    if 'Венгерский' in other_language and country == 'Венгрия':
        score += 3

    # Увлечения → рекомендации стран
    if 'Технологии' in hobbies and country in ['Германия', 'Нидерланды', 'Южная Корея', 'Эстония']:
        score += 2
    if 'Искусство' in hobbies and country in ['Австрия', 'Чехия', 'Грузия', 'Израиль']:
        score += 2
    if 'Бизнес' in hobbies and country in ['ОАЭ', 'Турция', 'Испания', 'США']:
        score += 2
    if 'Путешествия' in hobbies and country in ['Нидерланды', 'Германия', 'Великобритания']:
        score += 1
    if 'Волонтёрство' in hobbies and country in ['Германия', 'Нидерланды', 'Австрия']:
        score += 1
    if 'Спорт' in hobbies and country in ['Германия', 'Нидерланды', 'Венгрия']:
        score += 1

    # Карьерная цель → страны
    if 'IT' in career or 'Стартап' in career:
        if country in ['Германия', 'Нидерланды', 'Эстония', 'Южная Корея']:
            score += 2
    if 'Наука' in career:
        if country in ['Германия', 'Великобритания', 'США', 'Китай']:
            score += 2
    if 'Своё дело' in career:
        if country in ['ОАЭ', 'Турция', 'Эстония']:
            score += 2
    if 'Корпорация' in career:
        if country in ['Германия', 'США', 'Великобритания', 'Нидерланды']:
            score += 2
    if 'Социальные' in career:
        if country in ['Германия', 'Нидерланды', 'Австрия']:
            score += 2

    # Цель после учёбы → страны с хорошей иммиграцией
    if 'Остаться' in goal:
        if country in ['Германия', 'Канада', 'Нидерланды', 'Эстония']:
            score += 2
    if 'Вернуться' in goal:
        if country in ['Сербия', 'Грузия', 'Армения', 'Казахстан']:
            score += 1

    # Достижения → стипендии
    if 'Международные' in achievements:
        if scholarship != 'Нет' and 'Нет' not in scholarship:
            score += 3
    if 'Национальные' in achievements:
        if scholarship != 'Нет' and 'Нет' not in scholarship:
            score += 2

    # Личность → тип университета
    if 'Интроверт' in personality:
        if country in ['Германия', 'Чехия', 'Венгрия']:
            score += 1
    if 'Экстраверт' in personality:
        if country in ['Турция', 'ОАЭ', 'Испания', 'США']:
            score += 1

    # Приоритет при выборе
    if 'Рейтинг' in priority:
        if country in ['США', 'Великобритания', 'Германия']:
            score += 2
    if 'Стоимость' in priority:
        if uni.get('cost') == 'Бесплатно':
            score += 3
    if 'Безопасность' in priority:
        if country in ['Германия', 'Австрия', 'Нидерланды', 'Чехия']:
            score += 2
    if 'Трудоустройство' in priority:
        if country in ['Германия', 'США', 'Нидерланды', 'Великобритания']:
            score += 2

    # СНГ-комьюнити бонус
    if 'Большое СНГ' in community or 'Активное СНГ' in community:
        score += 1

    return score

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

SUBFIELDS = {
    "Разработка": ["📱 Мобильная разработка", "🌐 Веб-разработка", "🎮 Gamedev", "☁️ Облачные системы", "🔧 Встраиваемые системы"],
    "Data Science": ["📊 Анализ данных", "🤖 Машинное обучение", "📈 Бизнес-аналитика", "🔬 Научные данные"],
    "AI / Machine Learning": ["🧠 Нейросети", "👁️ Компьютерное зрение", "🗣️ Обработка языка", "🤖 Робототехника и AI"],
    "Кибербезопасность": ["🛡️ Защита сетей", "🔐 Криптография", "🕵️ Этичный хакинг", "☁️ Безопасность облака"],
    "Робототехника": ["🦾 Промышленные роботы", "🚗 Автономные системы", "🏥 Медицинская робототехника"],
    "Физика": ["⚛️ Ядерная физика", "🌌 Астрофизика", "💡 Оптика и фотоника", "🔬 Физика материалов"],
    "Химия": ["💊 Фармацевтическая химия", "🌿 Органическая химия", "⚗️ Аналитическая химия", "🏭 Промышленная химия"],
    "Биология": ["🧬 Молекулярная биология", "🌿 Экология", "🦠 Микробиология", "🧪 Биотехнологии"],
    "Экология": ["🌍 Охрана окружающей среды", "♻️ Устойчивое развитие", "🌊 Морская экология"],
    "Математика": ["📐 Чистая математика", "💻 Вычислительная математика", "📊 Статистика", "🔐 Криптография"],
    "Астрономия": ["🌌 Астрофизика", "🔭 Наблюдательная астрономия", "🛸 Планетология", "☀️ Гелиофизика"],
    "Менеджмент": ["🌍 Международный менеджмент", "💼 Управление проектами", "🏢 Корпоративное управление"],
    "Финансы": ["📈 Инвестиции и рынки", "🏦 Банковское дело", "💰 Корпоративные финансы", "📊 Финтех"],
    "Маркетинг": ["📱 Digital-маркетинг", "🎯 Бренд-менеджмент", "🔍 Аналитика и данные"],
    "Предпринимательство": ["🚀 Стартапы", "💡 Инновации", "🌍 Социальное предпринимательство"],
    "Логистика": ["🚢 Международная логистика", "🏭 Управление цепочками поставок", "✈️ Авиалогистика"],
    "Общая медицина": ["🧬 Научная / исследовательская", "👨‍⚕️ Клиническая практика", "🌍 Глобальная медицина", "🧠 Нейрология"],
    "Стоматология": ["🦷 Общая стоматология", "🏥 Хирургическая стоматология", "👶 Детская стоматология"],
    "Фармацевтика": ["💊 Клиническая фармация", "🔬 Фармацевтические исследования", "🏭 Промышленная фармация"],
    "Психология": ["🧠 Клиническая психология", "💼 Организационная психология", "🔬 Нейропсихология"],
    "Ветеринария": ["🐾 Мелкие животные", "🐄 Крупные животные", "🔬 Ветеринарные исследования"],
    "Графический дизайн": ["🎨 Визуальная коммуникация", "📦 Брендинг и упаковка", "🎬 Моушн-дизайн"],
    "UX/UI": ["📱 Мобильный дизайн", "🌐 Веб-дизайн", "🔬 UX-исследования", "🎮 Игровой интерфейс"],
    "Архитектура": ["🏙️ Современная и городская среда", "🏛️ Историческая и реставрация", "🌿 Эко-архитектура", "💻 Параметрическая / цифровая", "🎨 Архитектура и искусство"],
    "Мода": ["👗 Дизайн одежды", "♻️ Устойчивая мода", "🏢 Управление модным брендом"],
    "Анимация": ["🎬 2D анимация", "🎮 3D и геймдев", "🎭 Стоп-моушн", "✨ Спецэффекты"],
    "Фотография": ["📸 Документальная", "🎨 Художественная", "📰 Фотожурналистика", "💼 Коммерческая"],
    "Журналистика": ["📰 Печатная журналистика", "📺 ТВ и видео", "🌐 Digital-медиа", "🔍 Расследовательская"],
    "Дипломатия": ["🌍 Международные отношения", "🤝 Переговоры и медиация", "🏛️ Публичная дипломатия"],
    "Политология": ["🗳️ Сравнительная политика", "🌍 Международная политика", "📊 Политический анализ"],
    "Социология": ["🔬 Социальные исследования", "🏙️ Городская социология", "📊 Количественные методы"],
    "Международные отношения": ["🌍 Глобальная политика", "💼 Международная торговля", "☮️ Миротворчество"],
    "Право": ["⚖️ Международное право", "💼 Корпоративное право", "🌍 Права человека", "🔍 Уголовное право"],
    "История": ["🏛️ Древняя история", "🌍 Современная история", "📜 Архивное дело"],
    "Философия": ["🧠 Аналитическая философия", "🌍 Политическая философия", "⚖️ Этика"],
    "Лингвистика": ["🗣️ Прикладная лингвистика", "💻 Компьютерная лингвистика", "🌍 Социолингвистика"],
    "Культурология": ["🎭 Культура и медиа", "🌍 Межкультурная коммуникация", "🏛️ Культурное наследие"],
    "Антропология": ["🌍 Культурная антропология", "🦴 Физическая антропология", "🔬 Археология"],
    "Машиностроение": ["🚗 Автомобильная инженерия", "✈️ Аэрокосмическая", "🏭 Промышленная", "🤖 Мехатроника"],
    "Электроника": ["💡 Силовая электроника", "📡 Телекоммуникации", "🔌 Встраиваемые системы"],
    "Строительство": ["🏗️ Гражданское строительство", "🌉 Мосты и конструкции", "🌿 Зелёное строительство"],
    "Энергетика": ["☀️ Возобновляемая энергия", "⚡ Энергосистемы", "💨 Ветроэнергетика"],
    "Авиация": ["✈️ Аэронавтика", "🚀 Космические системы", "🛸 Беспилотники"],
    "Педагогика": ["👶 Дошкольное образование", "🏫 Школьное образование", "🌍 Международное образование"],
    "Психология образования": ["🧠 Когнитивное развитие", "📊 Образовательные исследования"],
    "Специальное образование": ["♿ Инклюзивное образование", "🧩 Работа с особыми потребностями"],
}

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
    bot.register_next_step_handler(message, ask_other_language)

def ask_other_language(message):
    user_data[message.chat.id]['certificate'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇩🇪 Немецкий', '🇫🇷 Французский')
    markup.add('🇹🇷 Турецкий', '🇨🇳 Китайский')
    markup.add('🇰🇷 Корейский', '🇷🇸 Сербский')
    markup.add('🇨🇿 Чешский', '🇭🇺 Венгерский')
    markup.add('➖ Только английский / русский')
    bot.send_message(message.chat.id,
        "Знаешь ли ты другие языки?\n\n"
        "💡 Во многих странах можно учиться бесплатно на местном языке!",
        reply_markup=markup)
    bot.register_next_step_handler(message, ask_other_language_level)

def ask_other_language_level(message):
    user_data[message.chat.id]['other_language'] = message.text
    if '➖' in message.text:
        ask_passport(message)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔴 Начинающий (A1–A2)', '🟡 Средний (B1–B2)')
    markup.add('🟢 Продвинутый (C1)', '⭐ Свободно (C2)')
    bot.send_message(message.chat.id, f"Какой уровень {message.text}?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_passport)

def ask_passport(message):
    if 'other_language_level' not in user_data[message.chat.id]:
        user_data[message.chat.id]['other_language_level'] = message.text
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
