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
WAITING_FOR_UNI_SEARCH = set()

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

def analyze_achievements(text):
    text = text.lower()
    results = []

    if any(w in text for w in ['олимпиад', 'олимп']):
        if any(w in text for w in ['международн', 'межд', 'international']):
            results.append("🏆 *Международная олимпиада* — очень сильное достижение! Повышает шансы на стипендии DAAD, Stipendium Hungaricum, GKS. Особенно ценится в TU Munich, Budapest ELTE, KAIST")
        elif any(w in text for w in ['национальн', 'всероссийск', 'республик']):
            results.append("🥇 *Национальная олимпиада* — хорошее достижение для стипендий. Упомяни в мотивационном письме для Германии и Венгрии")
        else:
            results.append("📚 *Олимпиада* — укажи уровень (школьная/национальная/международная) в резюме. Ценится во всех вузах")

    if any(w in text for w in ['волонтёр', 'волонтер', 'доброволец', 'volunteer']):
        results.append("🤝 *Волонтёрство* — сильный плюс для социальных наук, дипломатии, МО. Особенно ценится в Columbia SIPA, университетах Австрии и Нидерландов")

    if any(w in text for w in ['хакатон', 'hackathon', 'хакафон']):
        results.append("💻 *Хакатон* — отличное tech-достижение! Ценится в IT-программах TU Munich, TU Delft, KAIST, эстонских вузах")

    if any(w in text for w in ['публикац', 'статья', 'научн', 'исследован', 'research']):
        results.append("🔬 *Научная публикация/исследование* — очень ценно для PhD и исследовательских программ. Обязательно упомяни в Германии, Великобритании, Южной Корее")

    if any(w in text for w in ['стартап', 'startup', 'бизнес', 'компани', 'основал']):
        results.append("🚀 *Предпринимательский опыт* — выделит тебя в бизнес-школах. Особенно ценится в Koç University, IE University, ОАЭ")

    if any(w in text for w in ['спорт', 'чемпион', 'призёр', 'кмс', 'мастер спорта']):
        results.append("⚽ *Спортивные достижения* — некоторые вузы дают стипендии спортсменам. Укажи в Германии, Венгрии, США")

    if any(w in text for w in ['язык', 'сертификат', 'ielts', 'toefl', 'delf', 'goethe']):
        results.append("🗣️ *Языковой сертификат* — обязательное требование для поступления. Убедись что балл соответствует требованиям вуза")

    if any(w in text for w in ['диплом', 'победитель', 'призёр', 'лауреат', 'конкурс']):
        results.append("🏅 *Победа в конкурсе* — отличное дополнение к портфолио. Упомяни в мотивационном письме")

    if any(w in text for w in ['стипенди', 'грант', 'scholarship']):
        results.append("💰 *Стипендия/грант* — показывает что тебя уже оценили! Очень сильный аргумент для новых стипендий")

    if any(w in text for w in ['проект', 'project', 'разработ', 'создал', 'сделал']):
        results.append("💡 *Проект/разработка* — практический опыт ценится в IT и инженерных вузах. Добавь на GitHub или в портфолио")

    if any(w in text for w in ['работ', 'стажировк', 'intern', 'практик']):
        results.append("💼 *Опыт работы/стажировка* — особенно ценится в магистратуре. Columbia SIPA требует минимум 2 года опыта")

    if not results:
        results.append("📝 Не смогла распознать конкретные достижения. Убедись что упомянула их в мотивационном письме — любой опыт важен!")

    return results

def get_time_to_enroll(data):
    age_or_grade = data.get('age_or_grade', '')
    status = data.get('status', '')
    if '8 класс' in age_or_grade:
        return 'lots', '4+ года'
    elif '9 класс' in age_or_grade:
        return 'lots', '3+ года'
    elif '10 класс' in age_or_grade:
        return 'medium', '2 года'
    elif '11 класс' in age_or_grade:
        return 'urgent', '1 год'
    elif 'Студент' in status:
        return 'medium', '1-3 года'
    elif 'Выпускник' in status or 'Работаю' in status:
        return 'urgent', 'Сейчас'
    return 'medium', '1-2 года'

