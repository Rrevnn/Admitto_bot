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
    {"name": "University of Amsterdam", "country": "Нидерланды", "flag": "🇳🇱", "field": "Data Science", "cost": "€2,314/год", "rf_ok": True, "scholarship": "Holland Scholarship"},
    {"name": "Budapest Tech BME DS", "country": "Венгрия", "flag": "🇭🇺", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Charles University DS", "country": "Чехия", "flag": "🇨🇿", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Vienna DS", "country": "Австрия", "flag": "🇦🇹", "field": "Data Science", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Bilkent University DS", "country": "Турция", "flag": "🇹🇷", "field": "Data Science", "cost": "$5,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Tsinghua University DS", "country": "Китай", "flag": "🇨🇳", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "KAIST DS", "country": "Южная Корея", "flag": "🇰🇷", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "Tbilisi State University DS", "country": "Грузия", "flag": "🇬🇪", "field": "Data Science", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Belgrade DS", "country": "Сербия", "flag": "🇷🇸", "field": "Data Science", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Nazarbayev University DS", "country": "Казахстан", "flag": "🇰🇿", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Полная стипендия"},
    {"name": "TU Vienna Architecture", "country": "Австрия", "flag": "🇦🇹", "field": "Архитектура", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Charles University Architecture", "country": "Чехия", "flag": "🇨🇿", "field": "Архитектура", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest University of Technology", "country": "Венгрия", "flag": "🇭🇺", "field": "Архитектура", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "University of Belgrade Architecture", "country": "Сербия", "flag": "🇷🇸", "field": "Архитектура", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Istanbul Technical University", "country": "Турция", "flag": "🇹🇷", "field": "Архитектура", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Tbilisi Academy of Architecture", "country": "Грузия", "flag": "🇬🇪", "field": "Архитектура", "cost": "€1,200/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Warsaw University of Technology Architecture", "country": "Польша", "flag": "🇵🇱", "field": "Архитектура", "cost": "€2,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Corvinus University Diplomacy", "country": "Венгрия", "flag": "🇭🇺", "field": "Дипломатия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Charles University IR", "country": "Чехия", "flag": "🇨🇿", "field": "Дипломатия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Vienna IR", "country": "Австрия", "flag": "🇦🇹", "field": "Дипломатия", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Bilkent University IR", "country": "Турция", "flag": "🇹🇷", "field": "Дипломатия", "cost": "$6,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "University of Belgrade IR", "country": "Сербия", "flag": "🇷🇸", "field": "Дипломатия", "cost": "€1,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Peking University IR", "country": "Китай", "flag": "🇨🇳", "field": "Дипломатия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "Budapest ELTE IR", "country": "Венгрия", "flag": "🇭🇺", "field": "Международные отношения", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Charles University MO", "country": "Чехия", "flag": "🇨🇿", "field": "Международные отношения", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "University of Vienna MO", "country": "Австрия", "flag": "🇦🇹", "field": "Международные отношения", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Tbilisi State University MO", "country": "Грузия", "flag": "🇬🇪", "field": "Международные отношения", "cost": "€1,200/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Bilkent University MO", "country": "Турция", "flag": "🇹🇷", "field": "Международные отношения", "cost": "$6,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Seoul National University IR", "country": "Южная Корея", "flag": "🇰🇷", "field": "Международные отношения", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "Peking University MO", "country": "Китай", "flag": "🇨🇳", "field": "Международные отношения", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Разработка", "cost": "$57,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Data Science", "cost": "$57,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "AI / Machine Learning", "cost": "$57,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Робототехника", "cost": "$57,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Кибербезопасность", "cost": "$57,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Физика", "cost": "$57,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Математика", "cost": "$57,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Машиностроение", "cost": "$57,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Авиация", "cost": "$57,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Архитектура", "cost": "$57,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Columbia University", "country": "США", "flag": "🇺🇸", "field": "Международные отношения", "cost": "$63,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Columbia University", "country": "США", "flag": "🇺🇸", "field": "Дипломатия", "cost": "$63,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "University of Vienna Education", "country": "Австрия", "flag": "🇦🇹", "field": "Педагогика", "cost": "€1,500/год", "rf_ok": True, "scholarship": "OeAD стипендия"},
    {"name": "Charles University Education", "country": "Чехия", "flag": "🇨🇿", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest ELTE Education", "country": "Венгрия", "flag": "🇭🇺", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "University of Belgrade Education", "country": "Сербия", "flag": "🇷🇸", "field": "Педагогика", "cost": "€1,200/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Tbilisi State University Education", "country": "Грузия", "flag": "🇬🇪", "field": "Педагогика", "cost": "€1,000/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Ankara University Education", "country": "Турция", "flag": "🇹🇷", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Koç University Education", "country": "Турция", "flag": "🇹🇷", "field": "Педагогика", "cost": "$5,000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Peking University Education", "country": "Китай", "flag": "🇨🇳", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "Seoul National University Education", "country": "Южная Корея", "flag": "🇰🇷", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "Nazarbayev University Education", "country": "Казахстан", "flag": "🇰🇿", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Полная стипендия"},
    {"name": "Prague College", "country": "Чехия", "flag": "🇨🇿", "field": "Графический дизайн", "cost": "€4,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest Metropolitan University", "country": "Венгрия", "flag": "🇭🇺", "field": "Графический дизайн", "cost": "€3,500/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Tbilisi State Academy of Arts", "country": "Грузия", "flag": "🇬🇪", "field": "Графический дизайн", "cost": "€1,200/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Mimar Sinan Fine Arts University", "country": "Турция", "flag": "🇹🇷", "field": "Графический дизайн", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Seoul National University Design", "country": "Южная Корея", "flag": "🇰🇷", "field": "Графический дизайн", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "Tsinghua University Design", "country": "Китай", "flag": "🇨🇳", "field": "Графический дизайн", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "Budapest Metropolitan University UX", "country": "Венгрия", "flag": "🇭🇺", "field": "UX/UI", "cost": "€3,500/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Czech Technical University UX", "country": "Чехия", "flag": "🇨🇿", "field": "UX/UI", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Aalto University UX", "country": "Финляндия", "flag": "🇫🇮", "field": "UX/UI", "cost": "€5,000/год", "rf_ok": True, "scholarship": "Частичные гранты"},
    {"name": "Mimar Sinan Fine Arts University UX", "country": "Турция", "flag": "🇹🇷", "field": "UX/UI", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "KAIST Design", "country": "Южная Корея", "flag": "🇰🇷", "field": "UX/UI", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "Prague College Fashion", "country": "Чехия", "flag": "🇨🇿", "field": "Мода", "cost": "€4,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest Metropolitan University Fashion", "country": "Венгрия", "flag": "🇭🇺", "field": "Мода", "cost": "€3,500/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Mimar Sinan Fine Arts University Fashion", "country": "Турция", "flag": "🇹🇷", "field": "Мода", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Yildiz Technical University Fashion", "country": "Турция", "flag": "🇹🇷", "field": "Мода", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Tsinghua University Fashion", "country": "Китай", "flag": "🇨🇳", "field": "Мода", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "Prague College Animation", "country": "Чехия", "flag": "🇨🇿", "field": "Анимация", "cost": "€4,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest Metropolitan University Animation", "country": "Венгрия", "flag": "🇭🇺", "field": "Анимация", "cost": "€3,500/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Mimar Sinan Fine Arts University Animation", "country": "Турция", "flag": "🇹🇷", "field": "Анимация", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "KAIST Animation", "country": "Южная Корея", "flag": "🇰🇷", "field": "Анимация", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "Tsinghua University Animation", "country": "Китай", "flag": "🇨🇳", "field": "Анимация", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия"},
    {"name": "Prague College Photography", "country": "Чехия", "flag": "🇨🇿", "field": "Фотография", "cost": "€4,500/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Budapest Metropolitan University Photography", "country": "Венгрия", "flag": "🇭🇺", "field": "Фотография", "cost": "€3,500/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum"},
    {"name": "Tbilisi State Academy of Arts Photography", "country": "Грузия", "flag": "🇬🇪", "field": "Фотография", "cost": "€1,200/год", "rf_ok": True, "scholarship": "Нет"},
    {"name": "Mimar Sinan Fine Arts University Photography", "country": "Турция", "flag": "🇹🇷", "field": "Фотография", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships"},
    {"name": "Seoul National University Photography", "country": "Южная Корея", "flag": "🇰🇷", "field": "Фотография", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Разработка", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Data Science", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "AI / Machine Learning", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Физика", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Математика", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Химия", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Биология", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Машиностроение", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Архитектура", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Право", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Международные отношения", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Политология", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Психология", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "История", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Философия", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Лингвистика", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Педагогика", "cost": "£35,000/год", "rf_ok": True, "scholarship": "Cambridge Trust"},
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
        "Знаешь ли ты другие языки? (помимо русского и английского)\n\n"
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
            f"Отлично! Уточни направление в рамках {clean_field}:",
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

def show_results(message):
    data = user_data.get(message.chat.id, {})
    citizenship = data.get('citizenship', '')
    field = data.get('field', '')
    budget = message.text
    is_rf = 'Россия' in citizenship
    results = []

    clean_field = field.split(' ', 1)[1] if ' ' in field else field

    for uni in UNIVERSITIES:
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('🔍 Подобрать заново')
        bot.send_message(message.chat.id,
            "Не нашла точных совпадений 😔\n\nПопробуй расширить бюджет или выбрать другую специальность.",
            reply_markup=markup)
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
        "⚠️ _Данные актуальны на 2025 год. Всегда проверяй информацию на официальном сайте университета перед подачей документов._"
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
        "Разработка": {"ielts": "6.5+", "deadline": "15 января / 15 июля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-чат и встречи", "strengths": "Сильная инженерная школа, связи с индустрией, стажировки в крупных компаниях"},
        "Data Science": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €350/мес", "community": "Международное комьюнити", "strengths": "Исследовательская база, работа с реальными данными, партнёрства с tech-компаниями"},
        "AI / Machine Learning": {"ielts": "7.0+", "deadline": "15 января", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Активное tech-комьюнити", "strengths": "Передовые лаборатории, публикации в топ-журналах, связи с исследовательскими центрами"},
        "Физика": {"ielts": "6.0+", "deadline": "15 января / 1 июля", "duration": "3 года (бакалавр) / 2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Фундаментальные исследования, лаборатории мирового уровня, возможности для PhD"},
        "Химия": {"ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Есть русскоязычные студенты", "strengths": "Современные лаборатории, партнёрства с фармацевтическими компаниями"},
        "Биология": {"ielts": "6.0+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €200/мес", "community": "Небольшое", "strengths": "Биотехнологии, молекулярная биология, полевые исследования"},
        "Математика": {"ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Есть", "strengths": "Сильная математическая школа, применение в финансах и IT"},
        "Астрономия": {"ielts": "6.0+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Небольшое", "strengths": "Обсерватории, исследования космоса, международные коллаборации"},
        "Общая медицина": {"ielts": "6.5+", "deadline": "1 марта", "duration": "6 лет", "work": "Ограниченно", "housing": "Общежитие от €200/мес", "community": "Большое СНГ-комьюнити", "strengths": "Клиническая практика с первых лет, современные учебные больницы"},
        "Стоматология": {"ielts": "6.0+", "deadline": "1 марта", "duration": "5 лет", "work": "Ограниченно", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Клиническая практика, современное оборудование"},
        "Фармацевтика": {"ielts": "6.0+", "deadline": "1 февраля", "duration": "5 лет", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Небольшое", "strengths": "Лаборатории, партнёрства с фармкомпаниями"},
        "Психология": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Есть", "strengths": "Клиническая практика, исследования, работа с пациентами"},
        "Ветеринария": {"ielts": "6.0+", "deadline": "1 марта", "duration": "5–6 лет", "work": "Ограниченно", "housing": "Общежитие от €200/мес", "community": "Небольшое", "strengths": "Клиники, полевая практика"},
        "Менеджмент": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Активное бизнес-комьюнити", "strengths": "Международные стажировки, кейс-метод, нетворкинг"},
        "Финансы": {"ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Есть", "strengths": "CFA prep, партнёрства с банками, карьерный центр"},
        "Маркетинг": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Есть", "strengths": "Digital-маркетинг, аналитика, работа с реальными брендами"},
        "Предпринимательство": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Активное стартап-комьюнити", "strengths": "Инкубаторы, менторы, инвесторы, питч-конкурсы"},
        "Архитектура": {"ielts": "6.0+", "deadline": "1 марта", "duration": "4–5 лет (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Творческое комьюнити", "strengths": "Студии мирового уровня, практика с бюро, международные воркшопы"},
        "Графический дизайн": {"ielts": "6.0+", "deadline": "1 марта", "duration": "3–4 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Творческое комьюнити", "strengths": "Портфолио, выставки, связи с индустрией"},
        "UX/UI": {"ielts": "6.0+", "deadline": "1 февраля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Tech и дизайн комьюнити", "strengths": "Работа с реальными продуктами, стажировки в tech-компаниях"},
        "Мода": {"ielts": "6.0+", "deadline": "1 марта", "duration": "3–4 года", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Творческое", "strengths": "Показы, стажировки в домах мод, портфолио"},
        "Анимация": {"ielts": "6.0+", "deadline": "1 марта", "duration": "3–4 года", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Творческое комьюнити", "strengths": "Студии, фестивали, работа с индустрией"},
        "Журналистика": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Есть", "strengths": "Практика в редакциях, международные стажировки"},
        "Политология": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Есть", "strengths": "Исследовательские центры, стажировки в международных организациях"},
        "Право": {"ielts": "6.5+", "deadline": "1 марта", "duration": "3–4 года", "work": "До 20 часов в неделю", "housing": "Общежитие от €200/мес", "community": "Небольшое", "strengths": "Мут-корт, стажировки в юрфирмах, международное право"},
        "Международные отношения": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Международное", "strengths": "ООН, дипломатические стажировки, конференции"},
        "Дипломатия": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Международное", "strengths": "Симуляции переговоров, стажировки в МИД и международных организациях"},
        "Машиностроение": {"ielts": "6.0+", "deadline": "15 января", "duration": "3–4 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €250/мес", "community": "Есть СНГ-студенты", "strengths": "Лаборатории, практика на заводах, автомобильная и аэрокосмическая индустрия"},
        "Авиация": {"ielts": "6.5+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €300/мес", "community": "Небольшое", "strengths": "Аэрокосмические лаборатории, партнёрства с авиакомпаниями"},
        "Педагогика": {"ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "work": "До 20 часов в неделю", "housing": "Общежитие от €200/мес", "community": "Есть", "strengths": "Практика в школах, международные методики преподавания"},
    }

    d = details.get(uni['field'], {
        "ielts": "Уточняй на сайте",
        "deadline": "Уточняй на сайте",
        "duration": "Уточняй на сайте",
        "work": "До 20 часов в неделю",
        "housing": "Уточняй на сайте",
        "community": "Уточняй в местных чатах",
        "strengths": "Уточняй на официальном сайте университета"
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
        f"⭐ *Сильные стороны программы*\n"
        f"{d['strengths']}\n\n"
        f"🏠 *Жизнь*\n"
        f"Жильё: {d['housing']}\n"
        f"СНГ-комьюнити: {d['community']}\n\n"
        f"🇷🇺 *Для граждан РФ:* {rf_status}\n\n"
        f"⚠️ _Данные актуальны на 2025 год. Проверяй информацию на официальном сайте университета._\n\n"
        f"📌 Нужен чеклист документов для {uni['country']}? Нажми кнопку ниже!"
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(f"📋 Чеклист для {uni['country']}")
    markup.add('🔍 Подобрать заново')
    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)

bot.infinity_polling()
