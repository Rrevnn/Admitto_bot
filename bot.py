import telebot
from telebot import types
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
user_data = {}
WAITING_FOR_UNI_SEARCH = set()

UNIVERSITIES = [
    {"name": "TU Munich", "country": "Германия", "flag": "🇩🇪", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD €800/мес", "ielts": "6.5+", "deadline": "15 января / 15 июля", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-чат и встречи", "strengths": "Сильная инженерная школа связи с индустрией стажировки в крупных компаниях", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет (портфолио приветствуется)"},
    {"name": "TU Berlin", "country": "Германия", "flag": "🇩🇪", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января / 15 июля", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-чат", "strengths": "Сильная инженерная школа партнёрства с Berlin tech ecosystem", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет (портфолио приветствуется)"},
    {"name": "KIT Karlsruhe", "country": "Германия", "flag": "🇩🇪", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €280/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Один из топ технических университетов Германии исследования мирового уровня", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет (портфолио приветствуется)"},
    {"name": "Czech Technical University", "country": "Чехия", "flag": "🇨🇿", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть русскоязычные студенты", "strengths": "Сильная техническая школа доступное обучение в центре Праги", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет (портфолио приветствуется)"},
    {"name": "Budapest Tech BME", "country": "Венгрия", "flag": "🇭🇺", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё один из лучших технических вузов Венгрии", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (портфолио приветствуется)"},
    {"name": "METU", "country": "Турция", "flag": "🇹🇷", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Ведущий технический университет Турции сильные исследования", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Нет (портфолио приветствуется)"},
    {"name": "Tsinghua University", "country": "Китай", "flag": "🇨🇳", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.5+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Лучший технический университет Азии мощные исследования и индустриальные связи", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Нет (портфолио приветствуется)"},
    {"name": "KAIST", "country": "Южная Корея", "flag": "🇰🇷", "field": "Разработка", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия", "ielts": "6.5+", "deadline": "1 сентября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Топ технический университет Азии полностью на английском", "work": "До 20 часов в неделю", "language": "Английский / Корейский", "exams": "Нет (портфолио приветствуется)"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Разработка", "cost": "$57000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "7.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от $1000/мес", "community": "Международное комьюнити", "strengths": "Лучший технический университет мира уникальные исследовательские возможности", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (портфолио приветствуется)"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Разработка", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.0+", "deadline": "15 октября", "duration": "3 года (бакалавр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Один из лучших университетов мира уникальная система колледжей", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (портфолио приветствуется)"},
    {"name": "Warsaw University of Technology", "country": "Польша", "flag": "🇵🇱", "field": "Разработка", "cost": "€2000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 июля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Есть СНГ-студенты", "strengths": "Доступная разработка в ЕС сильная техническая школа", "work": "До 20 часов в неделю", "language": "Английский / Польский", "exams": "Нет (портфолио приветствуется)"},
    {"name": "TU Delft", "country": "Нидерланды", "flag": "🇳🇱", "field": "Data Science", "cost": "€2200/год", "rf_ok": True, "scholarship": "Holland Scholarship", "ielts": "6.5+", "deadline": "1 февраля / 1 сентября", "duration": "2 года (магистр)", "housing": "Общежитие от €350/мес", "community": "Международное комьюнити", "strengths": "Исследовательская база работа с реальными данными партнёрства с tech-компаниями", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (математический тест в некоторых вузах)"},
    {"name": "Eindhoven University", "country": "Нидерланды", "flag": "🇳🇱", "field": "Data Science", "cost": "€2200/год", "rf_ok": True, "scholarship": "Holland Scholarship", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €350/мес", "community": "Международное комьюнити", "strengths": "Сильная связь с индустрией Philips и другие крупные компании рядом", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (математический тест в некоторых вузах)"},
    {"name": "Harbin Institute of Technology", "country": "Китай", "flag": "🇨🇳", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.0+", "deadline": "1 января", "duration": "2 года (магистр)", "housing": "Общежитие от €100/мес", "community": "Есть СНГ-студенты", "strengths": "Сильные исследования в области AI и Data Science стипендия покрывает всё", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Нет (математический тест в некоторых вузах)"},
    {"name": "POSTECH", "country": "Южная Корея", "flag": "🇰🇷", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия", "ielts": "6.5+", "deadline": "1 сентября", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Один из лучших исследовательских университетов Азии", "work": "До 20 часов в неделю", "language": "Английский / Корейский", "exams": "Нет (математический тест в некоторых вузах)"},
    {"name": "University of Tartu", "country": "Эстония", "flag": "🇪🇪", "field": "Data Science", "cost": "€1660/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "6.0+", "deadline": "1 апреля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Цифровое государство Эстония уникальная среда для IT-исследований", "work": "До 20 часов в неделю", "language": "Английский / Эстонский", "exams": "Нет (математический тест в некоторых вузах)"},
    {"name": "University of Amsterdam", "country": "Нидерланды", "flag": "🇳🇱", "field": "Data Science", "cost": "€2314/год", "rf_ok": True, "scholarship": "Holland Scholarship", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €400/мес", "community": "Международное комьюнити", "strengths": "Сильная исследовательская база в центре Амстердама", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (математический тест в некоторых вузах)"},
    {"name": "Budapest Tech BME DS", "country": "Венгрия", "flag": "🇭🇺", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная техническая база", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (математический тест в некоторых вузах)"},
    {"name": "Charles University DS", "country": "Чехия", "flag": "🇨🇿", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Есть русскоязычные студенты", "strengths": "Бесплатное образование в центре Праги", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет (математический тест в некоторых вузах)"},
    {"name": "Nazarbayev University DS", "country": "Казахстан", "flag": "🇰🇿", "field": "Data Science", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Полная стипендия", "ielts": "6.5+", "deadline": "1 декабря", "duration": "2 года (магистр)", "housing": "Общежитие бесплатно", "community": "Большое СНГ-комьюнити", "strengths": "Полная стипендия партнёрства с топ университетами мира", "work": "До 20 часов в неделю", "language": "Английский / Русский", "exams": "Нет (математический тест в некоторых вузах)"},
    {"name": "TU Munich AI", "country": "Германия", "flag": "🇩🇪", "field": "AI / Machine Learning", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "7.0+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Передовые лаборатории публикации в топ-журналах связи с исследовательскими центрами", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Математический тест в части вузов"},
    {"name": "Bilkent University", "country": "Турция", "flag": "🇹🇷", "field": "AI / Machine Learning", "cost": "$6000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Ведущий частный университет Турции сильные AI-исследования", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Математический тест в части вузов"},
    {"name": "Seoul National University", "country": "Южная Корея", "flag": "🇰🇷", "field": "AI / Machine Learning", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия", "ielts": "6.5+", "deadline": "1 сентября", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Лучший университет Кореи мощные AI-лаборатории", "work": "До 20 часов в неделю", "language": "Английский / Корейский", "exams": "Математический тест в части вузов"},
    {"name": "KAIST AI", "country": "Южная Корея", "flag": "🇰🇷", "field": "AI / Machine Learning", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия", "ielts": "6.5+", "deadline": "1 сентября", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в AI-исследованиях", "work": "До 20 часов в неделю", "language": "Английский / Корейский", "exams": "Математический тест в части вузов"},
    {"name": "Tsinghua University AI", "country": "Китай", "flag": "🇨🇳", "field": "AI / Machine Learning", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.5+", "deadline": "1 января", "duration": "2 года (магистр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Топ AI в Азии стипендия покрывает всё", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Математический тест в части вузов"},
    {"name": "TU Berlin Security", "country": "Германия", "flag": "🇩🇪", "field": "Кибербезопасность", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Сильная школа кибербезопасности связи с немецкими компаниями", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "University of Tartu Security", "country": "Эстония", "flag": "🇪🇪", "field": "Кибербезопасность", "cost": "€1660/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "6.0+", "deadline": "1 апреля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Небольшое комьюнити", "strengths": "Эстония мировой лидер в e-government уникальная среда для кибербезопасности", "work": "До 20 часов в неделю", "language": "Английский / Эстонский", "exams": "Нет"},
    {"name": "Czech Technical University Cyber", "country": "Чехия", "flag": "🇨🇿", "field": "Кибербезопасность", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная кибербезопасность в ЕС", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет"},
    {"name": "Budapest Tech BME Cyber", "country": "Венгрия", "flag": "🇭🇺", "field": "Кибербезопасность", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная техническая база", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "KIT Karlsruhe Robotics", "country": "Германия", "flag": "🇩🇪", "field": "Робототехника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €280/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Мировой уровень исследований в робототехнике партнёрства с промышленностью", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет (портфолио для некоторых программ)"},
    {"name": "KAIST Robotics", "country": "Южная Корея", "flag": "🇰🇷", "field": "Робототехника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия", "ielts": "6.5+", "deadline": "1 сентября", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Топ робототехника в Азии уникальные лаборатории", "work": "До 20 часов в неделю", "language": "Английский / Корейский", "exams": "Нет (портфолио для некоторых программ)"},
    {"name": "TU Munich Robotics", "country": "Германия", "flag": "🇩🇪", "field": "Робототехника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Мировой лидер в роботизации партнёрства с BMW Siemens", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет (портфолио для некоторых программ)"},
    {"name": "MIT Robotics", "country": "США", "flag": "🇺🇸", "field": "Робототехника", "cost": "$57000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "7.0+", "deadline": "1 января", "duration": "2 года (магистр)", "housing": "Общежитие от $1000/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в робототехнике CSAIL лаборатория", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (портфолио для некоторых программ)"},
    {"name": "Heidelberg University", "country": "Германия", "flag": "🇩🇪", "field": "Физика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.0+", "deadline": "15 января / 1 июля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €250/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Один из старейших университетов Европы фундаментальные исследования мирового уровня", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Вступительный тест по физике/математике"},
    {"name": "LMU Munich", "country": "Германия", "flag": "🇩🇪", "field": "Физика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Топ университет Германии сильная физическая школа лауреаты Нобелевской премии", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Вступительный тест по физике/математике"},
    {"name": "Charles University", "country": "Чехия", "flag": "🇨🇿", "field": "Физика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть русскоязычные студенты", "strengths": "Старейший университет Центральной Европы бесплатное обучение", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Вступительный тест по физике/математике"},
    {"name": "Budapest ELTE", "country": "Венгрия", "flag": "🇭🇺", "field": "Физика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная физическая школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Вступительный тест по физике/математике"},
    {"name": "Peking University", "country": "Китай", "flag": "🇨🇳", "field": "Физика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Лучший университет Китая мощные исследования в физике", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Вступительный тест по физике/математике"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Физика", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.0+", "deadline": "15 октября", "duration": "3 года (бакалавр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Родина многих физических открытий Кавендишская лаборатория", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Вступительный тест по физике/математике"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Физика", "cost": "$57000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "7.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от $1000/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в физических исследованиях", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Вступительный тест по физике/математике"},
    {"name": "University of Vienna", "country": "Австрия", "flag": "🇦🇹", "field": "Химия", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €250/мес", "community": "Есть СНГ-студенты", "strengths": "Один из старейших университетов Европы сильная химическая школа", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Вступительный тест по химии"},
    {"name": "Masaryk University", "country": "Чехия", "flag": "🇨🇿", "field": "Химия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть русскоязычные студенты", "strengths": "Бесплатное обучение в красивом Брно", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Вступительный тест по химии"},
    {"name": "Koç University", "country": "Турция", "flag": "🇹🇷", "field": "Химия", "cost": "$5000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Ведущий частный университет Турции сильная исследовательская база", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Вступительный тест по химии"},
    {"name": "Charles University Chemistry", "country": "Чехия", "flag": "🇨🇿", "field": "Химия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть русскоязычные студенты", "strengths": "Бесплатная химия богатые лаборатории", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Вступительный тест по химии"},
    {"name": "Budapest ELTE Chemistry", "country": "Венгрия", "flag": "🇭🇺", "field": "Химия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная химическая школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Вступительный тест по химии"},
    {"name": "University of Belgrade", "country": "Сербия", "flag": "🇷🇸", "field": "Биология", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступное образование виза не нужна для граждан РФ", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Вступительный тест по биологии"},
    {"name": "University of Debrecen", "country": "Венгрия", "flag": "🇭🇺", "field": "Биология", "cost": "€2000/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Активное СНГ-комьюнити", "strengths": "Хорошая медицинская и биологическая школа стипендия доступна", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Вступительный тест по биологии"},
    {"name": "Tbilisi State University", "country": "Грузия", "flag": "🇬🇪", "field": "Биология", "cost": "€1200/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступное образование виза не нужна для граждан РФ", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Вступительный тест по биологии"},
    {"name": "Charles University Biology", "country": "Чехия", "flag": "🇨🇿", "field": "Биология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная биология сильная лаборатория", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Вступительный тест по биологии"},
    {"name": "Peking University Biology", "country": "Китай", "flag": "🇨🇳", "field": "Биология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Топ биология Азии стипендия покрывает всё", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Вступительный тест по биологии"},
    {"name": "University of Buenos Aires", "country": "Аргентина", "flag": "🇦🇷", "field": "Экология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "Не требуется", "deadline": "1 марта", "duration": "5 лет", "housing": "Жильё от €200/мес", "community": "Небольшое русскоязычное комьюнити", "strengths": "Бесплатное образование уникальная экосистема Южной Америки", "work": "До 20 часов в неделю", "language": "Испанский", "exams": "Нет"},
    {"name": "University of Wroclaw", "country": "Польша", "flag": "🇵🇱", "field": "Экология", "cost": "€2000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 июля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Есть СНГ-студенты", "strengths": "Доступная Польша красивый город сильная экологическая школа", "work": "До 20 часов в неделю", "language": "Английский / Польский", "exams": "Нет"},
    {"name": "Charles University Ecology", "country": "Чехия", "flag": "🇨🇿", "field": "Экология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная экология в центре Европы", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет"},
    {"name": "University of Vienna Ecology", "country": "Австрия", "flag": "🇦🇹", "field": "Экология", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Альпийская экология уникальные исследования природы", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "Tbilisi State University Ecology", "country": "Грузия", "flag": "🇬🇪", "field": "Экология", "cost": "€1200/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная экология Кавказский регион уникальные экосистемы", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Нет"},
    {"name": "Budapest ELTE Math", "country": "Венгрия", "flag": "🇭🇺", "field": "Математика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Венгрия известна сильной математической школой стипендия покрывает всё", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Вступительный тест по математике"},
    {"name": "Charles University Math", "country": "Чехия", "flag": "🇨🇿", "field": "Математика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть русскоязычные студенты", "strengths": "Бесплатное образование в центре Праги сильная математическая традиция", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Вступительный тест по математике"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Математика", "cost": "$57000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "7.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от $1000/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в математике Fields Medal выпускники", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Вступительный тест по математике"},
    {"name": "University of Vienna Math", "country": "Австрия", "flag": "🇦🇹", "field": "Математика", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Сильная математическая школа Вены", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Вступительный тест по математике"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Математика", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.0+", "deadline": "15 октября", "duration": "3 года (бакалавр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Родина Ньютона Харди и других великих математиков", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Вступительный тест по математике"},
    {"name": "Budapest ELTE Astronomy", "country": "Венгрия", "flag": "🇭🇺", "field": "Астрономия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная астрономическая традиция", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Вступительный тест по физике/математике"},
    {"name": "Charles University Astronomy", "country": "Чехия", "flag": "🇨🇿", "field": "Астрономия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть русскоязычные студенты", "strengths": "Бесплатное обучение обсерватории рядом", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Вступительный тест по физике/математике"},
    {"name": "Ankara University Astronomy", "country": "Турция", "flag": "🇹🇷", "field": "Астрономия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Международное комьюнити", "strengths": "Бесплатное образование стипендия доступна", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Вступительный тест по физике/математике"},
    {"name": "Peking University Astronomy", "country": "Китай", "flag": "🇨🇳", "field": "Астрономия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Передовые исследования космоса стипендия покрывает всё", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Вступительный тест по физике/математике"},
    {"name": "Seoul National University Astronomy", "country": "Южная Корея", "flag": "🇰🇷", "field": "Астрономия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия", "ielts": "6.5+", "deadline": "1 сентября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Топ университет Азии современные обсерватории", "work": "До 20 часов в неделю", "language": "Английский / Корейский", "exams": "Вступительный тест по физике/математике"},
    {"name": "University of Vienna Astronomy", "country": "Австрия", "flag": "🇦🇹", "field": "Астрономия", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Историческая астрономическая школа обсерватория Вены", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Вступительный тест по физике/математике"},
    {"name": "Corvinus University", "country": "Венгрия", "flag": "🇭🇺", "field": "Менеджмент", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Активное бизнес-комьюнити", "strengths": "Стипендия покрывает всё специализация на международном бизнесе", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (эссе/кейс в некоторых вузах)"},
    {"name": "Prague University of Economics", "country": "Чехия", "flag": "🇨🇿", "field": "Менеджмент", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатное образование в центре Праги сильная бизнес-школа", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет (эссе/кейс в некоторых вузах)"},
    {"name": "Nazarbayev University", "country": "Казахстан", "flag": "🇰🇿", "field": "Менеджмент", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Полная стипендия", "ielts": "6.5+", "deadline": "1 декабря", "duration": "4 года (бакалавр)", "housing": "Общежитие бесплатно", "community": "Большое СНГ-комьюнити", "strengths": "Полная стипендия покрывает всё партнёрства с топ университетами мира", "work": "До 20 часов в неделю", "language": "Английский / Русский", "exams": "Нет (эссе/кейс в некоторых вузах)"},
    {"name": "Tbilisi Free University", "country": "Грузия", "flag": "🇬🇪", "field": "Менеджмент", "cost": "€3000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Жильё от €200/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступное образование виза не нужна для граждан РФ", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Нет (эссе/кейс в некоторых вузах)"},
    {"name": "University of Belgrade Management", "country": "Сербия", "flag": "🇷🇸", "field": "Менеджмент", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступный менеджмент виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Нет (эссе/кейс в некоторых вузах)"},
    {"name": "IE University", "country": "Испания", "flag": "🇪🇸", "field": "Финансы", "cost": "$15000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Жильё от €600/мес", "community": "Международное комьюнити", "strengths": "Один из топ бизнес-школ Европы сильная карьерная поддержка", "work": "До 20 часов в неделю", "language": "Английский / Испанский", "exams": "Нет (математический тест в части вузов)"},
    {"name": "Tbilisi Free University Finance", "country": "Грузия", "flag": "🇬🇪", "field": "Финансы", "cost": "€3000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Жильё от €200/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступное образование виза не нужна для граждан РФ", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Нет (математический тест в части вузов)"},
    {"name": "Corvinus University Finance", "country": "Венгрия", "flag": "🇭🇺", "field": "Финансы", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная финансовая школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (математический тест в части вузов)"},
    {"name": "Prague University of Economics Finance", "country": "Чехия", "flag": "🇨🇿", "field": "Финансы", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатные финансы в центре Европы", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет (математический тест в части вузов)"},
    {"name": "American University of Armenia", "country": "Армения", "flag": "🇦🇲", "field": "Маркетинг", "cost": "$5000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "6.0+", "deadline": "1 марта", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Большое СНГ-комьюнити", "strengths": "Американская система образования в СНГ доступные цены", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет"},
    {"name": "Corvinus University Marketing", "country": "Венгрия", "flag": "🇭🇺", "field": "Маркетинг", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё digital-маркетинг и аналитика", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "Bilkent University Marketing", "country": "Турция", "flag": "🇹🇷", "field": "Маркетинг", "cost": "$6000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.5+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Ведущий частный университет Турции сильный маркетинг", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Нет"},
    {"name": "Tbilisi State University Marketing", "country": "Грузия", "flag": "🇬🇪", "field": "Маркетинг", "cost": "€1200/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступный маркетинг виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Нет"},
    {"name": "Koç University Business", "country": "Турция", "flag": "🇹🇷", "field": "Предпринимательство", "cost": "$9000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Топ стартап-экосистема Стамбула инкубаторы менторы инвесторы", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Нет (питч/бизнес-план приветствуется)"},
    {"name": "Nazarbayev University Entrepreneurship", "country": "Казахстан", "flag": "🇰🇿", "field": "Предпринимательство", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Полная стипендия", "ielts": "6.5+", "deadline": "1 декабря", "duration": "2 года (магистр)", "housing": "Общежитие бесплатно", "community": "Большое СНГ-комьюнити", "strengths": "Полная стипендия стартап-инкубатор", "work": "До 20 часов в неделю", "language": "Английский / Русский", "exams": "Нет (питч/бизнес-план приветствуется)"},
    {"name": "Budapest Metropolitan University Entrepreneurship", "country": "Венгрия", "flag": "🇭🇺", "field": "Предпринимательство", "cost": "€3500/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия доступна растущая стартап-сцена Будапешта", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (питч/бизнес-план приветствуется)"},
    {"name": "Heriot-Watt Dubai", "country": "ОАЭ", "flag": "🇦🇪", "field": "Логистика", "cost": "$12000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "6.0+", "deadline": "Rolling", "duration": "2 года (магистр)", "housing": "Жильё от $800/мес", "community": "Международное комьюнити", "strengths": "Дубай мировой хаб логистики уникальные карьерные возможности", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет"},
    {"name": "Koç University Logistics", "country": "Турция", "flag": "🇹🇷", "field": "Логистика", "cost": "$8000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Стамбул мост между Европой и Азией ключевой логистический хаб", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Нет"},
    {"name": "Corvinus University Logistics", "country": "Венгрия", "flag": "🇭🇺", "field": "Логистика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё Венгрия транспортный узел Европы", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "Warsaw University Logistics", "country": "Польша", "flag": "🇵🇱", "field": "Логистика", "cost": "€2000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 июля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Есть СНГ-студенты", "strengths": "Польша крупнейший логистический рынок ЦВЕ", "work": "До 20 часов в неделю", "language": "Английский / Польский", "exams": "Нет"},
    {"name": "Charles University Medicine", "country": "Чехия", "flag": "🇨🇿", "field": "Общая медицина", "cost": "€8000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.5+", "deadline": "1 марта", "duration": "6 лет", "housing": "Общежитие от €200/мес", "community": "Большое СНГ-комьюнити", "strengths": "Лучшая медицинская школа Центральной Европы обучение на английском", "work": "Ограниченно", "language": "Английский / Чешский", "exams": "Вступительный экзамен (биология, химия)"},
    {"name": "Semmelweis University", "country": "Венгрия", "flag": "🇭🇺", "field": "Общая медицина", "cost": "€9000/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.5+", "deadline": "1 марта", "duration": "6 лет", "housing": "Общежитие от €200/мес", "community": "Большое СНГ-комьюнити", "strengths": "Топ медицинский университет Европы стипендия доступна", "work": "Ограниченно", "language": "Английский / Венгерский", "exams": "Вступительный экзамен (биология, химия)"},
    {"name": "Tbilisi State Medical University", "country": "Грузия", "flag": "🇬🇪", "field": "Общая медицина", "cost": "$5000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 сентября", "duration": "6 лет", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная медицина виза не нужна признание диплома в Европе", "work": "Ограниченно", "language": "Английский / Грузинский", "exams": "Вступительный экзамен (биология, химия)"},
    {"name": "Ankara University Medicine", "country": "Турция", "flag": "🇹🇷", "field": "Общая медицина", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "6 лет", "housing": "Общежитие от €150/мес", "community": "Международное комьюнити", "strengths": "Бесплатное медицинское образование стипендия покрывает проживание", "work": "Ограниченно", "language": "Английский / Турецкий", "exams": "Вступительный экзамен (биология, химия)"},
    {"name": "Yerevan State Medical University", "country": "Армения", "flag": "🇦🇲", "field": "Общая медицина", "cost": "$4000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 сентября", "duration": "6 лет", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Самое доступное медицинское образование признание диплома в СНГ", "work": "Ограниченно", "language": "Английский", "exams": "Вступительный экзамен (биология, химия)"},
    {"name": "University of Debrecen Medicine", "country": "Венгрия", "flag": "🇭🇺", "field": "Стоматология", "cost": "€9000/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "1 марта", "duration": "5 лет", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Топ стоматология Венгрии стипендия доступна", "work": "Ограниченно", "language": "Английский / Венгерский", "exams": "Вступительный экзамен (биология, химия)"},
    {"name": "Poznan University of Medicine", "country": "Польша", "flag": "🇵🇱", "field": "Стоматология", "cost": "€6000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 июля", "duration": "5 лет", "housing": "Общежитие от €150/мес", "community": "Есть СНГ-студенты", "strengths": "Доступная стоматология в ЕС признание диплома по всей Европе", "work": "Ограниченно", "language": "Английский / Польский", "exams": "Вступительный экзамен (биология, химия)"},
    {"name": "Tbilisi State Medical University Dentistry", "country": "Грузия", "flag": "🇬🇪", "field": "Стоматология", "cost": "$4000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 сентября", "duration": "5 лет", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Самая доступная стоматология виза не нужна", "work": "Ограниченно", "language": "Английский / Грузинский", "exams": "Вступительный экзамен (биология, химия)"},
    {"name": "Semmelweis University Dentistry", "country": "Венгрия", "flag": "🇭🇺", "field": "Стоматология", "cost": "€10000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "5 лет", "housing": "Общежитие от €200/мес", "community": "Большое СНГ-комьюнити", "strengths": "Топ стоматология Европы современное оборудование", "work": "Ограниченно", "language": "Английский / Венгерский", "exams": "Вступительный экзамен (биология, химия)"},
    {"name": "Masaryk University Pharmacy", "country": "Чехия", "flag": "🇨🇿", "field": "Фармацевтика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "5 лет", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная фармацевтика на английском признание диплома в ЕС", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Вступительный экзамен (химия)"},
    {"name": "Charles University Pharmacy", "country": "Чехия", "flag": "🇨🇿", "field": "Фармацевтика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "5 лет", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная фармацевтика сильные лаборатории", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Вступительный экзамен (химия)"},
    {"name": "University of Belgrade Pharmacy", "country": "Сербия", "flag": "🇷🇸", "field": "Фармацевтика", "cost": "€2000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная фармацевтика виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Вступительный экзамен (химия)"},
    {"name": "Ankara University Pharmacy", "country": "Турция", "flag": "🇹🇷", "field": "Фармацевтика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "5 лет", "housing": "Общежитие от €150/мес", "community": "Международное комьюнити", "strengths": "Бесплатная фармацевтика стипендия доступна", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Вступительный экзамен (химия)"},
    {"name": "University of Vienna Psychology", "country": "Австрия", "flag": "🇦🇹", "field": "Психология", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Вена родина психоанализа сильнейшая психологическая школа Европы", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет (собеседование в части вузов)"},
    {"name": "Budapest ELTE Psychology", "country": "Венгрия", "flag": "🇭🇺", "field": "Психология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная психологическая школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (собеседование в части вузов)"},
    {"name": "Charles University Psychology", "country": "Чехия", "flag": "🇨🇿", "field": "Психология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.5+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная психология сильная клиническая школа", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет (собеседование в части вузов)"},
    {"name": "University of Belgrade Psychology", "country": "Сербия", "flag": "🇷🇸", "field": "Психология", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная психология виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Нет (собеседование в части вузов)"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Психология", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.0+", "deadline": "15 октября", "duration": "3 года (бакалавр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в психологических исследованиях", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (собеседование в части вузов)"},
    {"name": "University of Belgrade Vet", "country": "Сербия", "flag": "🇷🇸", "field": "Ветеринария", "cost": "€2000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "5 лет", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная ветеринария виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Вступительный экзамен (биология)"},
    {"name": "Budapest University of Veterinary Medicine", "country": "Венгрия", "flag": "🇭🇺", "field": "Ветеринария", "cost": "€4000/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "5.5 лет", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Топ ветеринария Европы стипендия доступна", "work": "Ограниченно", "language": "Английский / Венгерский", "exams": "Вступительный экзамен (биология)"},
    {"name": "Ankara University Veterinary", "country": "Турция", "flag": "🇹🇷", "field": "Ветеринария", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "5 лет", "housing": "Общежитие от €150/мес", "community": "Международное комьюнити", "strengths": "Бесплатная ветеринария стипендия доступна", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Вступительный экзамен (биология)"},
    {"name": "Tbilisi State University Vet", "country": "Грузия", "flag": "🇬🇪", "field": "Ветеринария", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 октября", "duration": "5 лет", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная ветеринария виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Вступительный экзамен (биология)"},
    {"name": "Aalto University", "country": "Финляндия", "flag": "🇫🇮", "field": "Графический дизайн", "cost": "€5000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "6.5+", "deadline": "1 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €350/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Один из топ дизайн-университетов Европы портфолио выставки связи с индустрией", "work": "До 20 часов в неделю", "language": "Английский / Финский", "exams": "Портфолио обязательно"},
    {"name": "Yildiz Technical University", "country": "Турция", "flag": "🇹🇷", "field": "Графический дизайн", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Международное комьюнити", "strengths": "Бесплатное дизайн-образование в Стамбуле стипендия доступна", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Портфолио обязательно"},
    {"name": "Prague College", "country": "Чехия", "flag": "🇨🇿", "field": "Графический дизайн", "cost": "€4500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "Rolling", "duration": "3 года (бакалавр)", "housing": "Жильё от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Английский язык обучения в центре Праги творческая среда", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Портфолио обязательно"},
    {"name": "Budapest Metropolitan University", "country": "Венгрия", "flag": "🇭🇺", "field": "Графический дизайн", "cost": "€3500/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия доступна творческая среда Будапешта", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Портфолио обязательно"},
    {"name": "Seoul National University Design", "country": "Южная Корея", "flag": "🇰🇷", "field": "Графический дизайн", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия", "ielts": "6.5+", "deadline": "1 сентября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Топ дизайн в Азии K-design мировое влияние", "work": "До 20 часов в неделю", "language": "Английский / Корейский", "exams": "Портфолио обязательно"},
    {"name": "Tsinghua University Design", "country": "Китай", "flag": "🇨🇳", "field": "Графический дизайн", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Лучший дизайн-факультет Китая стипендия покрывает всё", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Портфолио обязательно"},
    {"name": "Design Academy Eindhoven", "country": "Нидерланды", "flag": "🇳🇱", "field": "UX/UI", "cost": "€2200/год", "rf_ok": True, "scholarship": "Holland Scholarship", "ielts": "6.5+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €350/мес", "community": "Международное комьюнити", "strengths": "Один из лучших дизайн-университетов мира инновационный подход", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Портфолио обязательно"},
    {"name": "Czech Technical University UX", "country": "Чехия", "flag": "🇨🇿", "field": "UX/UI", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатное образование технический подход к дизайну", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Портфолио обязательно"},
    {"name": "Budapest Metropolitan University UX", "country": "Венгрия", "flag": "🇭🇺", "field": "UX/UI", "cost": "€3500/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия доступна практический подход", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Портфолио обязательно"},
    {"name": "KAIST Design", "country": "Южная Корея", "flag": "🇰🇷", "field": "UX/UI", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия", "ielts": "6.5+", "deadline": "1 сентября", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Топ UX в Азии связи с Samsung LG и другими", "work": "До 20 часов в неделю", "language": "Английский / Корейский", "exams": "Портфолио обязательно"},
    {"name": "Aalto University UX", "country": "Финляндия", "flag": "🇫🇮", "field": "UX/UI", "cost": "€5000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "6.5+", "deadline": "1 января", "duration": "2 года (магистр)", "housing": "Общежитие от €350/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Финский дизайн мирового уровня Nokia и другие партнёры", "work": "До 20 часов в неделю", "language": "Английский / Финский", "exams": "Портфолио обязательно"},
    {"name": "TU Delft Architecture", "country": "Нидерланды", "flag": "🇳🇱", "field": "Архитектура", "cost": "€2200/год", "rf_ok": True, "scholarship": "Holland Scholarship", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €350/мес", "community": "Международное комьюнити", "strengths": "Один из лучших архитектурных факультетов мира инновации в дизайне", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Портфолио + вступительный экзамен по рисунку"},
    {"name": "Academy of Fine Arts Vienna", "country": "Австрия", "flag": "🇦🇹", "field": "Архитектура", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.0+", "deadline": "1 марта", "duration": "4 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Историческая архитектурная школа в городе архитектурных шедевров", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Портфолио + вступительный экзамен по рисунку"},
    {"name": "TU Vienna Architecture", "country": "Австрия", "flag": "🇦🇹", "field": "Архитектура", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.0+", "deadline": "1 марта", "duration": "4 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Сильная техническая архитектура в столице архитектуры", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Портфолио + вступительный экзамен по рисунку"},
    {"name": "Charles University Architecture", "country": "Чехия", "flag": "🇨🇿", "field": "Архитектура", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть русскоязычные студенты", "strengths": "Бесплатное образование Прага город архитектуры", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Портфолио + вступительный экзамен по рисунку"},
    {"name": "Budapest University of Technology", "country": "Венгрия", "flag": "🇭🇺", "field": "Архитектура", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "5 лет", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё Будапешт архитектурная жемчужина", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Портфолио + вступительный экзамен по рисунку"},
    {"name": "Istanbul Technical University", "country": "Турция", "flag": "🇹🇷", "field": "Архитектура", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Лучшая архитектура Турции исторический Стамбул", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Портфолио + вступительный экзамен по рисунку"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Архитектура", "cost": "$57000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "7.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от $1000/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в архитектурных инновациях параметрическое проектирование", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Портфолио + вступительный экзамен по рисунку"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Архитектура", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.0+", "deadline": "15 октября", "duration": "3 года (бакалавр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Историческая архитектурная школа уникальный кампус", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Портфолио + вступительный экзамен по рисунку"},
    {"name": "Tbilisi Academy of Arts", "country": "Грузия", "flag": "🇬🇪", "field": "Мода", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 сентября", "duration": "4 года (бакалавр)", "housing": "Жильё от €150/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступное творческое образование виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Портфолио обязательно"},
    {"name": "Prague College Fashion", "country": "Чехия", "flag": "🇨🇿", "field": "Мода", "cost": "€4500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "Rolling", "duration": "3 года (бакалавр)", "housing": "Жильё от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Английский язык творческая среда Праги", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Портфолио обязательно"},
    {"name": "Budapest Metropolitan University Fashion", "country": "Венгрия", "flag": "🇭🇺", "field": "Мода", "cost": "€3500/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия доступна творческий Будапешт", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Портфолио обязательно"},
    {"name": "Yildiz Technical University Fashion", "country": "Турция", "flag": "🇹🇷", "field": "Мода", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Бесплатная мода в Стамбуле стипендия доступна", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Портфолио обязательно"},
    {"name": "Tsinghua University Fashion", "country": "Китай", "flag": "🇨🇳", "field": "Мода", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Стипендия покрывает всё растущая мода-индустрия Китая", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Портфолио обязательно"},
    {"name": "Mimar Sinan Fine Arts University Fashion", "country": "Турция", "flag": "🇹🇷", "field": "Мода", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Международное комьюнити", "strengths": "Старейший арт-университет Турции бесплатное образование", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Портфолио обязательно"},
    {"name": "Bezalel Academy", "country": "Израиль", "flag": "🇮🇱", "field": "Анимация", "cost": "$8000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "6.5+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Жильё от $600/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Один из топ арт-университетов мира уникальная творческая среда", "work": "До 20 часов в неделю", "language": "Английский / Иврит", "exams": "Портфолио обязательно"},
    {"name": "Prague College Animation", "country": "Чехия", "flag": "🇨🇿", "field": "Анимация", "cost": "€4500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "Rolling", "duration": "3 года (бакалавр)", "housing": "Жильё от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Прага центр европейской анимации богатые традиции", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Портфолио обязательно"},
    {"name": "Budapest Metropolitan University Animation", "country": "Венгрия", "flag": "🇭🇺", "field": "Анимация", "cost": "€3500/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия доступна сильная анимационная школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Портфолио обязательно"},
    {"name": "KAIST Animation", "country": "Южная Корея", "flag": "🇰🇷", "field": "Анимация", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия", "ielts": "6.5+", "deadline": "1 сентября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "K-animation мировое влияние стипендия покрывает всё", "work": "До 20 часов в неделю", "language": "Английский / Корейский", "exams": "Портфолио обязательно"},
    {"name": "Tsinghua University Animation", "country": "Китай", "flag": "🇨🇳", "field": "Анимация", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Стипендия покрывает всё растущая анимация-индустрия Китая", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Портфолио обязательно"},
    {"name": "Mimar Sinan Fine Arts University Animation", "country": "Турция", "flag": "🇹🇷", "field": "Анимация", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Международное комьюнити", "strengths": "Бесплатная анимация стипендия доступна", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Портфолио обязательно"},
    {"name": "Prague College Photography", "country": "Чехия", "flag": "🇨🇿", "field": "Фотография", "cost": "€4500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "Rolling", "duration": "3 года (бакалавр)", "housing": "Жильё от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Прага красивый город для фотографии творческая среда", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Портфолио обязательно"},
    {"name": "Budapest Metropolitan University Photography", "country": "Венгрия", "flag": "🇭🇺", "field": "Фотография", "cost": "€3500/год", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия доступна сильная фотошкола", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Портфолио обязательно"},
    {"name": "Tbilisi State Academy of Arts Photography", "country": "Грузия", "flag": "🇬🇪", "field": "Фотография", "cost": "€1200/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 сентября", "duration": "4 года (бакалавр)", "housing": "Жильё от €150/мес", "community": "Большое СНГ-комьюнити", "strengths": "Самое доступное художественное образование виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Портфолио обязательно"},
    {"name": "Seoul National University Photography", "country": "Южная Корея", "flag": "🇰🇷", "field": "Фотография", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия", "ielts": "6.5+", "deadline": "1 сентября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Топ арт в Азии стипендия покрывает всё", "work": "До 20 часов в неделю", "language": "Английский / Корейский", "exams": "Портфолио обязательно"},
    {"name": "Mimar Sinan Fine Arts University Photography", "country": "Турция", "flag": "🇹🇷", "field": "Фотография", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Международное комьюнити", "strengths": "Бесплатная фотография стипендия доступна", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Портфолио обязательно"},
    {"name": "Charles University Journalism", "country": "Чехия", "flag": "🇨🇿", "field": "Журналистика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть русскоязычные студенты", "strengths": "Бесплатная журналистика практика в редакциях Праги", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет (творческое задание в части вузов)"},
    {"name": "University of Belgrade Journalism", "country": "Сербия", "flag": "🇷🇸", "field": "Журналистика", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная журналистика виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Нет (творческое задание в части вузов)"},
    {"name": "Corvinus University Journalism", "country": "Венгрия", "flag": "🇭🇺", "field": "Журналистика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё медиашкола Будапешта", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (творческое задание в части вузов)"},
    {"name": "Bilkent University Journalism", "country": "Турция", "flag": "🇹🇷", "field": "Журналистика", "cost": "$5000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.5+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Ведущий частный университет Турции сильная медиашкола", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Нет (творческое задание в части вузов)"},
    {"name": "Tbilisi State University Journalism", "country": "Грузия", "flag": "🇬🇪", "field": "Журналистика", "cost": "€1200/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная журналистика виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Нет (творческое задание в части вузов)"},
    {"name": "Tbilisi State University IR", "country": "Грузия", "flag": "🇬🇪", "field": "Дипломатия", "cost": "€1200/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 октября", "duration": "2 года (магистр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная дипломатия виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Нет (собеседование)"},
    {"name": "Corvinus University Diplomacy", "country": "Венгрия", "flag": "🇭🇺", "field": "Дипломатия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё Будапешт дипломатический центр", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (собеседование)"},
    {"name": "Charles University IR", "country": "Чехия", "flag": "🇨🇿", "field": "Дипломатия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.5+", "deadline": "1 марта", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная дипломатия в центре Европы", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет (собеседование)"},
    {"name": "University of Vienna IR", "country": "Австрия", "flag": "🇦🇹", "field": "Дипломатия", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Вена мировая столица дипломатии стажировки в международных организациях", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет (собеседование)"},
    {"name": "Columbia University Diplomacy", "country": "США", "flag": "🇺🇸", "field": "Дипломатия", "cost": "$63000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "7.0+", "deadline": "5 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от $1200/мес", "community": "Международное комьюнити", "strengths": "Лучшая дипломатическая школа мира SIPA выпускники в ООН и МИД", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (собеседование)"},
    {"name": "Peking University IR", "country": "Китай", "flag": "🇨🇳", "field": "Дипломатия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.5+", "deadline": "1 января", "duration": "2 года (магистр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Стипендия покрывает всё дипломатия с китайской перспективой", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Нет (собеседование)"},
    {"name": "Bilkent University IR", "country": "Турция", "flag": "🇹🇷", "field": "Дипломатия", "cost": "$6000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Сильная дипломатическая школа Стамбул мост Восток-Запад", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Нет (собеседование)"},
    {"name": "University of Vienna Politics", "country": "Австрия", "flag": "🇦🇹", "field": "Политология", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Вена столица международных организаций ООН ОБСЕ стажировки", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "Budapest ELTE Politics", "country": "Венгрия", "flag": "🇭🇺", "field": "Политология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная политическая школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Политология", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.0+", "deadline": "15 октября", "duration": "3 года (бакалавр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в политических науках выпускники в топ позициях", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет"},
    {"name": "Charles University Politics", "country": "Чехия", "flag": "🇨🇿", "field": "Политология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.5+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная политология в центре Европы", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет"},
    {"name": "Bilkent University Politics", "country": "Турция", "flag": "🇹🇷", "field": "Политология", "cost": "$5000/год", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.5+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Сильная политическая школа Турции", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Нет"},
    {"name": "Prague University Sociology", "country": "Чехия", "flag": "🇨🇿", "field": "Социология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная социология в центре Праги", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет"},
    {"name": "University of Vienna Sociology", "country": "Австрия", "flag": "🇦🇹", "field": "Социология", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Сильная социологическая школа Вены", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "Budapest ELTE Sociology", "country": "Венгрия", "flag": "🇭🇺", "field": "Социология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная социологическая школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "University of Belgrade Sociology", "country": "Сербия", "flag": "🇷🇸", "field": "Социология", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная социология виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Нет"},
    {"name": "Tbilisi State University Sociology", "country": "Грузия", "flag": "🇬🇪", "field": "Социология", "cost": "€1200/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная социология виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Нет"},
    {"name": "Corvinus University IR", "country": "Венгрия", "flag": "🇭🇺", "field": "Международные отношения", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Активное бизнес-комьюнити", "strengths": "Стипендия покрывает всё специализация на международных отношениях", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (собеседование в топ-вузах)"},
    {"name": "Budapest ELTE IR", "country": "Венгрия", "flag": "🇭🇺", "field": "Международные отношения", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная МО-школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (собеседование в топ-вузах)"},
    {"name": "Charles University MO", "country": "Чехия", "flag": "🇨🇿", "field": "Международные отношения", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.5+", "deadline": "1 марта", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатное образование Прага центр европейской дипломатии", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет (собеседование в топ-вузах)"},
    {"name": "University of Vienna MO", "country": "Австрия", "flag": "🇦🇹", "field": "Международные отношения", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Вена столица международных организаций стажировки в ООН ОБСЕ", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет (собеседование в топ-вузах)"},
    {"name": "Columbia University", "country": "США", "flag": "🇺🇸", "field": "Международные отношения", "cost": "$63000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "7.0+", "deadline": "5 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от $1200/мес", "community": "Международное комьюнити", "strengths": "#1 в мире по International Affairs выпускники в ООН дипломатии бизнесе", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (собеседование в топ-вузах)"},
    {"name": "Seoul National University IR", "country": "Южная Корея", "flag": "🇰🇷", "field": "Международные отношения", "cost": "Бесплатно", "rf_ok": True, "scholarship": "GKS стипендия", "ielts": "6.5+", "deadline": "1 сентября", "duration": "2 года (магистр)", "housing": "Общежитие от €200/мес", "community": "Международное комьюнити", "strengths": "Топ МО в Азии стипендия покрывает всё", "work": "До 20 часов в неделю", "language": "Английский / Корейский", "exams": "Нет (собеседование в топ-вузах)"},
    {"name": "Peking University MO", "country": "Китай", "flag": "🇨🇳", "field": "Международные отношения", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.5+", "deadline": "1 января", "duration": "2 года (магистр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Стипендия покрывает всё уникальный взгляд на международные отношения", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Нет (собеседование в топ-вузах)"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Международные отношения", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.0+", "deadline": "15 октября", "duration": "2 года (магистр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер выпускники в топ дипломатических позициях", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (собеседование в топ-вузах)"},
    {"name": "American University of Armenia Law", "country": "Армения", "flag": "🇦🇲", "field": "Право", "cost": "$5000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "6.5+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Большое СНГ-комьюнити", "strengths": "Американская система образования доступные цены", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Вступительный тест (LNAT в Великобритании)"},
    {"name": "University of Belgrade Law", "country": "Сербия", "flag": "🇷🇸", "field": "Право", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступное право виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Вступительный тест (LNAT в Великобритании)"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Право", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.5+", "deadline": "15 октября", "duration": "3 года (бакалавр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Лучшая юридическая школа мира выпускники в топ юрфирмах", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Вступительный тест (LNAT в Великобритании)"},
    {"name": "Charles University Law", "country": "Чехия", "flag": "🇨🇿", "field": "Право", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.5+", "deadline": "1 марта", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатное право в ЕС признание диплома", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Вступительный тест (LNAT в Великобритании)"},
    {"name": "Corvinus University Law", "country": "Венгрия", "flag": "🇭🇺", "field": "Право", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.5+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё право ЕС", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Вступительный тест (LNAT в Великобритании)"},
    {"name": "University of Vienna History", "country": "Австрия", "flag": "🇦🇹", "field": "История", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Вена центр европейской истории уникальные архивы", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "История", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.0+", "deadline": "15 октября", "duration": "3 года (бакалавр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в исторических науках уникальные архивы и библиотеки", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет"},
    {"name": "Charles University History", "country": "Чехия", "flag": "🇨🇿", "field": "История", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.5+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная история богатая Центральная Европа", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет"},
    {"name": "Budapest ELTE History", "country": "Венгрия", "flag": "🇭🇺", "field": "История", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.5+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё богатая история региона", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "University of Belgrade History", "country": "Сербия", "flag": "🇷🇸", "field": "История", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная история виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Нет"},
    {"name": "Charles University Philosophy", "country": "Чехия", "flag": "🇨🇿", "field": "Философия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть русскоязычные студенты", "strengths": "Бесплатная философия богатые традиции Центральной Европы", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Философия", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.0+", "deadline": "15 октября", "duration": "3 года (бакалавр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Родина аналитической философии Витгенштейн Рассел", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет"},
    {"name": "University of Vienna Philosophy", "country": "Австрия", "flag": "🇦🇹", "field": "Философия", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Венская школа философии мирового уровня", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "Budapest ELTE Philosophy", "country": "Венгрия", "flag": "🇭🇺", "field": "Философия", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная философская школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "University of Belgrade Philosophy", "country": "Сербия", "flag": "🇷🇸", "field": "Философия", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная философия виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Нет"},
    {"name": "Budapest ELTE Linguistics", "country": "Венгрия", "flag": "🇭🇺", "field": "Лингвистика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная лингвистическая школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (языковой тест)"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Лингвистика", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.0+", "deadline": "15 октября", "duration": "3 года (бакалавр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в лингвистике уникальные исследования", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (языковой тест)"},
    {"name": "Charles University Linguistics", "country": "Чехия", "flag": "🇨🇿", "field": "Лингвистика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.5+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная лингвистика многоязычная среда", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет (языковой тест)"},
    {"name": "University of Vienna Linguistics", "country": "Австрия", "flag": "🇦🇹", "field": "Лингвистика", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Вена многоязычный город уникальная среда для лингвистики", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет (языковой тест)"},
    {"name": "Tbilisi State University Culture", "country": "Грузия", "flag": "🇬🇪", "field": "Культурология", "cost": "€1200/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная культурология виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Нет"},
    {"name": "Charles University Cultural Studies", "country": "Чехия", "flag": "🇨🇿", "field": "Культурология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.5+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная культурология богатая культура ЦЕ", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет"},
    {"name": "University of Vienna Cultural Studies", "country": "Австрия", "flag": "🇦🇹", "field": "Культурология", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Вена культурная столица Европы уникальная среда", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "Budapest ELTE Cultural Studies", "country": "Венгрия", "flag": "🇭🇺", "field": "Культурология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё богатая культура региона", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "Charles University Anthropology", "country": "Чехия", "flag": "🇨🇿", "field": "Антропология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.5+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатная антропология сильная исследовательская база", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет"},
    {"name": "University of Vienna Anthropology", "country": "Австрия", "flag": "🇦🇹", "field": "Антропология", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Сильная антропологическая школа Вены", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "Budapest ELTE Anthropology", "country": "Венгрия", "flag": "🇭🇺", "field": "Антропология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная антропологическая традиция", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "University of Belgrade Anthropology", "country": "Сербия", "flag": "🇷🇸", "field": "Антропология", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная антропология виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Нет"},
    {"name": "Peking University Anthropology", "country": "Китай", "flag": "🇨🇳", "field": "Антропология", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Уникальный взгляд на антропологию стипендия покрывает всё", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Нет"},
    {"name": "TU Munich Engineering", "country": "Германия", "flag": "🇩🇪", "field": "Машиностроение", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Лучшая инженерная школа Германии связи с BMW Siemens и другими", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Математический тест в части вузов"},
    {"name": "KIT Karlsruhe Engineering", "country": "Германия", "flag": "🇩🇪", "field": "Машиностроение", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €280/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Топ инженерия Германии сильные исследования", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Математический тест в части вузов"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Машиностроение", "cost": "$57000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "7.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от $1000/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в машиностроении", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Математический тест в части вузов"},
    {"name": "Budapest Tech BME Engineering", "country": "Венгрия", "flag": "🇭🇺", "field": "Машиностроение", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильное машиностроение", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Математический тест в части вузов"},
    {"name": "Czech Technical University Engineering", "country": "Чехия", "flag": "🇨🇿", "field": "Машиностроение", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатное машиностроение в ЦЕ чешская инженерная школа", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Математический тест в части вузов"},
    {"name": "Budapest Tech Electrical", "country": "Венгрия", "flag": "🇭🇺", "field": "Электроника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная электронная школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Математический тест в части вузов"},
    {"name": "TU Munich Electrical", "country": "Германия", "flag": "🇩🇪", "field": "Электроника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Мировой лидер в электронике партнёрства с Siemens Infineon", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Математический тест в части вузов"},
    {"name": "KIT Karlsruhe Electrical", "country": "Германия", "flag": "🇩🇪", "field": "Электроника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €280/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Топ электроника Германии", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Математический тест в части вузов"},
    {"name": "Eindhoven University Electrical", "country": "Нидерланды", "flag": "🇳🇱", "field": "Электроника", "cost": "€2200/год", "rf_ok": True, "scholarship": "Holland Scholarship", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €350/мес", "community": "Международное комьюнити", "strengths": "Philips и ASML рядом уникальные возможности для карьеры", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Математический тест в части вузов"},
    {"name": "METU Electrical", "country": "Турция", "flag": "🇹🇷", "field": "Электроника", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Международное комьюнити", "strengths": "Бесплатная электроника стипендия доступна", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Математический тест в части вузов"},
    {"name": "Czech Technical University Civil", "country": "Чехия", "flag": "🇨🇿", "field": "Строительство", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатное строительство в Праге городе архитектуры", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет"},
    {"name": "TU Munich Civil", "country": "Германия", "flag": "🇩🇪", "field": "Строительство", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Топ строительство Германии связи с крупными компаниями", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "Budapest Tech BME Civil", "country": "Венгрия", "flag": "🇭🇺", "field": "Строительство", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильное строительство", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "Warsaw University of Technology Civil", "country": "Польша", "flag": "🇵🇱", "field": "Строительство", "cost": "€2000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 июля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Есть СНГ-студенты", "strengths": "Доступное строительство в ЕС", "work": "До 20 часов в неделю", "language": "Английский / Польский", "exams": "Нет"},
    {"name": "University of Belgrade Engineering Energy", "country": "Сербия", "flag": "🇷🇸", "field": "Энергетика", "cost": "€1500/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная энергетика виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Нет"},
    {"name": "TU Munich Energy", "country": "Германия", "flag": "🇩🇪", "field": "Энергетика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Немецкий Energiewende лидер в возобновляемой энергетике", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "KIT Karlsruhe Energy", "country": "Германия", "flag": "🇩🇪", "field": "Энергетика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €280/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Ведущий исследовательский центр в энергетике", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "Eindhoven University Energy", "country": "Нидерланды", "flag": "🇳🇱", "field": "Энергетика", "cost": "€2200/год", "rf_ok": True, "scholarship": "Holland Scholarship", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €350/мес", "community": "Международное комьюнити", "strengths": "Нидерланды лидер в ветроэнергетике солнечных панелях", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет"},
    {"name": "Budapest Tech BME Energy", "country": "Венгрия", "flag": "🇭🇺", "field": "Энергетика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная энергетическая школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "TU Delft Aerospace", "country": "Нидерланды", "flag": "🇳🇱", "field": "Авиация", "cost": "€2200/год", "rf_ok": True, "scholarship": "Holland Scholarship", "ielts": "6.5+", "deadline": "1 февраля", "duration": "2 года (магистр)", "housing": "Общежитие от €350/мес", "community": "Международное комьюнити", "strengths": "Один из лучших аэрокосмических факультетов мира", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Математический/физический тест"},
    {"name": "MIT", "country": "США", "flag": "🇺🇸", "field": "Авиация", "cost": "$57000/год", "rf_ok": True, "scholarship": "Частичные гранты", "ielts": "7.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от $1000/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в аэрокосмической инженерии NASA связи", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Математический/физический тест"},
    {"name": "TU Munich Aerospace", "country": "Германия", "flag": "🇩🇪", "field": "Авиация", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Сильная авиационная школа Airbus и другие партнёры", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Математический/физический тест"},
    {"name": "KIT Karlsruhe Aerospace", "country": "Германия", "flag": "🇩🇪", "field": "Авиация", "cost": "Бесплатно", "rf_ok": True, "scholarship": "DAAD", "ielts": "6.5+", "deadline": "15 января", "duration": "2 года (магистр)", "housing": "Общежитие от €280/мес", "community": "Небольшое СНГ-комьюнити", "strengths": "Топ аэрокосмика Германии", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Математический/физический тест"},
    {"name": "Budapest Tech BME Aerospace", "country": "Венгрия", "flag": "🇭🇺", "field": "Авиация", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная авиационная программа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Математический/физический тест"},
    {"name": "University of Vienna Education", "country": "Австрия", "flag": "🇦🇹", "field": "Педагогика", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Сильная педагогическая школа международные методики преподавания", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет (собеседование)"},
    {"name": "Budapest ELTE Education", "country": "Венгрия", "flag": "🇭🇺", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё практика в школах", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (собеседование)"},
    {"name": "Ankara University Education", "country": "Турция", "flag": "🇹🇷", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Türkiye Scholarships", "ielts": "6.0+", "deadline": "1 февраля", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Международное комьюнити", "strengths": "Бесплатная педагогика стипендия доступна", "work": "До 20 часов в неделю", "language": "Английский / Турецкий", "exams": "Нет (собеседование)"},
    {"name": "Nazarbayev University Education", "country": "Казахстан", "flag": "🇰🇿", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Полная стипендия", "ielts": "6.5+", "deadline": "1 декабря", "duration": "4 года (бакалавр)", "housing": "Общежитие бесплатно", "community": "Большое СНГ-комьюнити", "strengths": "Полная стипендия партнёрства с топ педагогическими школами", "work": "До 20 часов в неделю", "language": "Английский / Русский", "exams": "Нет (собеседование)"},
    {"name": "Peking University Education", "country": "Китай", "flag": "🇨🇳", "field": "Педагогика", "cost": "Бесплатно", "rf_ok": True, "scholarship": "CSC стипендия", "ielts": "6.0+", "deadline": "1 января", "duration": "4 года (бакалавр)", "housing": "Общежитие от €150/мес", "community": "Большое международное комьюнити", "strengths": "Стипендия покрывает всё китайская педагогическая система", "work": "До 20 часов в неделю", "language": "Английский / Китайский", "exams": "Нет (собеседование)"},
    {"name": "University of Belgrade Education", "country": "Сербия", "flag": "🇷🇸", "field": "Педагогика", "cost": "€1200/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступная педагогика виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Нет (собеседование)"},
    {"name": "Tbilisi State University Education", "country": "Грузия", "flag": "🇬🇪", "field": "Педагогика", "cost": "€1000/год", "rf_ok": True, "scholarship": "Нет", "ielts": "5.5+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Самая доступная педагогика виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Грузинский", "exams": "Нет (собеседование)"},
    {"name": "University of Cambridge", "country": "Великобритания", "flag": "🇬🇧", "field": "Педагогика", "cost": "£35000/год", "rf_ok": True, "scholarship": "Cambridge Trust", "ielts": "7.0+", "deadline": "15 октября", "duration": "1 год (магистр)", "housing": "Колледж от £800/мес", "community": "Международное комьюнити", "strengths": "Мировой лидер в образовании уникальные исследования", "work": "До 20 часов в неделю", "language": "Английский", "exams": "Нет (собеседование)"},
    {"name": "Charles University Education", "country": "Чехия", "flag": "🇨🇿", "field": "Психология образования", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатное образование сильная педагогическая традиция", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет"},
    {"name": "University of Vienna Educational Psychology", "country": "Австрия", "flag": "🇦🇹", "field": "Психология образования", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Сильная психология образования Вены", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет"},
    {"name": "Budapest ELTE Educational Psychology", "country": "Венгрия", "flag": "🇭🇺", "field": "Психология образования", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная школа", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет"},
    {"name": "Nazarbayev University Educational Psychology", "country": "Казахстан", "flag": "🇰🇿", "field": "Психология образования", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Полная стипендия", "ielts": "6.5+", "deadline": "1 декабря", "duration": "2 года (магистр)", "housing": "Общежитие бесплатно", "community": "Большое СНГ-комьюнити", "strengths": "Полная стипендия международные партнёрства", "work": "До 20 часов в неделю", "language": "Английский / Русский", "exams": "Нет"},
    {"name": "Charles University Special Education", "country": "Чехия", "flag": "🇨🇿", "field": "Специальное образование", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 марта", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Есть СНГ-студенты", "strengths": "Бесплатное специальное образование сильная практика", "work": "До 20 часов в неделю", "language": "Английский / Чешский", "exams": "Нет (собеседование)"},
    {"name": "University of Vienna Special Education", "country": "Австрия", "flag": "🇦🇹", "field": "Специальное образование", "cost": "€1500/год", "rf_ok": True, "scholarship": "OeAD стипендия", "ielts": "6.5+", "deadline": "1 февраля", "duration": "3 года (бакалавр)", "housing": "Общежитие от €300/мес", "community": "Есть СНГ-студенты", "strengths": "Австрия лидер в инклюзивном образовании", "work": "До 20 часов в неделю", "language": "Английский / Немецкий", "exams": "Нет (собеседование)"},
    {"name": "Budapest ELTE Special Education", "country": "Венгрия", "flag": "🇭🇺", "field": "Специальное образование", "cost": "Бесплатно", "rf_ok": True, "scholarship": "Stipendium Hungaricum", "ielts": "6.0+", "deadline": "15 января", "duration": "3 года (бакалавр)", "housing": "Общежитие от €200/мес", "community": "Активное СНГ-комьюнити", "strengths": "Стипендия покрывает всё сильная школа специального образования", "work": "До 20 часов в неделю", "language": "Английский / Венгерский", "exams": "Нет (собеседование)"},
    {"name": "University of Belgrade Special Education", "country": "Сербия", "flag": "🇷🇸", "field": "Специальное образование", "cost": "€1200/год", "rf_ok": True, "scholarship": "Нет", "ielts": "6.0+", "deadline": "1 октября", "duration": "4 года (бакалавр)", "housing": "Общежитие от €100/мес", "community": "Большое СНГ-комьюнити", "strengths": "Доступное специальное образование виза не нужна", "work": "До 20 часов в неделю", "language": "Английский / Сербский", "exams": "Нет (собеседование)"},
]
def analyze_achievements(text):
    t = text.lower()
    results = []
    if any(w in t for w in ["олимпиад"]):
        if any(w in t for w in ["международн", "international"]):
            results.append("🏆 *Международная олимпиада* — сильное достижение! Повышает шансы на DAAD, Stipendium Hungaricum, GKS")
        else:
            results.append("🥇 *Олимпиада* — хорошее достижение. Упомяни в мотивационном письме")
    if any(w in t for w in ["волонтёр", "волонтер", "volunteer"]):
        results.append("🤝 *Волонтёрство* — плюс для социальных наук и дипломатии. Ценится в Columbia SIPA, вузах Австрии")
    if any(w in t for w in ["хакатон", "hackathon"]):
        results.append("💻 *Хакатон* — отличное tech-достижение! Ценится в IT-программах TU Munich, TU Delft, KAIST")
    if any(w in t for w in ["публикац", "статья", "научн", "research"]):
        results.append("🔬 *Научная работа* — очень ценно для PhD. Обязательно упомяни в Германии и Великобритании")
    if any(w in t for w in ["стартап", "startup", "бизнес", "основал"]):
        results.append("🚀 *Предпринимательский опыт* — выделит в бизнес-школах. Ценится в Koç University, ОАЭ")
    if any(w in t for w in ["проект", "разработ", "создал"]):
        results.append("💡 *Проект/разработка* — практический опыт ценится в IT и инженерных вузах")
    if any(w in t for w in ["работ", "стажировк", "intern"]):
        results.append("💼 *Опыт работы/стажировка* — особенно ценится в магистратуре")
    if not results:
        results.append("📝 Упомяни все достижения в мотивационном письме — любой опыт важен!")
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

    plan = f"📅 *План поступления в {uni['name']}*\n\n"
    if time_type == "lots":
        plan += "У тебя много времени — готовься основательно! 🌱\n\n*Прямо сейчас:*\n"
        plan += "☐ Начни учить английский — цель IELTS 6.5+\n"
        if country in ["Германия", "Австрия"] and "Немецкий" not in other_language:
            plan += "☐ Начни учить немецкий — откроет бесплатное обучение\n"
        plan += "☐ Участвуй в олимпиадах\n\n*За 2 года:*\n"
        plan += "☐ Сдай IELTS на нужный балл\n"
        if scholarship and "Нет" not in scholarship:
            plan += f"☐ Изучи условия стипендии {scholarship}\n"
        plan += "☐ Начни писать мотивационное письмо\n\n*За 1 год:*\n"
    elif time_type == "medium":
        plan += "Времени достаточно — действуй планомерно! ⚡\n\n*Прямо сейчас:*\n"
        if "Нет" in certificate or "Планирую" in certificate:
            plan += "☐ Запишись на IELTS — подготовка 3-6 месяцев\n"
        plan += "☐ Оформи загранпаспорт если нет\n"
        if scholarship and "Нет" not in scholarship:
            plan += f"☐ Изучи условия стипендии {scholarship}\n"
        plan += "\n*За 6 месяцев:*\n"
    else:
        plan += "Действуй быстро! 🔥\n\n*Срочно:*\n"
        if "Нет" in certificate or "Планирую" in certificate:
            plan += "☐ СРОЧНО запишись на IELTS!\n"
        plan += "☐ Оформи загранпаспорт если нет\n\n*В ближайшие месяцы:*\n"

    plans_by_country = {
        "Германия": [
            "☐ Начни нострификацию аттестата",
            "☐ Напиши мотивационное письмо",
            "☐ Попроси 2 рекомендательных письма",
            "☐ Подай на стипендию DAAD (дедлайн октябрь)" if scholarship and "DAAD" in scholarship else None,
            "\n*Для граждан РФ:*\n☐ Подача через uni-assist!\n☐ Заложи +4-8 недель" if is_rf else None,
            "\n*После зачисления:*\n☐ Открыть Sperrkonto €11,208\n☐ Студенческая виза\n☐ Страховка",
        ],
        "Венгрия": [
            "☐ Напиши мотивационное письмо",
            "☐ Переведи аттестат + апостиль",
            "☐ Подай на Stipendium Hungaricum (дедлайн январь)" if scholarship and "Stipendium" in scholarship else None,
            "\n*После зачисления:*\n☐ Студенческая виза\n☐ Регистрация по месту проживания",
        ],
        "Чехия": [
            "☐ Нострификация аттестата",
            "☐ Напиши мотивационное письмо",
            "☐ Выучи чешский B2 для бесплатного обучения" if "Чешский" not in other_language else None,
            "\n*После зачисления:*\n☐ Студенческая виза",
        ],
        "Сербия": [
            "☐ Перевод аттестата на сербский",
            "☐ Справка об отсутствии судимости",
            "☐ Медицинская справка",
            "\n✅ *Для граждан РФ: виза не нужна!*" if is_rf else None,
            "\n*После зачисления:*\n☐ Регистрация по месту проживания",
        ],
        "Грузия": [
            "☐ Перевод аттестата",
            "☐ Напиши мотивационное письмо",
            "\n✅ *Для граждан РФ: виза не нужна!*" if is_rf else None,
            "\n*После зачисления:*\n☐ Регистрация",
        ],
        "Турция": [
            "☐ Переведи аттестат + апостиль",
            "☐ Напиши мотивационное письмо",
            "☐ Подай на Türkiye Scholarships (дедлайн февраль)" if scholarship and "Türkiye" in scholarship else None,
            "\n*После зачисления:*\n☐ Студенческая виза",
        ],
        "Китай": [
            "☐ Переведи аттестат + апостиль",
            "☐ Медицинская справка",
            "☐ Напиши мотивационное письмо",
            "☐ Подай на стипендию CSC (дедлайн март)" if scholarship and "CSC" in scholarship else None,
            "\n*После зачисления:*\n☐ Виза X1",
        ],
        "Южная Корея": [
            "☐ Переведи аттестат + апостиль",
            "☐ Напиши мотивационное письмо",
            "☐ Подай на GKS стипендию (дедлайн март)" if scholarship and "GKS" in scholarship else None,
            "\n*После зачисления:*\n☐ Виза D-2",
        ],
        "Нидерланды": [
            "☐ Переведи аттестат + апостиль",
            "☐ Напиши мотивационное письмо",
            "☐ Подай через Studielink",
            "☐ Подай на Holland Scholarship" if scholarship and "Holland" in scholarship else None,
            "\n*После зачисления:*\n☐ Виза MVV\n☐ Регистрация в муниципалитете",
        ],
        "Великобритания": [
            "☐ Переведи аттестат + апостиль",
            "☐ Напиши Personal Statement",
            "☐ 2 рекомендательных письма",
            "\n*После зачисления:*\n☐ Виза Tier 4",
        ],
        "США": [
            "☐ Сдай SAT/GRE если нужно",
            "☐ Напиши Personal Statement",
            "☐ 3 рекомендательных письма",
            "\n*После зачисления:*\n☐ Виза F-1",
        ],
    }

    steps = plans_by_country.get(country, [
        "☐ Уточни требования на сайте университета",
        "☐ Переведи документы + апостиль",
        "☐ Напиши мотивационное письмо",
        "\n*После зачисления:*\n☐ Студенческая виза",
    ])
    for step in steps:
        if step:
            plan += f"{step}\n"

    plan += f"\n⚠️ _Дедлайн подачи: {uni['deadline']}_"
    plan += "\n\n✅ Сохрани этот план!"
    return plan

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
        reasons.append("🗣️ Знаешь немецкий — можешь учиться бесплатно")
    if "Турецкий" in other_language and country == "Турция":
        reasons.append("🗣️ Знаешь турецкий — больше программ")
    if "Китайский" in other_language and country == "Китай":
        reasons.append("🗣️ Знаешь китайский — доступны все программы")
    if "Корейский" in other_language and country == "Южная Корея":
        reasons.append("🗣️ Знаешь корейский — доступны все программы")
    if "Технологии" in hobbies and country in ["Германия", "Нидерланды", "Южная Корея"]:
        reasons.append("💻 Страна с сильной tech-индустрией")
    if "Искусство" in hobbies and country in ["Австрия", "Чехия", "Грузия"]:
        reasons.append("🎨 Богатая культурная среда")
    if ("IT" in career or "Стартап" in career) and country in ["Германия", "Нидерланды", "Эстония"]:
        reasons.append("🚀 Один из лучших рынков для IT-карьеры")
    if "Наука" in career and country in ["Германия", "Великобритания", "США"]:
        reasons.append("🔬 Мировой центр научных исследований")
    if "Остаться" in goal and country in ["Германия", "Нидерланды", "Эстония"]:
        reasons.append("🌍 Хорошие возможности для эмиграции")
    if "Вернуться" in goal and country in ["Сербия", "Грузия", "Армения"]:
        reasons.append("🏠 Близко к дому")
    if scholarship and "Нет" not in scholarship and ("Международные" in achievements or "Национальные" in achievements):
        reasons.append(f"🎓 Твои достижения повышают шансы на {scholarship}")
    if "Стоимость" in priority and uni.get("cost") == "Бесплатно":
        reasons.append("💰 Бесплатное обучение")
    if "Безопасность" in priority and country in ["Германия", "Австрия", "Нидерланды"]:
        reasons.append("🔒 Одна из самых безопасных стран")
    if "Большое СНГ" in community or "Активное СНГ" in community:
        reasons.append("🤝 Большое СНГ-комьюнити")
    if country in ["Сербия", "Грузия"] and "Россия" in data.get("citizenship", ""):
        reasons.append("✅ Виза не нужна")
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
    if "Технологии" in hobbies and country in ["Германия", "Нидерланды", "Южная Корея"]: score += 2
    if "Искусство" in hobbies and country in ["Австрия", "Чехия", "Грузия"]: score += 2
    if "Бизнес" in hobbies and country in ["ОАЭ", "Турция", "США"]: score += 2
    if "Волонтёрство" in hobbies and country in ["Германия", "Нидерланды", "Австрия"]: score += 1
    if ("IT" in career or "Стартап" in career) and country in ["Германия", "Нидерланды", "Эстония", "Южная Корея"]: score += 2
    if "Наука" in career and country in ["Германия", "Великобритания", "США", "Китай"]: score += 2
    if "Своё дело" in career and country in ["ОАЭ", "Турция", "Эстония"]: score += 2
    if "Корпорация" in career and country in ["Германия", "США", "Великобритания"]: score += 2
    if "Социальные" in career and country in ["Германия", "Нидерланды", "Австрия"]: score += 2
    if "Остаться" in goal and country in ["Германия", "Нидерланды", "Эстония"]: score += 2
    if "Вернуться" in goal and country in ["Сербия", "Грузия", "Армения", "Казахстан"]: score += 1
    if "Международные" in achievements and scholarship != "Нет": score += 3
    if "Национальные" in achievements and scholarship != "Нет": score += 2
    if "Интроверт" in personality and country in ["Германия", "Чехия", "Венгрия"]: score += 1
    if "Экстраверт" in personality and country in ["Турция", "ОАЭ", "США"]: score += 1
    if "Рейтинг" in priority and country in ["США", "Великобритания", "Германия"]: score += 2
    if "Стоимость" in priority and uni.get("cost") == "Бесплатно": score += 3
    if "Безопасность" in priority and country in ["Германия", "Австрия", "Нидерланды", "Чехия"]: score += 2
    if "Трудоустройство" in priority and country in ["Германия", "США", "Нидерланды"]: score += 2
    if "Большое СНГ" in community or "Активное СНГ" in community: score += 1
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


EMPLOYMENT_BY_COUNTRY = {
    "Германия": {
        "score": "⭐⭐⭐⭐⭐",
        "visa": "Голубая карта ЕС (Blue Card) — легкий путь к ПМЖ",
        "salary": "€40,000–70,000/год для выпускников",
        "market": "Острая нехватка специалистов во всех отраслях",
        "stay": "После учёбы — 18 месяцев на поиск работы",
    },
    "Нидерланды": {
        "score": "⭐⭐⭐⭐⭐",
        "visa": "Orientation Year Visa — 1 год на поиск работы",
        "salary": "€35,000–60,000/год",
        "market": "Сильный рынок IT, финансов, логистики",
        "stay": "12 месяцев на поиск работы после диплома",
    },
    "Чехия": {
        "score": "⭐⭐⭐⭐",
        "visa": "Рабочая виза после учёбы",
        "salary": "€20,000–35,000/год",
        "market": "Растущий IT-рынок, много международных компаний",
        "stay": "9 месяцев на поиск работы",
    },
    "Венгрия": {
        "score": "⭐⭐⭐",
        "visa": "Рабочая виза ЕС",
        "salary": "€15,000–25,000/год",
        "market": "Небольшой рынок, многие уезжают в Западную Европу",
        "stay": "Можно остаться в ЕС через другие страны",
    },
    "Австрия": {
        "score": "⭐⭐⭐⭐⭐",
        "visa": "Красно-бело-красная карта",
        "salary": "€35,000–60,000/год",
        "market": "Сильный рынок, высокий уровень жизни",
        "stay": "12 месяцев на поиск работы",
    },
    "Сербия": {
        "score": "⭐⭐⭐",
        "visa": "Рабочая виза (не ЕС)",
        "salary": "€10,000–20,000/год",
        "market": "Небольшой рынок, но растущий IT-сектор",
        "stay": "Многие используют как плацдарм для ЕС",
    },
    "Грузия": {
        "score": "⭐⭐⭐",
        "visa": "Без визы для РФ",
        "salary": "€8,000–15,000/год",
        "market": "Маленький рынок, но лёгкий старт для бизнеса",
        "stay": "Удобная база для удалённой работы",
    },
    "Турция": {
        "score": "⭐⭐⭐⭐",
        "visa": "Рабочий ВНЖ",
        "salary": "€12,000–25,000/год",
        "market": "Растущая экономика, много стартапов",
        "stay": "Активная экосистема особенно в Стамбуле",
    },
    "Китай": {
        "score": "⭐⭐⭐⭐",
        "visa": "Рабочая виза Z",
        "salary": "€15,000–40,000/год",
        "market": "Огромный рынок, знание китайского открывает все двери",
        "stay": "Уникальные возможности для тех кто знает язык",
    },
    "Южная Корея": {
        "score": "⭐⭐⭐⭐",
        "visa": "D-10 visa — поиск работы после учёбы",
        "salary": "€20,000–45,000/год",
        "market": "Samsung, LG, Hyundai — крупные работодатели",
        "stay": "6 месяцев на поиск работы",
    },
    "США": {
        "score": "⭐⭐⭐⭐⭐",
        "visa": "OPT — 1-3 года работы после учёбы",
        "salary": "$60,000–120,000/год",
        "market": "Лучший рынок для IT, финансов, науки",
        "stay": "OPT + H-1B виза для долгосрочного остатка",
    },
    "Великобритания": {
        "score": "⭐⭐⭐⭐⭐",
        "visa": "Graduate Route — 2 года работы после учёбы",
        "salary": "£30,000–60,000/год",
        "market": "Лондон — финансовый центр мира",
        "stay": "2 года без ограничений по работодателю",
    },
    "Польша": {
        "score": "⭐⭐⭐",
        "visa": "Рабочая виза ЕС",
        "salary": "€15,000–25,000/год",
        "market": "Растущий IT-рынок, много аутсорсинга",
        "stay": "9 месяцев на поиск работы",
    },
    "Финляндия": {
        "score": "⭐⭐⭐⭐",
        "visa": "Job-seeker visa — 1 год",
        "salary": "€30,000–50,000/год",
        "market": "Nokia, Rovio — сильный tech-сектор",
        "stay": "12 месяцев на поиск работы",
    },
    "Эстония": {
        "score": "⭐⭐⭐⭐",
        "visa": "Job-seeker visa",
        "salary": "€20,000–40,000/год",
        "market": "Цифровая страна — Skype, Transferwise родились здесь",
        "stay": "9 месяцев на поиск работы",
    },
    "Казахстан": {
        "score": "⭐⭐⭐",
        "visa": "Не нужна для СНГ",
        "salary": "€10,000–20,000/год",
        "market": "Растущая экономика, нефтяной сектор",
        "stay": "Легко для граждан СНГ",
    },
    "Армения": {
        "score": "⭐⭐⭐",
        "visa": "Без визы для РФ",
        "salary": "€8,000–18,000/год",
        "market": "Растущий IT-сектор, много стартапов",
        "stay": "Удобная база для удалённой работы",
    },
    "ОАЭ": {
        "score": "⭐⭐⭐⭐⭐",
        "visa": "Рабочая виза",
        "salary": "$40,000–100,000/год (без налогов!)",
        "market": "Финансы, логистика, tech — всё есть",
        "stay": "Продление визы через работодателя",
    },
    "Израиль": {
        "score": "⭐⭐⭐⭐",
        "visa": "Рабочая виза",
        "salary": "$30,000–80,000/год",
        "market": "Стартап-нация — один из лучших IT-рынков мира",
        "stay": "Высокий спрос на tech-специалистов",
    },
    "Испания": {
        "score": "⭐⭐⭐⭐",
        "visa": "EU Blue Card",
        "salary": "€20,000–40,000/год",
        "market": "Туризм, IT, финансы",
        "stay": "12 месяцев на поиск работы",
    },
    "Аргентина": {
        "score": "⭐⭐",
        "visa": "Рабочая виза",
        "salary": "€8,000–15,000/год",
        "market": "Нестабильная экономика, но дешёвая жизнь",
        "stay": "Многие работают удалённо на западные компании",
    },
}

def normalize(text):
    if not text:
        return ""
    return " ".join(text.split()).strip().lower()

def clean_field(text):
    if not text:
        return text
    parts = text.strip().split(" ", 1)
    if len(parts) > 1 and len(parts[0]) <= 3:
        return parts[1].strip()
    return text.strip()

@bot.message_handler(commands=["start"])
def start(message):
    bot.clear_step_handler_by_chat_id(message.chat.id)
    user_data[message.chat.id] = {}
    WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Подобрать университеты")
    markup.add("🔎 Быстрый поиск")
    markup.add("📋 Чеклист документов")
    bot.send_message(message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я Viamo — твой помощник по поступлению за рубеж.\n\n"
        "Помогу найти университеты под твой профиль, собрать документы и не пропустить дедлайны.\n\n"
        "Что хочешь сделать?",
        reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["🔍 Подобрать университеты", "🔍 Подобрать заново"])
def ask_name(message):
    bot.clear_step_handler_by_chat_id(message.chat.id)
    user_data[message.chat.id] = {}
    WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
    bot.send_message(message.chat.id, "Отлично! Давай познакомимся 🎯\n\nКак тебя зовут?")
    bot.register_next_step_handler(message, ask_age)

def ask_age(message):
    user_data[message.chat.id]["name"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("До 18", "18–22")
    markup.add("23–27", "28+")
    bot.send_message(message.chat.id, f"Приятно познакомиться, {message.text}! 👋\n\nСколько тебе лет?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_grade_or_status)

def ask_grade_or_status(message):
    user_data[message.chat.id]["age"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == "До 18":
        markup.add("8 класс", "9 класс")
        markup.add("10 класс", "11 класс")
        markup.add("Другое")
        bot.send_message(message.chat.id, "В каком классе ты сейчас?", reply_markup=markup)
    else:
        markup.add("🎓 Студент", "📄 Выпускник")
        markup.add("💼 Работаю", "Другое")
        bot.send_message(message.chat.id, "Кто ты сейчас?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_citizenship)

def ask_citizenship(message):
    user_data[message.chat.id]["age_or_grade"] = message.text
    user_data[message.chat.id]["status"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🇷🇺 Россия", "🇰🇿 Казахстан")
    markup.add("🇺🇿 Узбекистан", "🇺🇦 Украина")
    markup.add("🇦🇿 Азербайджан", "🇧🇾 Беларусь")
    markup.add("🇬🇪 Грузия", "Другое")
    bot.send_message(message.chat.id, "Твоё гражданство?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_gpa)

def ask_gpa(message):
    user_data[message.chat.id]["citizenship"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⭐⭐⭐⭐⭐ Отлично (4.5–5)")
    markup.add("⭐⭐⭐⭐ Хорошо (3.5–4.5)")
    markup.add("⭐⭐⭐ Удовлетворительно")
    bot.send_message(message.chat.id, "Твой средний балл?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_achievements)

def ask_achievements(message):
    user_data[message.chat.id]["gpa"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🏆 Международные олимпиады")
    markup.add("🥇 Национальные олимпиады")
    markup.add("📚 Школьные / университетские")
    markup.add("➖ Пока нет")
    bot.send_message(message.chat.id, "Есть ли у тебя академические достижения?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_achievements_detail)

def ask_achievements_detail(message):
    user_data[message.chat.id]["achievements"] = message.text
    if "➖" in message.text:
        user_data[message.chat.id]["achievements_detail"] = ""
        ask_english(message)
        return
    bot.send_message(message.chat.id,
        "Расскажи подробнее — напиши свои достижения через запятую 📝\n\n"
        "_Например: призёр олимпиады по математике, волонтёр ООН, победитель хакатона_",
        parse_mode="Markdown")
    bot.register_next_step_handler(message, process_achievements_detail)

def process_achievements_detail(message):
    user_data[message.chat.id]["achievements_detail"] = message.text
    analysis = analyze_achievements(message.text)
    response = "🎯 *Анализ твоих достижений:*\n\n"
    for item in analysis:
        response += f"{item}\n\n"
    response += "💡 _Упомяни все достижения в мотивационном письме!_"
    bot.send_message(message.chat.id, response, parse_mode="Markdown")
    ask_english(message)

def ask_english(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔴 A1–A2", "🟡 B1–B2")
    markup.add("🟢 C1", "⭐ C2")
    bot.send_message(message.chat.id, "Уровень английского?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_certificate)

def ask_certificate(message):
    user_data[message.chat.id]["english"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✅ IELTS", "✅ TOEFL")
    markup.add("✅ Goethe / TestDaF", "✅ DELF / DALF")
    markup.add("📅 Планирую сдать", "➖ Нет")
    bot.send_message(message.chat.id, "Языковые сертификаты?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_other_language)

def ask_other_language(message):
    user_data[message.chat.id]["certificate"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🇩🇪 Немецкий", "🇫🇷 Французский")
    markup.add("🇹🇷 Турецкий", "🇨🇳 Китайский")
    markup.add("🇰🇷 Корейский", "🇷🇸 Сербский")
    markup.add("🇨🇿 Чешский", "🇭🇺 Венгерский")
    markup.add("➖ Только английский / русский")
    bot.send_message(message.chat.id,
        "Знаешь ли ты другие языки?\n\n💡 Во многих странах можно учиться бесплатно на местном языке!",
        reply_markup=markup)
    bot.register_next_step_handler(message, ask_other_language_level)

def ask_other_language_level(message):
    user_data[message.chat.id]["other_language"] = message.text
    if "➖" in message.text:
        user_data[message.chat.id]["other_language_level"] = "Нет"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("✅ Есть, действующий")
        markup.add("⚠️ Скоро истечёт")
        markup.add("❌ Нет")
        bot.send_message(message.chat.id, "Загранпаспорт?", reply_markup=markup)
        bot.register_next_step_handler(message, ask_visa)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔴 Начинающий (A1–A2)", "🟡 Средний (B1–B2)")
    markup.add("🟢 Продвинутый (C1)", "⭐ Свободно (C2)")
    bot.send_message(message.chat.id, f"Какой уровень {message.text}?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_passport)

def ask_passport(message):
    user_data[message.chat.id]["other_language_level"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✅ Есть, действующий")
    markup.add("⚠️ Скоро истечёт")
    markup.add("❌ Нет")
    bot.send_message(message.chat.id, "Загранпаспорт?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_visa)

def ask_visa(message):
    user_data[message.chat.id]["passport"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➖ Нет опыта", "✈️ Туристические")
    markup.add("🎓 Студенческие", "⚠️ Были отказы")
    bot.send_message(message.chat.id, "Опыт получения виз?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_hobbies)

def ask_hobbies(message):
    user_data[message.chat.id]["visa"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⚽ Спорт", "🎵 Музыка")
    markup.add("💻 Технологии", "🎨 Искусство")
    markup.add("📚 Наука / чтение", "🤝 Волонтёрство")
    markup.add("💼 Бизнес", "✈️ Путешествия")
    bot.send_message(message.chat.id, "Твои главные увлечения?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_personality)

def ask_personality(message):
    user_data[message.chat.id]["hobbies"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🧩 Интроверт")
    markup.add("🌟 Экстраверт")
    markup.add("⚖️ Посередине")
    bot.send_message(message.chat.id, "Как бы ты описал себя?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_stress)

def ask_stress(message):
    user_data[message.chat.id]["personality"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💡 Ищу решение", "🤝 Прошу помощи")
    markup.add("🎮 Отвлекаюсь", "🔒 Замыкаюсь")
    bot.send_message(message.chat.id, "Как реагируешь на стресс?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_leadership)

def ask_leadership(message):
    user_data[message.chat.id]["stress"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🦁 Беру инициативу")
    markup.add("🤝 Поддерживаю команду")
    markup.add("🎯 Работаю самостоятельно")
    bot.send_message(message.chat.id, "В команде ты чаще...", reply_markup=markup)
    bot.register_next_step_handler(message, ask_goal)

def ask_goal(message):
    user_data[message.chat.id]["leadership"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🌍 Остаться за рубежом")
    markup.add("🏠 Вернуться домой")
    markup.add("🤷 Пока не знаю")
    bot.send_message(message.chat.id, "Что планируешь после учёбы?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_career)

def ask_career(message):
    user_data[message.chat.id]["goal"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💻 IT / Стартап", "🏢 Корпорация")
    markup.add("🚀 Своё дело", "🔬 Наука")
    markup.add("🌱 Социальные проекты")
    bot.send_message(message.chat.id, "Карьерная цель?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_priority)

def ask_priority(message):
    user_data[message.chat.id]["career"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🏆 Рейтинг вуза", "💰 Стоимость")
    markup.add("🌍 Страна", "💼 Трудоустройство")
    markup.add("🏙️ Город и жизнь", "🔒 Безопасность")
    bot.send_message(message.chat.id, "Что важнее при выборе университета?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_main_field)

def ask_main_field(message):
    user_data[message.chat.id]["priority"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for f in FIELDS.keys():
        markup.add(f)
    bot.send_message(message.chat.id, "Почти готово! 🎯\n\nВыбери направление учёбы:", reply_markup=markup)
    bot.register_next_step_handler(message, ask_sub_field)

def ask_sub_field(message):
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
    sub_field = message.text
    user_data[message.chat.id]["field"] = sub_field
    cf = clean_field(sub_field)
    subfields = SUBFIELDS.get(cf, [])
    if subfields:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for s in subfields:
            markup.add(s)
        markup.add("➖ Любое направление")
        bot.send_message(message.chat.id, f"Уточни направление в рамках {cf}:", reply_markup=markup)
        bot.register_next_step_handler(message, ask_budget)
    else:
        ask_budget(message)

def ask_budget(message):
    if "subfield" not in user_data[message.chat.id]:
        user_data[message.chat.id]["subfield"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💚 Бесплатно / стипендия")
    markup.add("💛 До €5,000 в год")
    markup.add("🧡 До €15,000 в год")
    markup.add("❤️ Бюджет не ограничен")
    bot.send_message(message.chat.id, "Бюджет на обучение в год?", reply_markup=markup)
    bot.register_next_step_handler(message, show_results)

def get_profile_type(data):
    hobbies = data.get("hobbies", "")
    career = data.get("career", "")
    if "Технологии" in hobbies or "IT" in career:
        return "🚀 Технологический лидер", "Аналитический ум, любишь решать сложные задачи, нацелен на tech-карьеру"
    elif "Наука" in hobbies or "Наука" in career:
        return "🔬 Исследователь", "Глубокое мышление, любишь докапываться до сути"
    elif "Бизнес" in hobbies or "Своё дело" in career:
        return "💼 Предприниматель", "Амбициозный, видишь возможности там где другие видят проблемы"
    elif "Искусство" in hobbies:
        return "🎨 Творческая личность", "Мыслишь образами, создаёшь красоту, видишь мир иначе"
    elif "Волонтёрство" in hobbies or "Социальные" in career:
        return "🌱 Созидатель", "Хочешь менять мир к лучшему"
    else:
        return "🌍 Искатель возможностей", "Открыт к новому, гибкий, найдёшь себя в любой среде"

def get_missing_requirements(data, budget):
    missing = []
    if "A1" in data.get("english", "") or "A2" in data.get("english", ""):
        missing.append("📚 Подтяни английский до B2")
    if "➖ Нет" in data.get("certificate", ""):
        missing.append("📝 Сдай IELTS или TOEFL")
    if "Планирую" in data.get("certificate", ""):
        missing.append("⏰ Запишись на IELTS — подготовка 3-6 месяцев")
    if "❌ Нет" in data.get("passport", ""):
        missing.append("🛂 Оформи загранпаспорт")
    if "⚠️" in data.get("passport", ""):
        missing.append("🛂 Продли загранпаспорт")
    if "Удовл" in data.get("gpa", ""):
        missing.append("📊 Подними средний балл")
    if "Бесплатно" in budget:
        missing.append("💰 Расширь бюджет или активно ищи стипендии")
    return missing

def show_results(message):
    data = user_data.get(message.chat.id, {})
    citizenship = data.get("citizenship", "")
    field = data.get("field", "")
    budget = message.text
    is_rf = "Россия" in citizenship
    cf = clean_field(field)

    bot.send_message(message.chat.id, "⏳ Анализирую твой профиль...")

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
        f"✨ *Твой профиль готов, {name}!*\n\n{profile_type}\n_{profile_desc}_\n\n⏱ До поступления: {time_label}",
        parse_mode="Markdown")

    if not results:
        missing = get_missing_requirements(data, budget)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🔄 Сменить специальность", "🔄 Сменить направление")
        markup.add("💰 Расширить бюджет", "🔍 Начать заново")
        msg = f"😔 Не нашла университетов по *{cf}* с твоими критериями.\n\n"
        if missing:
            msg += "📋 *Что стоит подготовить:*\n"
            for item in missing:
                msg += f"{item}\n"
            msg += "\n"
        msg += "Что изменим?"
        bot.send_message(message.chat.id, msg, parse_mode="Markdown", reply_markup=markup)
        WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
        return

    subfield_text = f" · {subfield}" if subfield and "➖" not in subfield else ""
    response = f"🎯 *Топ для тебя — {cf}{subfield_text}:*\n\n"
    for uni in results[:6]:
        rf_status = "✅" if uni["rf_ok"] else "⚠️"
        stars = "⭐" * min(uni["score"], 5) if uni["score"] > 0 else ""
        reasons = get_match_reasons(uni, data)
        reason_text = f"\n_{reasons[0]}_" if reasons else ""
        response += f"{uni['flag']} *{uni['name']}* — {uni['country']} {stars}\n💰 {uni['cost']} · 🎓 {uni['scholarship']} · РФ: {rf_status}{reason_text}\n\n"
    response += "📌 Напиши название университета чтобы узнать подробнее!\n\n⚠️ _Данные актуальны на 2025 год._"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Подобрать заново", "📋 Чеклист документов")
    bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=markup)
    WAITING_FOR_UNI_SEARCH.add(message.chat.id)

@bot.message_handler(func=lambda m: m.text == "🔄 Сменить специальность")
def change_speciality(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for f in FIELDS.keys():
        markup.add(f)
    bot.send_message(message.chat.id, "Выбери новое направление:", reply_markup=markup)
    bot.register_next_step_handler(message, ask_sub_field)

@bot.message_handler(func=lambda m: m.text == "🔄 Сменить направление")
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

@bot.message_handler(func=lambda m: m.text == "💰 Расширить бюджет")
def expand_budget(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💛 До €5,000 в год")
    markup.add("🧡 До €15,000 в год")
    markup.add("❤️ Бюджет не ограничен")
    bot.send_message(message.chat.id, "Выбери новый бюджет:", reply_markup=markup)
    bot.register_next_step_handler(message, show_results)

@bot.message_handler(func=lambda m: m.text == "🔎 Быстрый поиск")
def quick_search(message):
    WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 По направлению", "🌍 По стране")
    markup.add("💰 Бесплатные", "🎓 Со стипендией")
    markup.add("🔙 Назад")
    bot.send_message(message.chat.id, "Как хочешь искать?", reply_markup=markup)
    bot.register_next_step_handler(message, quick_search_filter)

def quick_search_filter(message):
    if message.text == "📚 По направлению":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for f in FIELDS.keys():
            markup.add(f)
        bot.send_message(message.chat.id, "Выбери направление:", reply_markup=markup)
        bot.register_next_step_handler(message, quick_search_by_main_field)
    elif message.text == "🌍 По стране":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🇩🇪 Германия", "🇳🇱 Нидерланды")
        markup.add("🇭🇺 Венгрия", "🇨🇿 Чехия")
        markup.add("🇷🇸 Сербия", "🇬🇪 Грузия")
        markup.add("🇹🇷 Турция", "🇨🇳 Китай")
        markup.add("🇰🇷 Южная Корея", "🇺🇸 США")
        markup.add("🇬🇧 Великобритания", "🇦🇲 Армения")
        markup.add("🇦🇹 Австрия", "🇰🇿 Казахстан")
        bot.send_message(message.chat.id, "Выбери страну:", reply_markup=markup)
        bot.register_next_step_handler(message, quick_search_by_country)
    elif message.text == "💰 Бесплатные":
        quick_show_filtered(message.chat.id, cost_filter="Бесплатно")
    elif message.text == "🎓 Со стипендией":
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
    markup.add("➖ Все специальности")
    bot.send_message(message.chat.id, "Уточни специальность:", reply_markup=markup)
    bot.register_next_step_handler(message, quick_search_by_sub_field)

def quick_search_by_sub_field(message):
    main_field = user_data.get(message.chat.id, {}).get("quick_main_field", "")
    if "➖" in message.text:
        quick_show_filtered(message.chat.id, main_field=main_field)
    else:
        quick_show_filtered(message.chat.id, field_filter=message.text)

def quick_search_by_country(message):
    text = message.text
    parts = text.split(" ", 1)
    country = parts[1].strip() if len(parts) > 1 else text.strip()
    quick_show_filtered(message.chat.id, country_filter=country)

def quick_show_filtered(chat_id, field_filter=None, main_field=None, country_filter=None, cost_filter=None, scholarship_filter=False):
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
            if cf_norm != uni_field_norm:
                continue
        elif main_field_subs_norm:
            if uni_field_norm not in main_field_subs_norm:
                continue

        if country_filter:
            if normalize(country_filter) not in normalize(uni["country"]):
                continue

        if cost_filter:
            if normalize(uni["cost"]) != normalize(cost_filter):
                continue

        if scholarship_filter:
            s = normalize(uni["scholarship"])
            if not s or s == "нет":
                continue

        results.append(uni)

    if not results:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🔎 Быстрый поиск", "🔍 Подобрать университеты")
        label = cf or country_filter or ("бесплатные" if cost_filter else "со стипендией")
        bot.send_message(chat_id,
            f"Не нашла университетов по *{label}* 😔\n\nПопробуй другой фильтр!",
            parse_mode="Markdown", reply_markup=markup)
        return

    label = cf or country_filter or ("бесплатные" if cost_filter else "со стипендией")
    response = f"🎓 *{label} — найдено {len(results)}:*\n\n"
    for uni in results[:8]:
        rf_status = "✅" if uni["rf_ok"] else "⚠️"
        response += f"{uni['flag']} *{uni['name']}* — {uni['country']}\n"
        response += f"💰 {uni['cost']} · {uni['field']} · РФ: {rf_status}\n\n"
    if len(results) > 8:
        response += f"_...и ещё {len(results) - 8}. Используй полный подбор для точных результатов._\n\n"
    response += "📌 Напиши название университета чтобы узнать подробнее!"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔎 Быстрый поиск", "🔍 Подобрать университеты")
    bot.send_message(chat_id, response, parse_mode="Markdown", reply_markup=markup)
    WAITING_FOR_UNI_SEARCH.add(chat_id)

@bot.message_handler(func=lambda m: m.text == "📋 Чеклист документов")
def checklist(message):
    WAITING_FOR_UNI_SEARCH.discard(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🇩🇪 Германия", "🇳🇱 Нидерланды")
    markup.add("🇭🇺 Венгрия", "🇨🇿 Чехия")
    markup.add("🇷🇸 Сербия", "🇬🇪 Грузия")
    markup.add("🇹🇷 Турция", "🇨🇳 Китай")
    bot.send_message(message.chat.id, "Для какой страны нужен чеклист?", reply_markup=markup)
    bot.register_next_step_handler(message, show_checklist)

def show_checklist(message):
    checklists = {
        "🇩🇪 Германия": "📋 *Германия:*\n\n✅ Загранпаспорт\n✅ Аттестат + нострификация\n✅ IELTS 6.5+ или TestDaF\n✅ Мотивационное письмо\n✅ 2 рекомендательных письма\n✅ CV\n✅ Sperrkonto €11,208\n✅ Страховка\n\n⚠️ Для РФ: через uni-assist, срок до 8 недель",
        "🇳🇱 Нидерланды": "📋 *Нидерланды:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 6.0+\n✅ Мотивационное письмо\n✅ CV\n✅ Выписка с банковского счёта\n\n⚠️ Подача через Studielink",
        "🇭🇺 Венгрия": "📋 *Венгрия:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 5.5+\n✅ Мотивационное письмо\n✅ CV\n✅ Медицинская справка\n\n🎓 Stipendium Hungaricum покрывает всё!",
        "🇨🇿 Чехия": "📋 *Чехия:*\n\n✅ Загранпаспорт\n✅ Аттестат (нострификация)\n✅ Чешский B2 (для бесплатного)\n✅ Мотивационное письмо\n✅ CV\n\n⚠️ Бесплатно только на чешском",
        "🇷🇸 Сербия": "📋 *Сербия:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод на сербский)\n✅ Справка об отсутствии судимости\n✅ Медицинская справка\n\n✅ Виза не нужна для РФ!",
        "🇬🇪 Грузия": "📋 *Грузия:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод)\n✅ IELTS 5.5+\n✅ Мотивационное письмо\n\n✅ Виза не нужна для РФ!",
        "🇹🇷 Турция": "📋 *Турция:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ IELTS 6.0+\n✅ Мотивационное письмо\n✅ CV\n\n🎓 Türkiye Scholarships — подай до февраля!",
        "🇨🇳 Китай": "📋 *Китай:*\n\n✅ Загранпаспорт\n✅ Аттестат (перевод + апостиль)\n✅ Медицинская справка\n✅ Мотивационное письмо\n✅ CV\n\n🎓 CSC стипендия покрывает всё!",
    }
    text = checklists.get(message.text, "Пока нет чеклиста для этой страны. Скоро добавим!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Подобрать университеты", "📋 Чеклист документов")
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and m.text.startswith("📅 План поступления"))
def show_admission_plan(message):
    data = user_data.get(message.chat.id, {})
    uni = data.get("last_uni")
    if not uni:
        bot.send_message(message.chat.id, "Сначала выбери университет из списка!")
        return
    plan = get_admission_plan(uni, data)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Подобрать заново", "📋 Чеклист документов")
    bot.send_message(message.chat.id, plan, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: m.chat.id in WAITING_FOR_UNI_SEARCH)
def handle_university_search(message):
    if message.text.startswith("/"): return
   skip = ["🔍 Подобрать университеты", "🔍 Подобрать заново", "📋 Чеклист документов",
        "🔎 Быстрый поиск", "🔄 Сменить специальность", "🔄 Сменить направление",
        "💰 Расширить бюджет", "🔍 Начать заново", "🔙 Назад",
        "⚖️ Сравнить с другим", "🗑 Очистить сравнение"]
    if message.text in skip or message.text.startswith("📅") or message.text.startswith("📋 Чеклист для"):
        return
    query = message.text.lower()
    found = [u for u in UNIVERSITIES if query in u["name"].lower()]
    if not found:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🔍 Подобрать университеты", "📋 Чеклист документов")
        bot.send_message(message.chat.id, "Не нашла такой университет 😔\n\nПроверь название или напиши /start.", reply_markup=markup)
        return
    uni = found[0]
    rf_status = "✅ Принимают" if uni["rf_ok"] else "⚠️ Уточняй на сайте"
    data = user_data.get(message.chat.id, {})
    reasons = get_match_reasons(uni, data)
    emp = EMPLOYMENT_BY_COUNTRY.get(uni["country"], {})
    emp_text = ""
    if emp:
        emp_text = (
            f"\n💼 *Трудоустройство после учёбы* {emp.get('score', '')}\n"
            f"Рынок: {emp.get('market', '')}\n"
            f"Зарплата: {emp.get('salary', '')}\n"
            f"Виза: {emp.get('visa', '')}\n"
            f"Остаться: {emp.get('stay', '')}\n"
        )
    response = (
        f"{uni['flag']} *{uni['name']}*\n"
        f"📍 {uni['country']} · {uni['field']}\n\n"
        f"💰 *Финансы*\nОбучение: {uni['cost']}\nСтипендия: {uni['scholarship']}\nРабота: {uni['work']}\n\n"
        f"📋 *Поступление*\nЯзык обучения: {uni['language']}\nВступительные экзамены: {uni['exams']}\nIELTS: {uni['ielts']}\nДедлайн: {uni['deadline']}\nДлительность: {uni['duration']}\n\n"
        f"⭐ *Сильные стороны*\n{uni['strengths']}\n\n"
        f"🏠 *Жизнь*\nЖильё: {uni['housing']}\nСНГ-комьюнити: {uni['community']}\n\n"
        f"🇷🇺 *Для граждан РФ:* {rf_status}"
        + emp_text
    )
    if reasons:
        response += "\n🎯 *Почему подходит тебе:*\n"
        for r in reasons[:3]:
            response += f"• {r}\n"
    response += "\n⚠️ _Данные актуальны на 2025 год._"
    uni_name_short = uni["name"][:20]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(f"📅 План поступления в {uni_name_short}")
    markup.add(f"📋 Чеклист для {uni['country']}")
    markup.add(f"⚖️ Сравнить с другим")
    markup.add("🔍 Подобрать заново")
    user_data[message.chat.id]["last_uni"] = uni
    # Добавляем в список сравнения
    if "compare_list" not in user_data[message.chat.id]:
        user_data[message.chat.id]["compare_list"] = []
    bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "⚖️ Сравнить с другим")
def start_compare(message):
    uni = user_data.get(message.chat.id, {}).get("last_uni")
    if not uni:
        bot.send_message(message.chat.id, "Сначала открой карточку университета!")
        return
    compare_list = user_data[message.chat.id].get("compare_list", [])
    # Добавляем текущий если ещё нет
    if not any(u["name"] == uni["name"] for u in compare_list):
        compare_list.append(uni)
        user_data[message.chat.id]["compare_list"] = compare_list
    if len(compare_list) < 2:
        bot.send_message(message.chat.id,
            f"✅ *{uni['name']}* добавлен к сравнению!\n\nТеперь найди второй университет и нажми ⚖️ Сравнить с другим ещё раз.",
            parse_mode="Markdown")
    else:
        show_comparison(message)

def show_comparison(message):
    compare_list = user_data.get(message.chat.id, {}).get("compare_list", [])
    if len(compare_list) < 2:
        bot.send_message(message.chat.id, "Добавь минимум 2 университета для сравнения!")
        return

    unis = compare_list[:3]
    response = "⚖️ *Сравнение университетов:*\n\n"

    fields_to_compare = [
        ("🌍 Страна", "country"),
        ("💰 Стоимость", "cost"),
        ("🎓 Стипендия", "scholarship"),
        ("🗣️ Язык", "language"),
        ("📝 IELTS", "ielts"),
        ("📅 Дедлайн", "deadline"),
        ("⏱ Длительность", "duration"),
        ("🏠 Жильё", "housing"),
        ("✍️ Экзамены", "exams"),
    ]

    # Заголовки
    headers = " | ".join([f"*{u['name'][:15]}*" for u in unis])
    response += headers + "\n" + "—" * 30 + "\n"

    for label, key in fields_to_compare:
        values = [u.get(key, "—")[:25] for u in unis]
        response += f"\n{label}:\n"
        for i, (uni, val) in enumerate(zip(unis, values)):
            response += f"  {uni['flag']} {val}\n"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🗑 Очистить сравнение")
    markup.add("🔍 Подобрать заново", "📋 Чеклист документов")
    user_data[message.chat.id]["compare_list"] = []
    bot.send_message(message.chat.id, response, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🗑 Очистить сравнение")
def clear_comparison(message):
    user_data[message.chat.id]["compare_list"] = []
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Подобрать университеты")
    markup.add("🔎 Быстрый поиск")
    markup.add("📋 Чеклист документов")
    bot.send_message(message.chat.id, "Список сравнения очищен! Начни заново.", reply_markup=markup)


bot.infinity_polling()