def get_admission_plan(uni, data):
    country = uni.get('country', '')
    citizenship = data.get('citizenship', '')
    certificate = data.get('certificate', '')
    other_language = data.get('other_language', '')
    scholarship = uni.get('scholarship', '')
    is_rf = 'Россия' in citizenship
    time_type, time_label = get_time_to_enroll(data)

    plan = f"📅 *План поступления в {uni['name']}*\n\n"

    if time_type == 'lots':
        plan += "У тебя много времени — готовься основательно! 🌱\n\n"
        plan += "*Прямо сейчас:*\n"
        plan += "☐ Начни учить английский — цель IELTS 6.5+\n"
        if country in ['Германия', 'Австрия'] and 'Немецкий' not in other_language:
            plan += "☐ Начни учить немецкий — откроет бесплатное обучение\n"
        if country == 'Китай':
            plan += "☐ Начни учить китайский — откроет больше программ\n"
        if country == 'Южная Корея':
            plan += "☐ Начни учить корейский — стипендия GKS\n"
        plan += "☐ Участвуй в олимпиадах — повысит шансы на стипендию\n"
        plan += "☐ Следи за новостями об университете\n\n"
        plan += "*За 2 года:*\n"
        plan += "☐ Сдай IELTS на нужный балл\n"
        if scholarship and 'Нет' not in scholarship:
            plan += f"☐ Изучи условия стипендии {scholarship}\n"
        plan += "☐ Начни писать мотивационное письмо\n\n"
        plan += "*За 1 год:*\n"

    elif time_type == 'medium':
        plan += "Времени достаточно — действуй планомерно! ⚡\n\n"
        plan += "*Прямо сейчас:*\n"
        if '➖ Нет' in certificate or 'Планирую' in certificate:
            plan += "☐ Запишись на IELTS — подготовка 3-6 месяцев\n"
        plan += "☐ Оформи загранпаспорт если нет\n"
        if scholarship and 'Нет' not in scholarship:
            plan += f"☐ Изучи условия стипендии {scholarship}\n"
        plan += "\n*За 6 месяцев:*\n"

    else:
        plan += "Действуй быстро — времени мало! 🔥\n\n"
        plan += "*Срочно:*\n"
        if '➖ Нет' in certificate or 'Планирую' in certificate:
            plan += "☐ СРОЧНО запишись на IELTS!\n"
        plan += "☐ Оформи загранпаспорт если нет\n\n"
        plan += "*В ближайшие месяцы:*\n"

    if country == 'Германия':
        plan += "☐ Начни нострификацию аттестата\n"
        plan += "☐ Напиши мотивационное письмо\n"
        plan += "☐ Попроси 2 рекомендательных письма\n"
        if scholarship and 'DAAD' in scholarship:
            plan += "☐ Подай на стипендию DAAD (дедлайн октябрь)\n"
        if is_rf:
            plan += "\n*Для граждан РФ:*\n"
            plan += "☐ Подача через uni-assist (не напрямую!)\n"
            plan += "☐ Заложи дополнительно 4-8 недель на обработку\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Открыть Sperrkonto €11,208\n"
        plan += "☐ Подать на студенческую визу\n"
        plan += "☐ Записаться в общежитие Studentenwerk\n"
        plan += "☐ Купить медицинскую страховку\n"

    elif country == 'Венгрия':
        plan += "☐ Напиши мотивационное письмо\n"
        plan += "☐ Переведи аттестат + апостиль\n"
        if 'Stipendium' in scholarship:
            plan += "☐ Подай на Stipendium Hungaricum (дедлайн январь)\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Оформить студенческую визу\n"
        plan += "☐ Зарегистрироваться по месту проживания\n"

    elif country == 'Чехия':
        plan += "☐ Нострификация аттестата\n"
        plan += "☐ Напиши мотивационное письмо\n"
        if 'Немецкий' not in other_language:
            plan += "☐ Если хочешь бесплатно — выучи чешский B2\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Оформить студенческую визу\n"
        plan += "☐ Зарегистрироваться в Праге\n"

    elif country == 'Сербия':
        plan += "☐ Перевод аттестата на сербский\n"
        plan += "☐ Справка об отсутствии судимости\n"
        plan += "☐ Медицинская справка\n"
        if is_rf:
            plan += "\n✅ *Для граждан РФ: виза не нужна!*\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Регистрация по месту проживания\n"

    elif country == 'Грузия':
        plan += "☐ Перевод аттестата\n"
        plan += "☐ Напиши мотивационное письмо\n"
        if is_rf:
            plan += "\n✅ *Для граждан РФ: виза не нужна!*\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Регистрация по месту проживания\n"

    elif country == 'Турция':
        plan += "☐ Переведи аттестат + апостиль\n"
        plan += "☐ Напиши мотивационное письмо\n"
        if scholarship and 'Türkiye' in scholarship:
            plan += "☐ Подай на Türkiye Scholarships (дедлайн февраль)\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Оформить студенческую визу\n"

    elif country == 'Китай':
        plan += "☐ Переведи аттестат + апостиль\n"
        plan += "☐ Медицинская справка\n"
        plan += "☐ Напиши мотивационное письмо\n"
        if 'CSC' in scholarship:
            plan += "☐ Подай на стипендию CSC (дедлайн март)\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Студенческая виза X1\n"

    elif country == 'Южная Корея':
        plan += "☐ Переведи аттестат + апостиль\n"
        plan += "☐ Напиши мотивационное письмо\n"
        if 'GKS' in scholarship:
            plan += "☐ Подай на GKS стипендию (дедлайн март)\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Студенческая виза D-2\n"

    elif country == 'Нидерланды':
        plan += "☐ Переведи аттестат + апостиль\n"
        plan += "☐ Напиши мотивационное письмо\n"
        plan += "☐ Подай через Studielink\n"
        if 'Holland' in scholarship:
            plan += "☐ Подай на Holland Scholarship\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Студенческая виза MVV\n"
        plan += "☐ Регистрация в муниципалитете\n"

    elif country == 'Великобритания':
        plan += "☐ Переведи аттестат + апостиль\n"
        plan += "☐ Напиши Personal Statement\n"
        plan += "☐ 2 рекомендательных письма\n"
        if 'Cambridge' in scholarship:
            plan += "☐ Подай на Cambridge Trust\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Студенческая виза Tier 4\n"
        plan += "☐ Оплата Immigration Health Surcharge\n"

    elif country == 'США':
        plan += "☐ Сдай SAT/GRE если нужно\n"
        plan += "☐ Напиши Personal Statement\n"
        plan += "☐ 3 рекомендательных письма\n"
        plan += "☐ Финансовое подтверждение (I-20)\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Студенческая виза F-1\n"

    else:
        plan += "☐ Уточни требования на сайте университета\n"
        plan += "☐ Переведи документы + апостиль\n"
        plan += "☐ Напиши мотивационное письмо\n"
        plan += "\n*После зачисления:*\n"
        plan += "☐ Оформи студенческую визу\n"

    plan += f"\n⚠️ _Дедлайн подачи: {uni['deadline']}_"
    plan += "\n\n✅ Сохрани этот план и отмечай выполненные шаги!"
    return plan

