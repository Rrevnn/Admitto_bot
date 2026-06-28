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
    bot.register_next_step_handler(message, ask_sub_subfield)

def ask_sub_subfield(message):
    sub_field = message.text
    user_data[message.chat.id]['field'] = sub_field
    clean_field = sub_field.split(' ', 1)[1] if ' ' in sub_field else sub_field
    subfields = SUBFIELDS.get(clean_field, [])
    if subfields:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for s in subfields:
            markup.add(s)
        markup.add('➖ Любое направление')
        bot.send_message(message.chat.id,
            f"Уточни направление в рамках {clean_field}:",
            reply_markup=markup)
        bot.register_next_step_handler(message, ask_budget)
    else:
        ask_budget(message)

def ask_budget(message):
    if 'subfield' not in user_data[message.chat.id]:
        user_data[message.chat.id]['subfield'] = message.text
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

def get_missing_requirements(data, budget):
    missing = []
    english = data.get('english', '')
    certificate = data.get('certificate', '')
    passport = data.get('passport', '')
    gpa = data.get('gpa', '')

    if 'A1' in english or 'A2' in english:
        missing.append("📚 Подтяни английский до B2 минимум — большинство программ требуют B2-C1")
    if '➖ Нет' in certificate:
        missing.append("📝 Сдай IELTS или TOEFL — без сертификата не примут в большинство вузов")
    if 'Планирую' in certificate:
        missing.append("⏰ Запишись на IELTS как можно скорее — подготовка занимает 3-6 месяцев")
    if '❌ Нет' in passport:
        missing.append("🛂 Оформи загранпаспорт — без него невозможно подать документы")
    if '⚠️' in passport:
        missing.append("🛂 Продли загранпаспорт — он должен быть действителен минимум 1.5 года")
    if 'Удовл' in gpa:
        missing.append("📊 Подними средний балл — большинство вузов требуют хорошую успеваемость")
    if 'Бесплатно' in budget:
        missing.append("💰 Расширь бюджет или активно ищи стипендии — бесплатных мест мало и конкурс высокий")

    return missing

def show_results(message):
    data = user_data.get(message.chat.id, {})
    citizenship = data.get('citizenship', '')
    field = data.get('field', '')
    budget = message.text
    is_rf = 'Россия' in citizenship
    clean_field = field.split(' ', 1)[1] if ' ' in field else field

    bot.send_message(message.chat.id, "⏳ Ищу подходящие университеты...")

    try:
        UNIVERSITIES = get_universities()
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка загрузки базы университетов. Попробуй позже.")
        return

    results = []
    for uni in UNIVERSITIES:
        if not uni['name']:
            continue
        if is_rf and not uni['rf_ok']:
            continue
        if uni['field'] != clean_field:
            continue
        if 'Бесплатно' in budget and uni['cost'] != 'Бесплатно':
            continue
        results.append(uni)

    name = data.get('name', '')
    profile_type, profile_desc = get_profile_type(data)
    subfield = data.get('subfield', '')

    profile_msg = (
        f"✨ *Твой профиль готов, {name}!*\n\n"
        f"{profile_type}\n"
        f"_{profile_desc}_\n\n"
    )
    bot.send_message(message.chat.id, profile_msg, parse_mode='Markdown')

    if not results:
        missing = get_missing_requirements(data, budget)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🔍 Подобрать заново', '📋 Чеклист документов')

        no_results_msg = (
            f"😔 По твоим критериям не нашла подходящих университетов для *{clean_field}*.\n\n"
        )

        if missing:
            no_results_msg += "📋 *Вот что стоит подготовить:*\n\n"
            for item in missing:
                no_results_msg += f"{item}\n"
            no_results_msg += "\n"

        no_results_msg += (
            "💡 *Попробуй:*\n"
            "— Расширить бюджет\n"
            "— Выбрать другую страну\n"
            "— Рассмотреть смежные специальности\n\n"
            "Нажми *Подобрать заново* чтобы изменить параметры!"
        )

        bot.send_message(message.chat.id, no_results_msg, parse_mode='Markdown', reply_markup=markup)
        return

    subfield_text = f" · {subfield}" if subfield and '➖' not in subfield else ""
    response = f"🎯 *Нашла {len(results)} вариантов — {clean_field}{subfield_text}:*\n\n"
    for uni in results[:6]:
        rf_status = "✅" if uni['rf_ok'] else "⚠️"
        response += (
            f"{uni['flag']} *{uni['name']}* — {uni['country']}\n"
            f"💰 {uni['cost']} · 🎓 {uni['scholarship']} · РФ: {rf_status}\n\n"
        )
    response += (
        "📌 Напиши название университета чтобы узнать подробнее!\n\n"
        "⚠️ _Данные актуальны на 2025 год. Всегда проверяй информацию на официальном сайте._"
    )

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
    try:
        UNIVERSITIES = get_universities()
    except:
        bot.send_message(message.chat.id, "Ошибка загрузки базы. Попробуй позже.")
        return

    found = [u for u in UNIVERSITIES if query in u['name'].lower()]

    if not found:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🔍 Подобрать университеты', '📋 Чеклист документов')
        bot.send_message(message.chat.id,
            "Не нашла такой университет 😔\n\nПроверь название или напиши /start чтобы начать заново.",
            reply_markup=markup)
        return

    uni = found[0]
    rf_status = "✅ Принимают без ограничений" if uni['rf_ok'] else "⚠️ Уточняй на сайте"

    response = (
        f"{uni['flag']} *{uni['name']}*\n"
        f"📍 {uni['country']} · {uni['field']}\n\n"
        f"💰 *Финансы*\n"
        f"Обучение: {uni['cost']}\n"
        f"Стипендия: {uni['scholarship']}\n"
        f"Работа во время учёбы: {uni['work']}\n\n"
        f"📋 *Поступление*\n"
        f"Язык обучения: {uni['language']}\n"
        f"IELTS: {uni['ielts']}\n"
        f"Дедлайн подачи: {uni['deadline']}\n"
        f"Длительность программы: {uni['duration']}\n\n"
        f"⭐ *Сильные стороны программы*\n"
        f"{uni['strengths']}\n\n"
        f"🏠 *Жизнь*\n"
        f"Жильё: {uni['housing']}\n"
        f"СНГ-комьюнити: {uni['community']}\n\n"
        f"🇷🇺 *Для граждан РФ:* {rf_status}\n\n"
        f"⚠️ _Данные актуальны на 2025 год. Проверяй на официальном сайте._\n\n"
        f"📌 Нужен чеклист документов для {uni['country']}?"
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(f"📋 Чеклист для {uni['country']}")
    markup.add('🔍 Подобрать заново')
    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)

bot.infinity_polling()
