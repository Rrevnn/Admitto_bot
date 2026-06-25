
# Admitto Bot — поступление за рубеж для СНГ
# Установи библиотеку: pip install pyTelegramBotAPI

import telebot
from telebot import types
import os

# Твой токен от BotFather
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# База университетов (начальная)
UNIVERSITIES = [
    # IT / Технологии
    {"name": "TU Munich", "country": "Германия", "flag": "🇩🇪", "field": "IT", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD €800/мес"},
    {"name": "TU Berlin", "country": "Германия", "flag": "🇩🇪", "field": "IT", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "KIT Karlsruhe", "country": "Германия", "flag": "🇩🇪", "field": "IT", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "TU Delft", "country": "Нидерланды", "flag": "🇳🇱", "field": "IT", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "Eindhoven University", "country": "Нидерланды", "flag": "🇳🇱", "field": "IT", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "Budapest Tech BME", "country": "Венгрия", "flag": "🇭🇺", "field": "IT", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "KAIST", "country": "Южная Корея", "flag": "🇰🇷", "field": "IT", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "POSTECH", "country": "Южная Корея", "flag": "🇰🇷", "field": "IT", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "Tsinghua University", "country": "Китай", "flag": "🇨🇳", "field": "IT", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "Harbin Institute of Technology", "country": "Китай", "flag": "🇨🇳", "field": "IT", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "Bilkent University", "country": "Турция", "flag": "🇹🇷", "field": "IT", "cost": "$6,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "METU", "country": "Турция", "flag": "🇹🇷", "field": "IT", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Czech Technical University", "country": "Чехия", "flag": "🇨🇿", "field": "IT", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Tartu", "country": "Эстония", "flag": "🇪🇪", "field": "IT", "cost": "€1,660/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Innopolis University", "country": "ОАЭ", "flag": "🇦🇪", "field": "IT", "cost": "$10,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Heriot-Watt Dubai", "country": "ОАЭ", "flag": "🇦🇪", "field": "IT", "cost": "$12,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "University of Ljubljana", "country": "Словения", "flag": "🇸🇮", "field": "IT", "cost": "€3,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Warsaw University of Technology", "country": "Польша", "flag": "🇵🇱", "field": "IT", "cost": "€2,000/год", "rf_ok": True, "scholarship": "Нет"},

    # Естественные науки
    {"name": "Heidelberg University", "country": "Германия", "flag": "🇩🇪", "field": "Науки", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "LMU Munich", "country": "Германия", "flag": "🇩🇪", "field": "Науки", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD"},
    {"name": "University of Vienna", "country": "Австрия", "flag": "🇦🇹", "field": "Науки", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Charles University", "country": "Чехия", "flag": "🇨🇿", "field": "Науки", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest ELTE", "country": "Венгрия", "flag": "🇭🇺", "field": "Науки", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Seoul National University", "country": "Южная Корея", "flag": "🇰🇷", "field": "Науки", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "Peking University", "country": "Китай", "flag": "🇨🇳", "field": "Науки", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "University of Belgrade", "country": "Сербия", "flag": "🇷🇸", "field": "Науки", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Masaryk University", "country": "Чехия", "flag": "🇨🇿", "field": "Науки", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Debrecen", "country": "Венгрия", "flag": "🇭🇺", "field": "Науки", "cost": "€2,000/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Koç University", "country": "Турция", "flag": "🇹🇷", "field": "Науки", "cost": "$5,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "University of Buenos Aires", "country": "Аргентина", "flag": "🇦🇷", "field": "Науки", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Wroclaw", "country": "Польша", "flag": "🇵🇱", "field": "Науки", "cost": "€2,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Tbilisi State University", "country": "Грузия", "flag": "🇬🇪", "field": "Науки", "cost": "€1,200/год", "rf_ok": True, "scholarship": "Нет"},

    # Бизнес / Экономика
    {"name": "University of Belgrade Business", "country": "Сербия", "flag": "🇷🇸", "field": "Бизнес", "cost": "€2,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Bilkent University Business", "country": "Турция", "flag": "🇹🇷", "field": "Бизнес", "cost": "$8,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Heriot-Watt Dubai Business", "country": "ОАЭ", "flag": "🇦🇪", "field": "Бизнес", "cost": "$12,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Corvinus University", "country": "Венгрия", "flag": "🇭🇺", "field": "Бизнес", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Prague University of Economics", "country": "Чехия", "flag": "🇨🇿", "field": "Бизнес", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Koç University Business", "country": "Турция", "flag": "🇹🇷", "field": "Бизнес", "cost": "$9,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "IE University", "country": "Испания", "flag": "🇪🇸", "field": "Бизнес", "cost": "$15,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Tbilisi Free University", "country": "Грузия", "flag": "🇬🇪", "field": "Бизнес", "cost": "€3,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "American University of Armenia", "country": "Армения", "flag": "🇦🇲", "field": "Бизнес", "cost": "$5,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Nazarbayev University", "country": "Казахстан", "flag": "🇰🇿", "field": "Бизнес", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Полная стипендия"},

    # Дизайн / Искусство
    {"name": "Aalto University", "country": "Финляндия", "flag": "🇫🇮", "field": "Дизайн", "cost": "€5,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Design Academy Eindhoven", "country": "Нидерланды", "flag": "🇳🇱", "field": "Дизайн", "cost": "€2,200/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "Bezalel Academy", "country": "Израиль", "flag": "🇮🇱", "field": "Дизайн", "cost": "$8,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Tbilisi Academy of Arts", "country": "Грузия", "flag": "🇬🇪", "field": "Дизайн", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Yildiz Technical University", "country": "Турция", "flag": "🇹🇷", "field": "Дизайн", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Academy of Fine Arts Vienna", "country": "Австрия", "flag": "🇦🇹", "field": "Дизайн", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},

    # Медицина
    {"name": "Charles University Medicine", "country": "Чехия", "flag": "🇨🇿", "field": "Медицина", "cost": "€8,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Debrecen Medicine", "country": "Венгрия", "flag": "🇭🇺", "field": "Медицина", "cost": "€9,000/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Semmelweis University", "country": "Венгрия", "flag": "🇭🇺", "field": "Медицина", "cost": "€9,000/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Tbilisi State Medical University", "country": "Грузия", "flag": "🇬🇪", "field": "Медицина", "cost": "$5,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Ankara University Medicine", "country": "Турция", "flag": "🇹🇷", "field": "Медицина", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Poznan University of Medicine", "country": "Польша", "flag": "🇵🇱", "field": "Медицина", "cost": "€6,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Yerevan State Medical University", "country": "Армения", "flag": "🇦🇲", "field": "Медицина", "cost": "$4,000/год", "rf_ok": True, "scholarship": "Нет"},
]

# Храним данные пользователя во время диалога
user_data = {}

# Команда /start — приветствие
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

# Подбор университетов — шаг 1: гражданство
@bot.message_handler(func=lambda m: m.text == '🔍 Подобрать университеты')
def ask_citizenship(message):
    user_data[message.chat.id] = {}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇷🇺 Россия', '🇰🇿 Казахстан')
    markup.add('🇺🇿 Узбекистан', '🇺🇦 Украина')
    markup.add('🇦🇿 Азербайджан', 'Другое')
    bot.send_message(message.chat.id, "Твоё гражданство?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_field)

# Шаг 2: специальность
def ask_field(message):
    user_data[message.chat.id]['citizenship'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💻 IT / Технологии', '💼 Бизнес / Экономика')
    markup.add('🎨 Дизайн / Искусство', '⚗️ Естественные науки')
    markup.add('⚕️ Медицина', '📚 Другое')
    bot.send_message(message.chat.id, "Какая специальность тебя интересует?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_budget)

# Шаг 3: бюджет
def ask_budget(message):
    field_map = {
        '💻 IT / Технологии': 'IT',
        '💼 Бизнес / Экономика': 'Бизнес',
        '🎨 Дизайн / Искусство': 'Дизайн',
        '⚗️ Естественные науки': 'Науки',
        '⚕️ Медицина': 'Медицина',
    }
    user_data[message.chat.id]['field'] = field_map.get(message.text, 'Любое')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💚 Бесплатно / стипендия')
    markup.add('💛 До €5,000 в год')
    markup.add('🧡 До €15,000 в год')
    markup.add('❤️ Бюджет не ограничен')
    bot.send_message(message.chat.id, "Какой бюджет на обучение в год?", reply_markup=markup)
    bot.register_next_step_handler(message, show_results)

# Показываем результаты
def show_results(message):
    data = user_data.get(message.chat.id, {})
    citizenship = data.get('citizenship', '')
    field = data.get('field', 'Любое')
    budget = message.text

    is_rf = 'Россия' in citizenship
    results = []

    for uni in UNIVERSITIES:
        if is_rf and not uni['rf_ok']:
            continue
        if field != 'Любое' and uni['field'] != field:
            continue
        if 'Бесплатно' in budget and uni['cost'] != 'Бесплатно':
            continue
        results.append(uni)

    if not results:
        bot.send_message(message.chat.id,
            "Не нашла точных совпадений 😔\n\nПопробуй расширить критерии — напиши /start и выбери другие параметры.")
        return

    response = f"🎯 Нашла {len(results)} вариантов для тебя:\n\n"
    for uni in results[:5]:
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

# Чеклист документов
@bot.message_handler(func=lambda m: m.text == '📋 Чеклист документов')
def checklist(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇩🇪 Германия', '🇳🇱 Нидерланды')
    markup.add('🇨🇦 Канада', '🇷🇸 Сербия')
    markup.add('🔙 Назад')
    bot.send_message(message.chat.id, "Для какой страны нужен чеклист?", reply_markup=markup)
    bot.register_next_step_handler(message, show_checklist)

def show_checklist(message):
    checklists = {
        '🇩🇪 Германия': "📋 *Документы для Германии:*\n\n"
                      "✅ Загранпаспорт\n"
                      "✅ Аттестат + нострификация\n"
                      "✅ IELTS 6.5+ или TestDaF\n"
                      "✅ Мотивационное письмо\n"
                      "✅ 2 рекомендательных письма\n"
                      "✅ CV / резюме\n"
                      "✅ Заблокированный счёт Sperrkonto (€11,208)\n"
                      "✅ Медицинская страховка\n\n"
                      "⚠️ Для граждан РФ: подача через uni-assist, срок увеличен до 8 недель",
        '🇳🇱 Нидерланды': "📋 *Документы для Нидерландов:*\n\n"
                        "✅ Загранпаспорт\n"
                        "✅ Аттестат (перевод + апостиль)\n"
                        "✅ IELTS 6.0+\n"
                        "✅ Мотивационное письмо\n"
                        "✅ CV / резюме\n"
                        "✅ Портфолио (для творческих)\n"
                        "✅ Выписка с банковского счёта\n\n"
                        "⚠️ Подача через Studielink",
        '🇷🇸 Сербия': "📋 *Документы для Сербии:*\n\n"
                    "✅ Загранпаспорт\n"
                    "✅ Аттестат (перевод на сербский)\n"
                    "✅ Справка об отсутствии судимости\n"
                    "✅ Медицинская справка\n\n"
                    "✅ Виза не нужна для граждан РФ!",
    }
    text = checklists.get(message.text, "Пока нет чеклиста для этой страны. Напиши /start чтобы начать заново.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔍 Подобрать университеты', '📋 Чеклист документов')
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

# Запускаем бота
bot.infinity_polling()