def get_match_reasons(uni, data):
    reasons = []
    country = uni.get('country', '')
    other_language = data.get('other_language', '')
    hobbies = data.get('hobbies', '')
    career = data.get('career', '')
    goal = data.get('goal', '')
    priority = data.get('priority', '')
    achievements = data.get('achievements', '')
    scholarship = uni.get('scholarship', 'Нет')
    community = uni.get('community', '')

    if 'Немецкий' in other_language and country in ['Германия', 'Австрия']:
        reasons.append("🗣️ Знаешь немецкий — можешь учиться бесплатно на местном языке")
    if 'Турецкий' in other_language and country == 'Турция':
        reasons.append("🗣️ Знаешь турецкий — больше программ и возможностей")
    if 'Китайский' in other_language and country == 'Китай':
        reasons.append("🗣️ Знаешь китайский — доступны все программы")
    if 'Корейский' in other_language and country == 'Южная Корея':
        reasons.append("🗣️ Знаешь корейский — доступны все программы")
    if 'Технологии' in hobbies and country in ['Германия', 'Нидерланды', 'Южная Корея']:
        reasons.append("💻 Страна с сильной tech-индустрией — идеально для твоих увлечений")
    if 'Искусство' in hobbies and country in ['Австрия', 'Чехия', 'Грузия']:
        reasons.append("🎨 Богатая культурная среда — вдохновение каждый день")
    if ('IT' in career or 'Стартап' in career) and country in ['Германия', 'Нидерланды', 'Эстония']:
        reasons.append("🚀 Один из лучших рынков для IT-карьеры в Европе")
    if 'Наука' in career and country in ['Германия', 'Великобритания', 'США']:
        reasons.append("🔬 Мировой центр научных исследований")
    if 'Остаться' in goal and country in ['Германия', 'Нидерланды', 'Эстония']:
        reasons.append("🌍 Хорошие возможности для эмиграции после учёбы")
    if 'Вернуться' in goal and country in ['Сербия', 'Грузия', 'Армения']:
        reasons.append("🏠 Близко к дому — легко ездить и принимать родных")
    if scholarship and 'Нет' not in scholarship and ('Международные' in achievements or 'Национальные' in achievements):
        reasons.append(f"🎓 Твои достижения повышают шансы на стипендию {scholarship}")
    if 'Стоимость' in priority and uni.get('cost') == 'Бесплатно':
        reasons.append("💰 Бесплатное обучение — соответствует твоему приоритету")
    if 'Безопасность' in priority and country in ['Германия', 'Австрия', 'Нидерланды']:
        reasons.append("🔒 Одна из самых безопасных стран в мире")
    if 'Большое СНГ' in community or 'Активное СНГ' in community:
        reasons.append("🤝 Большое СНГ-комьюнити — легче адаптироваться")
    if country in ['Сербия', 'Грузия'] and 'Россия' in data.get('citizenship', ''):
        reasons.append("✅ Виза не нужна — проще въезд и меньше бюрократии")
    return reasons

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

    if 'Немецкий' in other_language and country in ['Германия', 'Австрия']:
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
    if 'Технологии' in hobbies and country in ['Германия', 'Нидерланды', 'Южная Корея', 'Эстония']:
        score += 2
    if 'Искусство' in hobbies and country in ['Австрия', 'Чехия', 'Грузия', 'Израиль']:
        score += 2
    if 'Бизнес' in hobbies and country in ['ОАЭ', 'Турция', 'Испания', 'США']:
        score += 2
    if 'Волонтёрство' in hobbies and country in ['Германия', 'Нидерланды', 'Австрия']:
        score += 1
    if 'Спорт' in hobbies and country in ['Германия', 'Нидерланды', 'Венгрия']:
        score += 1
    if ('IT' in career or 'Стартап' in career) and country in ['Германия', 'Нидерланды', 'Эстония', 'Южная Корея']:
        score += 2
    if 'Наука' in career and country in ['Германия', 'Великобритания', 'США', 'Китай']:
        score += 2
    if 'Своё дело' in career and country in ['ОАЭ', 'Турция', 'Эстония']:
        score += 2
    if 'Корпорация' in career and country in ['Германия', 'США', 'Великобритания', 'Нидерланды']:
        score += 2
    if 'Социальные' in career and country in ['Германия', 'Нидерланды', 'Австрия']:
        score += 2
    if 'Остаться' in goal and country in ['Германия', 'Нидерланды', 'Эстония']:
        score += 2
    if 'Вернуться' in goal and country in ['Сербия', 'Грузия', 'Армения', 'Казахстан']:
        score += 1
    if 'Международные' in achievements and scholarship != 'Нет':
        score += 3
    if 'Национальные' in achievements and scholarship != 'Нет':
        score += 2
    if 'Интроверт' in personality and country in ['Германия', 'Чехия', 'Венгрия']:
        score += 1
    if 'Экстраверт' in personality and country in ['Турция', 'ОАЭ', 'Испания', 'США']:
        score += 1
    if 'Рейтинг' in priority and country in ['США', 'Великобритания', 'Германия']:
        score += 2
    if 'Стоимость' in priority and uni.get('cost') == 'Бесплатно':
        score += 3
    if 'Безопасность' in priority and country in ['Германия', 'Австрия', 'Нидерланды', 'Чехия']:
        score += 2
    if 'Трудоустройство' in priority and country in ['Германия', 'США', 'Нидерланды', 'Великобритания']:
        score += 2
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
    WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔍 Подобрать университеты')
    markup.add('🔎 Быстрый поиск')
    markup.add('📋 Чеклист документов')
    bot.send_message(message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я Viamo — твой помощник по поступлению за рубеж.\n\n"
        "Помогу найти университеты под твой профиль, собрать документы и не пропустить дедлайны.\n\n"
        "Что хочешь сделать?",
        reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ['🔍 Подобрать университеты', '🔍 Подобрать заново'])
def ask_name(message):
    user_data[message.chat.id] = {}
    WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
    bot.send_message(message.chat.id, "Отлично! Давай познакомимся 🎯\n\nКак тебя зовут?")
    bot.register_next_step_handler(message, ask_age)

def ask_age(message):
    user_data[message.chat.id]['name'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('До 18', '18–22')
    markup.add('23–27', '28+')
    bot.send_message(message.chat.id, f"Приятно познакомиться, {message.text}! 👋\n\nСколько тебе лет?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_grade_or_status)

def ask_grade_or_status(message):
    user_data[message.chat.id]['age'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'До 18':
        markup.add('8 класс', '9 класс')
        markup.add('10 класс', '11 класс')
        markup.add('Другое')
        bot.send_message(message.chat.id, "В каком классе ты сейчас?", reply_markup=markup)
    else:
        markup.add('🎓 Студент', '📄 Выпускник')
        markup.add('💼 Работаю', 'Другое')
        bot.send_message(message.chat.id, "Кто ты сейчас?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_citizenship)

def ask_citizenship(message):
    user_data[message.chat.id]['age_or_grade'] = message.text
    user_data[message.chat.id]['status'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇷🇺 Россия', '🇰🇿 Казахстан')
    markup.add('🇺🇿 Узбекистан', '🇺🇦 Украина')
    markup.add('🇦🇿 Азербайджан', '🇧🇾 Беларусь')
    markup.add('🇬🇪 Грузия', 'Другое')
    bot.send_message(message.chat.id, "Твоё гражданство?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_gpa)

def ask_gpa(message):
    user_data[message.chat.id]['citizenship'] = message.text
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
    bot.register_next_step_handler(message, ask_achievements_detail)

def ask_achievements_detail(message):
    user_data[message.chat.id]['achievements'] = message.text
    if '➖' in message.text:
        user_data[message.chat.id]['achievements_detail'] = ''
        ask_english(message)
        return
    bot.send_message(message.chat.id,
        "Расскажи подробнее — напиши свои достижения через запятую 📝\n\n"
        "_Например: призёр олимпиады по математике, волонтёр ООН, победитель хакатона_",
        parse_mode='Markdown')
    bot.register_next_step_handler(message, process_achievements_detail)

def process_achievements_detail(message):
    user_data[message.chat.id]['achievements_detail'] = message.text
    analysis = analyze_achievements(message.text)
    response = "🎯 *Анализ твоих достижений:*\n\n"
    for item in analysis:
        response += f"{item}\n\n"
    response += "💡 _Упомяни все достижения в мотивационном письме!_"
    bot.send_message(message.chat.id, response, parse_mode='Markdown')
    ask_english(message)

def ask_english(message):
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
        "Знаешь ли ты другие языки?\n\n💡 Во многих странах можно учиться бесплатно на местном языке!",
        reply_markup=markup)
    bot.register_next_step_handler(message, ask_other_language_level)

def ask_other_language_level(message):
    user_data[message.chat.id]['other_language'] = message.text
    if '➖' in message.text:
        user_data[message.chat.id]['other_language_level'] = 'Нет'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('✅ Есть, действующий')
        markup.add('⚠️ Скоро истечёт')
        markup.add('❌ Нет')
        bot.send_message(message.chat.id, "Загранпаспорт?", reply_markup=markup)
        bot.register_next_step_handler(message, ask_visa)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔴 Начинающий (A1–A2)', '🟡 Средний (B1–B2)')
    markup.add('🟢 Продвинутый (C1)', '⭐ Свободно (C2)')
    bot.send_message(message.chat.id, f"Какой уровень {message.text}?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_passport)

def ask_passport(message):
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
    bot.send_message(message.chat.id, "Почти готово! 🎯\n\nВыбери направление учёбы:", reply_markup=markup)
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
        bot.send_message(message.chat.id, f"Уточни направление в рамках {clean_field}:", reply_markup=markup)
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
    if 'A1' in data.get('english', '') or 'A2' in data.get('english', ''):
        missing.append("📚 Подтяни английский до B2 — большинство программ требуют B2-C1")
    if '➖ Нет' in data.get('certificate', ''):
        missing.append("📝 Сдай IELTS или TOEFL — без сертификата не примут в большинство вузов")
    if 'Планирую' in data.get('certificate', ''):
        missing.append("⏰ Запишись на IELTS — подготовка занимает 3-6 месяцев")
    if '❌ Нет' in data.get('passport', ''):
        missing.append("🛂 Оформи загранпаспорт — без него невозможно подать документы")
    if '⚠️' in data.get('passport', ''):
        missing.append("🛂 Продли загранпаспорт — нужен минимум 1.5 года действия")
    if 'Удовл' in data.get('gpa', ''):
        missing.append("📊 Подними средний балл — вузы требуют хорошую успеваемость")
    if 'Бесплатно' in budget:
        missing.append("💰 Расширь бюджет или активно ищи стипендии")
    return missing

def show_results(message):
    data = user_data.get(message.chat.id, {})
    citizenship = data.get('citizenship', '')
    field = data.get('field', '')
    budget = message.text
    is_rf = 'Россия' in citizenship
    clean_field = field.split(' ', 1)[1] if ' ' in field else field

    bot.send_message(message.chat.id, "⏳ Анализирую твой профиль...")

    try:
        UNIVERSITIES = get_universities()
    except:
        bot.send_message(message.chat.id, "Ошибка загрузки базы. Попробуй позже.")
        return

    results = []
    for uni in UNIVERSITIES:
        if not uni['name']:
            continue
        if is_rf and not uni['rf_ok']:
            continue
        if uni['field'].strip() != clean_field.strip():
            continue
        if 'Бесплатно' in budget and uni['cost'] != 'Бесплатно':
            continue
        uni['score'] = score_university(uni, data)
        results.append(uni)

    results.sort(key=lambda x: x['score'], reverse=True)

    name = data.get('name', '')
    profile_type, profile_desc = get_profile_type(data)
    subfield = data.get('subfield', '')
    time_type, time_label = get_time_to_enroll(data)

    bot.send_message(message.chat.id,
        f"✨ *Твой профиль готов, {name}!*\n\n{profile_type}\n_{profile_desc}_\n\n⏱ До поступления: {time_label}",
        parse_mode='Markdown')

    if not results:
        missing = get_missing_requirements(data, budget)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🔄 Сменить специальность', '🔄 Сменить направление')
        markup.add('💰 Расширить бюджет', '🔍 Начать заново')
        msg = f"😔 Не нашла университетов по *{clean_field}* с твоими критериями.\n\n"
        if missing:
            msg += "📋 *Что стоит подготовить:*\n"
            for item in missing:
                msg += f"{item}\n"
            msg += "\n"
        msg += "Что изменим?"
        bot.send_message(message.chat.id, msg, parse_mode='Markdown', reply_markup=markup)
        WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
        return

    subfield_text = f" · {subfield}" if subfield and '➖' not in subfield else ""
    response = f"🎯 *Топ для тебя — {clean_field}{subfield_text}:*\n\n"
    for uni in results[:6]:
        rf_status = "✅" if uni['rf_ok'] else "⚠️"
        stars = "⭐" * min(uni['score'], 5) if uni['score'] > 0 else ""
        reasons = get_match_reasons(uni, data)
        reason_text = f"\n_{reasons[0]}_" if reasons else ""
        response += f"{uni['flag']} *{uni['name']}* — {uni['country']} {stars}\n💰 {uni['cost']} · 🎓 {uni['scholarship']} · РФ: {rf_status}{reason_text}\n\n"
    response += "📌 Напиши название университета чтобы узнать подробнее!\n\n⚠️ _Данные актуальны на 2025 год._"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔍 Подобрать заново', '📋 Чеклист документов')
    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)
    WAITING_FOR_UNI_SEARCH.add(message.chat.id)

@bot.message_handler(func=lambda m: m.text == '🔄 Сменить специальность')
def change_speciality(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for field in FIELDS.keys():
        markup.add(field)
    bot.send_message(message.chat.id, "Выбери новое направление:", reply_markup=markup)
    bot.register_next_step_handler(message, ask_sub_field)

@bot.message_handler(func=lambda m: m.text == '🔄 Сменить направление')
def change_direction(message):
    main_field = user_data.get(message.chat.id, {}).get('main_field', '')
    if main_field and main_field in FIELDS:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for sub in FIELDS[main_field]:
            markup.add(sub)
        bot.send_message(message.chat.id, "Выбери другое направление:", reply_markup=markup)
        bot.register_next_step_handler(message, ask_sub_subfield)
    else:
        change_speciality(message)

@bot.message_handler(func=lambda m: m.text == '💰 Расширить бюджет')
def expand_budget(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💛 До €5,000 в год')
    markup.add('🧡 До €15,000 в год')
    markup.add('❤️ Бюджет не ограничен')
    bot.send_message(message.chat.id, "Выбери новый бюджет:", reply_markup=markup)
    bot.register_next_step_handler(message, show_results)

@bot.message_handler(func=lambda m: m.text == '🔎 Быстрый поиск')
def quick_search(message):
    WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('📚 По направлению', '🌍 По стране')
    markup.add('💰 Бесплатные', '🎓 Со стипендией')
    markup.add('🔙 Назад')
    bot.send_message(message.chat.id, "Как хочешь искать?", reply_markup=markup)
    bot.register_next_step_handler(message, quick_search_filter)

def quick_search_filter(message):
    if message.text == '📚 По направлению':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for field in FIELDS.keys():
            markup.add(field)
        bot.send_message(message.chat.id, "Выбери направление:", reply_markup=markup)
        bot.register_next_step_handler(message, quick_search_by_field)
    elif message.text == '🌍 По стране':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🇩🇪 Германия', '🇳🇱 Нидерланды')
        markup.add('🇭🇺 Венгрия', '🇨🇿 Чехия')
        markup.add('🇷🇸 Сербия', '🇬🇪 Грузия')
        markup.add('🇹🇷 Турция', '🇨🇳 Китай')
        markup.add('🇰🇷 Южная Корея', '🇺🇸 США')
        markup.add('🇬🇧 Великобритания', '🇦🇲 Армения')
        bot.send_message(message.chat.id, "Выбери страну:", reply_markup=markup)
        bot.register_next_step_handler(message, quick_search_by_country)
    elif message.text == '💰 Бесплатные':
        quick_show_filtered(message.chat.id, message, cost_filter='Бесплатно')
    elif message.text == '🎓 Со стипендией':
        quick_show_filtered(message.chat.id, message, scholarship_filter=True)
    else:
        start(message)

def quick_search_by_field(message):
    main_field = message.text
    if main_field not in FIELDS:
        start(message)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for sub in FIELDS[main_field]:
        markup.add(sub)
    markup.add('➖ Все специальности')
    bot.send_message(message.chat.id, "Уточни специальность:", reply_markup=markup)
    bot.register_next_step_handler(message, lambda m: quick_show_filtered(
        message.chat.id, m,
        field_filter=m.text if '➖' not in m.text else None,
        main_field=main_field
    ))

def quick_search_by_country(message):
    country = message.text.split(' ', 1)[1] if ' ' in message.text else message.text
    quick_show_filtered(message.chat.id, message, country_filter=country)

def quick_show_filtered(chat_id, message, field_filter=None, main_field=None, country_filter=None, cost_filter=None, scholarship_filter=False):
    try:
        UNIVERSITIES = get_universities()
    except:
        bot.send_message(chat_id, "Ошибка загрузки базы. Попробуй позже.")
        return

    results = []
    for uni in UNIVERSITIES:
        if not uni['name']:
            continue
        if field_filter and uni['field'].strip() != field_filter.strip():
            continue
        if main_field and not field_filter:
            subs = FIELDS.get(main_field, [])
            if uni['field'] not in subs:
                continue
        if country_filter and country_filter not in uni['country']:
            continue
        if cost_filter and uni['cost'] != cost_filter:
            continue
        if scholarship_filter and (not uni['scholarship'] or uni['scholarship'] == 'Нет'):
            continue
        results.append(uni)

    if not results:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🔎 Быстрый поиск', '🔍 Подобрать университеты')
        bot.send_message(chat_id, "Не нашла университетов по этим критериям 😔", reply_markup=markup)
        return

    response = f"🎓 *Найдено {len(results)} университетов:*\n\n"
    for uni in results[:8]:
        rf_status = "✅" if uni['rf_ok'] else "⚠️"
        response += f"{uni['flag']} *{uni['name']}* — {uni['country']}\n💰 {uni['cost']} · {uni['field']} · РФ: {rf_status}\n\n"
    if len(results) > 8:
        response += f"_...и ещё {len(results) - 8}. Используй подбор по анкете для точных результатов._\n\n"
    response += "📌 Напиши название университета чтобы узнать подробнее!"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔎 Быстрый поиск', '🔍 Подобрать университеты')
    bot.send_message(chat_id, response, parse_mode='Markdown', reply_markup=markup)
    WAITING_FOR_UNI_SEARCH.add(chat_id)

@bot.message_handler(func=lambda m: m.text == '📋 Чеклист документов')
def checklist(message):
    WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🇩🇪 Германия', '🇳🇱 Нидерланды')
    markup.add('🇭🇺 Венгрия', '🇨🇿 Чехия')
    markup.add('🇷🇸 Сербия', '🇬🇪 Грузия')
    markup.add('🇹🇷 Турция', '🇨🇳 Китай')
    bot.send_message(message.chat.id, "Для какой страны нужен чеклист?", reply_markup=markup)
    bot.register_next_step_handler(message, show_checklist)

def show_checklist(message):
    checklists = {
        '🇩🇪 Германия': "📋 *Германия:*\n\n✅ Загранпаспорт\n✅ Аттестат + нострификация\n✅ IELTS 6.5+ или TestDaF\n✅ Мотивационное письмо\n✅ 2 рекомендательных письма\n✅ CV\n✅ Sperrkonto €11,208\n✅ Страховка\n\n⚠️ Для РФ: через uni-assist, срок до 8 недель",
        '🇳🇱 Нидерланды': "📋 *Нидерланды:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 6.0+\n✅ Мотивационное письмо\n✅ CV\n✅ Выписка с банковского счёта\n\n⚠️ Подача через Studielink",
        '🇭🇺 Венгрия': "📋 *Венгрия:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 5.5+\n✅ Мотивационное письмо\n✅ CV\n✅ Медицинская справка\n\n🎓 Stipendium Hungaricum покрывает всё!",
        '🇨🇿 Чехия': "📋 *Чехия:*\n\n✅ Загранпаспорт\n✅ Аттестат (нострификация)\n✅ Чешский B2 (для бесплатного)\n✅ Мотивационное письмо\n✅ CV\n\n⚠️ Бесплатно только на чешском",
        '🇷🇸 Сербия': "📋 *Сербия:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод на сербский)\n✅ Справка об отсутствии судимости\n✅ Медицинская справка\n\n✅ Виза не нужна для РФ!",
        '🇬🇪 Грузия': "📋 *Грузия:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод)\n✅ IELTS 5.5+\n✅ Мотивационное письмо\n\n✅ Виза не нужна для РФ!",
        '🇹🇷 Турция': "📋 *Турция:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 6.0+\n✅ Мотивационное письмо\n✅ CV\n\n🎓 Türkiye Scholarships — подай до февраля!",
        '🇨🇳 Китай': "📋 *Китай:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ Медицинская справка\n✅ Мотивационное письмо\n✅ CV\n\n🎓 CSC стипендия покрывает всё!",
    }
    text = checklists.get(message.text, "Пока нет чеклиста для этой страны. Скоро добавим!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔍 Подобрать университеты', '📋 Чеклист документов')
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and m.text.startswith('📅 План поступления'))
def show_admission_plan(message):
    data = user_data.get(message.chat.id, {})
    uni = data.get('last_uni')
    if not uni:
        bot.send_message(message.chat.id, "Сначала выбери университет из списка!")
        return
    plan = get_admission_plan(uni, data)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🔍 Подобрать заново', '📋 Чеклист документов')
    bot.send_message(message.chat.id, plan, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda m: m.chat.id in WAITING_FOR_UNI_SEARCH)
def handle_university_search(message):
    if message.text.startswith('/'):
        return
    skip = ['🔍 Подобрать университеты', '🔍 Подобрать заново', '📋 Чеклист документов',
            '🔎 Быстрый поиск', '🔄 Сменить специальность', '🔄 Сменить направление',
            '💰 Расширить бюджет', '🔍 Начать заново', '🔙 Назад']
    if message.text in skip or message.text.startswith('📅') or message.text.startswith('📋 Чеклист для'):
        return

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
        bot.send_message(message.chat.id, "Не нашла такой университет 😔\n\nПроверь название или напиши /start.", reply_markup=markup)
        return

    uni = found[0]
    rf_status = "✅ Принимают" if uni['rf_ok'] else "⚠️ Уточняй на сайте"
    data = user_data.get(message.chat.id, {})
    reasons = get_match_reasons(uni, data)

    response = (
        f"{uni['flag']} *{uni['name']}*\n"
        f"📍 {uni['country']} · {uni['field']}\n\n"
        f"💰 *Финансы*\n"
        f"Обучение: {uni['cost']}\n"
        f"Стипендия: {uni['scholarship']}\n"
        f"Работа: {uni['work']}\n\n"
        f"📋 *Поступление*\n"
        f"Язык обучения: {uni['language']}\n"
        f"IELTS: {uni['ielts']}\n"
        f"Дедлайн: {uni['deadline']}\n"
        f"Длительность: {uni['duration']}\n\n"
        f"⭐ *Сильные стороны*\n"
        f"{uni['strengths']}\n\n"
        f"🏠 *Жизнь*\n"
        f"Жильё: {uni['housing']}\n"
        f"СНГ-комьюнити: {uni['community']}\n\n"
        f"🇷🇺 *Для граждан РФ:* {rf_status}\n"
    )

    if reasons:
        response += "\n🎯 *Почему подходит тебе:*\n"
        for r in reasons[:3]:
            response += f"• {r}\n"

    response += "\n⚠️ _Данные актуальны на 2025 год._"

    uni_name_short = uni['name'][:20]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(f"📅 План поступления в {uni_name_short}")
    markup.add(f"📋 Чеклист для {uni['country']}")
    markup.add('🔍 Подобрать заново')

    user_data[message.chat.id]['last_uni'] = uni
    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)

bot.infinity_polling()
