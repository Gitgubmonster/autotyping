# -*- coding: utf-8 -*-
__version__ = "1.0.0"

import time
import random
import threading
import ctypes
from ctypes import wintypes
import sys
import json
import os
import collections
import urllib.request

# ==================== НАСТРОЙКИ АВТООБНОВЛЕНИЯ ====================
GITHUB_USER = "Gitgubmonster"
GITHUB_REPO = "autotyping"
GITHUB_BRANCH = "main"
UPDATE_PROTECTED = ["config.json", "words.json"]
# =================================================================

CONFIG_FILE = "config.json"
WORDS_FILE  = "words.json"

DEFAULT_PUNCHES = [
    "Я ТВОЮ МАТЬ В КОСТЮМЕ ПУГАЛА ЕБАЛ ЗА УГЛОМ ПОП КЛУБА ОНА ВМЕСТО СТОНОВ РЫЧАЛА МРАЗЬ, ТЫ ТУРНИКЕТЫ ЖОПОЙ ЕБЕШЬ ТЫ МАШИНЕ ОТСОСАЛ КИК СТОПОМ НАЗЫВАЕШЬ ИДИ ЖОПУ ОБ ЛЮСТРУ ВЫТЕРИ",
    "КОЛИКЦИОНЕР СМЕШАРИКОВ СКВОЗЬ ВСЕЛЕНОЙ ПРИШЕЛЕЦ ЕБАНЫЙ ИДИ НАХУЙ ТЕБЯ КАРКАРЫЧЬ НИМЕРНО ТРАХНУЛ СЕЛЯНИН КОНЧЕНЫЙ ИЗ САНДАЛЬСКИХ ВОЙСК",
    "ТВОЯ БАБКА НА БУХАНКЕ ХЛЕБА ОТ МЕНТОВ УЕЗЖАЛА КРИЧАЛА АЙН СВАЙН ДРАЙН ПОЛИЦАЙН ОЙ ФЮРЕР ВЫ КАК ГИТЛЕР НА АРАБСКОМ ЗАСТОНАЛИ УСАТИК ЕБАНЫЙ",
    "СЫН СПРИНГТРАПА С МУЛЬТИКА ПРО ПИКИНЕСОВ ТЫ ЛАПОЧКУ В ЖОПУ СУВАЛА ДУМАЛА ЧТО ТЫ СВЕДОДИОДНЫЙ ШАР КРИНЖОВАЯ КУТИКУЛА ОТОРВАННАЯ ОТ ЖОПЫ",
    "У ТЕБЯ ПАПА МАШКА ГУМИБЕР ЗЕЛЕНАЯ КАЛОВАЯ МАСА КАК СТРАШЫЛКА С РОБЛОКСА РОСТЕКЛАСЬ ДАЛБОЕБ У ТЕБЯ НА РИНГТОНЕ АЕЙЛИЛИ АЕЙЛИЛА ВИС ВИС ВИС АУСВОЛА",
    "ДАЛБОЕБ Я ТЕБЕ КОПРА НА ЕБАЛЬНИКЕ СДАВИЛ ТЫ КАК КОВБОЙ ПЛЕТКОЙ МАМУ СВОЮ СЛОВИЛ И ГОВОРИШЬ СУДАРЫНЯ ВЫ СЕГОДНЯ ВОНЯЕТЕ Я ЗАСТРЕЛИЛ ЕЕ СВОИМ КЛАПОНОВЫМ ОРУЖИЕМ",
    "ХУЕСОС ТЫ КАК ТАНУКИ С ИЗМЕРЕНИЕ ПИТИПАЛЫХ УРОДЦОВ ИДИ ДАЛЬШЕ СВОЙ МАМЕ ГУСИНИЦЕ В ЖОПУ ЧЕРВЕЙ ПИХАЙ ДАУНИДЗЕ ЗАГНИВШИЙ ЗОМБИ ЖЕЛТОРОТИК Я ТЕБЕ МОЧЕВИНОЙ ПО ГУБАМ ВОДИЛ",
    "РЕЙНБОВ ТРАНСВЕСТИТ ТЫ КОГДА ДЕДА СВОЕГО УВИДИЛ У ТЕБЯ ДАВЛЕНИЕ В ЖОПЕ ПОДСКОЧИЛО",
    "У ТЕБЯ ПАПА БУРУНДУК ЕБАНЫЙ МОИ ОРЕХИ У НЕГО ВО РТУ ТЫ ПОСМОТРИ НА СВОЮ МАМУ ЕБАНАЯ БЕЛКА ЛЕТЯГА С КРЫЛЬЯМИ НА ЖОПЕ КАК ГОВОРИТСЯ БЕДНАЯ ДЬЯВОЛИЦА КОГДА ЕБУ ЗА РОГА ДЕРЖУ СЫН БЛЯДИ",
    "ТЫ КАК ВАМПИР В ЗЕРКАЛО ПОСМОТРЕЛ ПАПА ПОЛТЕРГЕЙСТ ОТОБРАЖАЕТ А БАБКА ТО ВОБЩЕ ПИЗДЕЦ ВАМПИРША БЛЯДСКАЯ НА МОЙ ОСИНОВЫЙ КОЛ СЕЛА ДУРА",
    "ТЕБЕ БАБА КАПА НА ЕБАЛО КУЛИЧ НАКИНУЛА ЛУНТИК ЕБАНЫЙ С ЛУНЫ УПАЛ МАМУ ПОТЕРЯЛ ХУЕСОС ТУПОВАТЫЙ РОЗОВАЯ ШКОЛЬНИЦА МЫ ВСЕ ТЕБЯ ТЫНДЫРИЛИ В ОЧКО СЫН ШЛЮХИ",
    "ХОДЯЧИЙ WI-FI БЕЗ ИНТЕРНЕТА ТЕБЕ БАБКА ПОСЛЕДНИЕ ПРОВОДА ПИЗДОЙ КЛЕЕЛА СУЧКА",
    "ЦЕРБЕР ЕБАННЫЙ ТРЕХ ГОЛОВЫЙ С ЗАМКА ЧЕРНОБЫЛЬСКИХ БУРУНДУКОВ ТЫ НАХУЙ ВЫЛЕЗ ДАЛБОЕБ У ТЯ КАК У САЙРЕН ХЕТА ЕХОЛОКАТОР В ЖОПЕ ИДИ ГОЛОС МАМЫ ПАРАДИРУЙ И НА БАТЛЕ ВЫСТУПАЙ",
    "КСИВИВАЙДОВСКИЙ ЗАБИТАЯ ДУРА С МУЗЫКАЛЬНОЙ ЖОПОЙ ИДИ НАХУЙ ТЕБЯ У СЕМЕРОЧКИ САМ БУФИРАМИ В ЖОПУ ЕБАЛИ",
    "Я ЕМУ ПИНКА ПОД ЗАД ДАЛ ОН МАМУ ПОТЕРЯЛ УЛЕТЕЛА В ОГОРОД ДУРА ЖОПОЙ МАНДАРИНЫ СОБИРАТЬ ДУРА ЧЕБУРАШКА ЕБАННЯ НАХУЙ ТЫ ЭТИ САМЫЕ МАНДАРИНЫ С ЖОПЫ ВЫПУКИВАЕШЬ ДАУН",
    "СПУКИ СПУКИ СКЕЛЕТОН ДУРА НАХУЙ ТЫ ЖИЗНЕ ХЕНДЛЕС КУПИЛА БЕЗ ГОЛОВЫЙ ПИДОР У ТЯ ЕС ЧЕ ПРАВАЯ СЕЛЬСКАЯ НОГА ЗА УМ ОТВЕЧАЕТ СТРАПОНЕСА ОТБИТАЯ",
    "У ТЕБЯ МАМА МЕРИ ПОПЕНС ПИЗДОЙ КРАБСБУРГЕРЫ ДЕЛАЕТ СВИНЯНЯ ЛАДНО ТЫ ЖОПОЙ БЫЧКИ ПОДНИМАЕШЬ КУРТИЗАНКА МЕСТНАЯ",
    "ЕГО МАМУ ОТПИДОРИЛИ 2 БОМБОРДИРО КРОКОДИЛО У НЕГО ЛИЦО ПОСЛЕ ЭТОГО ТИПО ТУНТУНТУНТУНТУН САХУР ЕБАЛ ТЯ ФРИК",
    "КАРАБАС БАРАБАС КРИВОРЫЛЫЙ ДИМДИМЫЧЬ ЕБАНЫЙ С ПОМОГАТОРОМ В ЖОПЕ ДАЖЕ ТВОИ ФИКСИКИ НЕ ИСПРАВЯТ ТВОИ ГОВНОПАНЧИ АЛАХКБАР ЖОПОЙ СДЕЛАЙ",
    "ТЕБЯ ПАПУАСЫ АТАКУЮТ ТЫ СИСЬКАМИ МАТЕРИ ОТБИВАТЬСЯ НАЧАЛ ВНАТУРЕ КОЖЕНОЕ ИЗДЕЛИЕ У ТЕБЯ ПАПА ПОД ПЛИНТУС ПОДСТИЛИЛСЯ ЧТОБ ОБ НЕГО ВСЕ НОГИ ВЫТЕРЯЛИ",
    "СТАКАН ВЕЛИКАН ВЕЛЕКОДУШНЫЙ СЫН ШЛЮХИ ТЫ ЖОПОЙ ОРБИЗАМИ КОНЧАЕШЬ И КРИЧИШЬ ТРАЛАЛЕЛО ТРАЛАЛА",
    "Я ТЯ В ТВОЕМ СЕЛЕ ТЕБЯ ГРИГОРИМЛЕНА НОСАТОГО КАК ФУФУЛШМЕРЦА ТРАХАЛ ЕБАНУТЫЙ ПИДОР НОСОМ АВИКАТАСТРОФЫ ПРИНИМАЕТ",
    "Я ЩАС СВОИМ МЕЖ НОЖНЫМ РУСИФИКАТОРОМ ТЯ ПОТЫКАЮ ОПРОКИНУ ТЯ ДЕВОЧКА МАЛЕНЬКАЯ САЛЬНО ГОЛОВАЯ",
    "ТАК ВСЕМ ПРИВЕТ ЭТО Я ПАПОЧКА БАКИ, А ВОТ Я ВИЖУ ДАУНА, ЭТО ТОТ САМЫЙ СПОЧНБОБ КВДАРАТНЫЙ КУБИК КОТОРЫЙ СЕБЕ ГИРИ НА ЕБАЛО УРАНИЛ, КРАСАВА, АЛЛАХ АКБАР, В ПОЧЕТЕ У ПАРАШИ ТЕПЕРЬ БУДЕШЬ",
    "ЕСЛИ ЧТО У ДАУНА ПОХОДКА В РЕАЛЬНЫЙ ЖИЗНИ КАК В РОБЛОКСЕ, НА 1 НОГИ ПОДПРИГИВАЕТ ДАУН",
    "ТВОЯ МАМА СЛУЧАЙНО НЕ КОЛОБОК 26 ГОДА, А ЧЕ ОНА НА МОЙ ХУЙ КАК С ЭВЕРЕСТА ПОКАТИЛАСЬ",
    "ЧЕЛОВЕК БУРМАЛДА, ЕГО БАБКА В СОБАЧЬЕЙ БУТКИ ЗАПЕРЛА, ЧИСТО ПОГОНЯЛО У ПАРАШИ: ОТРЫЖКА СВИНЬИ, КЛИКУХА: БАРАНЬЯ ЖОПА",
    "УСЛЫШАЛ ЖИТЕЛЬ КУРИНОЙ МАССЫ, КУРОЧКА РЯБА, КОРМУШКА ДЛЯ ОСЛОВ, ГРОМКИЙ НО ОПАСНЫЙ, ЧИСТО ЗВУЧИТ ГРОЗНО НО НА САМОМ ДЕЛЕ ЗАЛУПА ЕБАННАЯ: СЕЛЬСКИЙ ВОЛКОДАВ, ОХРАНИК В СЕЛЬСКОМ ПОДВАЛЕ, МЕНЕДЖЕР КОМПАНИЯ АЛИБАБА АХЛЕ АХЛЕМА",
    "ЕСЛИ ЧТО ПРОСТО К СЛОВУ, ОН ЕБАННЫЙ РОБОТ ПЫЛЕСОС, 67ВОЛЬТ ПИТАНИЕ У ДАУНА, ВЕНТИЛЯТОР МЕСТНЫЙ, ВОЗДУШНАЯ БУМАЖНАЯ АТАКА, КТО ТЕБЕ РАЗРЕШАЛ ВКЛЮЧАТЬСЯ, МУХОБОЙКА ЕБАННАЯ, ОСВИЖИТЕЛЬ ВОЗДУХА",
    "ЧИСТО ТЕОРЕТИЧЕСКИЙ НА ДРУГОЙ ПЛАНЕТЕ ТЫ ТАНОС С 4 КАМНЯМИ БЕССКОНЕЧНОСТИ, А ТУТ ТЫ КАЛЬКУТОР ЕБАННЫЙ С ПОГОНЯЛ ШЕРСТЯНОЙ",
    "КОРОЧЕ ПРЕДСТАВЬТЕ, ЭТОТ ДАУН РАЗОЗЛИЛСЯ НА ЕГО ПО ЛЕВОЙ ЧАСТИ ПЯТКИ ОТЧИМА, ПОШЕЛ ЕГО ОТПИЗДИТЬ, ВОЗОМНИЛ СЕБЯ МАЙК ТАЙСОНОМ, ЧИСТО ДАУН СПОДСКОЗЬНУЗЛСЯ, ПЕРЕВЕРНУЛСЯ, НАЕБНУЛСЯ И ЛИЦОМ В ГОВНО СОБАКИ МУТАНТА 3 НОГОЙ С ЧЕРНОБЫЛЯ",
    "НОРМЛАЬНО ДАУН ПЕРЕИГРАЛ В ФРИФАЕР, ОДЕЛ СЕБЕ СКОВОРОДУ НА ГОЛОВУ, ПОШЕЛ ПИЗДИТЬСЯ С БОМЖОМ У ПОДЬЕЗДА, ТОТ ЗАБРАЛИ СКВОРАДУ И ОТПИЗДИЛ ЕГО, ЧИСТО ГОРИЛАВОЗ",
    "БАШМАК ЕБАННЫЙ БУКВАЛЬНО ТЫ ХУЕТА КРИПОВАЯ С ЕБАЛО НА НОЛЬ ВЫКРУЧИНЫМ ДЕВЯТКА ПЕРЕВЕРНУТАЯ",
    "Я ХУЙ ЕГО ЗНАЕТ БРАТ ОЛЕГА МАНГОЛА ЛОБОТРЯС ЕБАННЫЙ С КРУЖИВНЫМИ ТРУСАМИ НА ЛИЦЕ С ЧЕРКАШОМ СПИД БУСТ ЕПТА ЕБАТЬ МОИ ЯЙЦА У ТЕБЯ НА ЛИЦЕ БРЫКАЮТСЯ",
    "АЛЁ ДАЛБОЕБ ТЫ КЕГЛЯ ЕБАННАЯ ХОДЯЧАЯ С ФИНИКАМИ В ЖОПЕ Я ВОБЩЕ В АХУЕ ЭТОТ СКИНВОЛКЕР ТУПО НА ПАЛЬЦАХ СТОЙКУ ДЛЯ МИНЕТА СДЕЛАЛ ТАК ЕЩЕ И ЯЗЫКОМ КОВРИК ДЛЯ МАШИНЫ ВЫЛЕЗАЛ",
    "ХУЙНЯ ЕБАННАЯ ТУПАЯ ПОЧЕШИ МОЙ ЛАБОК НОСОМ ГОРГОМЕЛЬ ПРЫЩЯВЫЙ",
    "Я ХУЕЮ С ТЕБЯ ДАЛБОЕБ С ЧЕРЕШНЕЙ ВМЕСТО ЛИЦА Я ТЕБЕ ПРОСТО СКРАМБЕЛ НА ЕБАЛЬНИКЕ СПЕРМОЙ НАРИСОВАЛ",
    "ТЫ ДАЛБОЕБ СВОЕЙ МАМЕ ДОМКРАДОМ ЖОПУ ВСКРЫВАЛ",
    "ФЕРМЕР ХЗ КУРНИК ЕБАННЫЙ КРУПУ ДЛЯ КУР КЛЮЕТ ДУМАЕТ ЧТО ХЛОПЬЯ ЕБАНАТ",
    "Я ТВОЮ МАТЬ ЕБАЛ КАРАБАС БАРАБАС КРИВОРЫЛЫЙ У ТЕБЯ ЧЕЛЮСТЬ ДО ПЯТОК СВИСАЕТ ЕБАНАШКА КОНЧЕННАЯ",
    "ПРОСТО У ДАЛБОЕБА ЗАБОЛЕВАНИЕ ЧЕСОТКИ БОМЖА НА УЛИЦЕ ПРОСТИТУТКА КОНЧЕННАЯ НА ТВОЮ ЖОПУ ИНГАБУТОРЫ НАПРАВЛЕННЫЙ БОЙСЯ",
    "А ЕЩЕ ЭТО ПИЗДА СИДИТ ПАЦАН В БАНАНОВЫХ КАЛГОТКАХ А ЕЩЕ И МИНЬЕНЫ РАЗГОВАРИВАТЬ УЧИЛИ ЧТО ЭТО АПППААПА",
    "ПИЗДЕЦ ХУИЛА У ТЕБЯ РОТ КАК ПЕПЕЛЬНИЦА ДЛЯ ХУЕВ ИСПОЛЬЗУЕТСЯ ЩА ПОДОЖДИ ЗАТУШУ НИХУЯ ХВАЫФХЩЗВ",
    "СМОТРИТЕ ТАМ ЕГО БАБКА КАЧЕРГА НАПЕРЕГОНКИ С ПИСЬКАМИ БИЖИТ НИХУЯ СТАРУХА ФЛЕКСИТ",
    "ЕБАНУТЫЙ ТЫ АПАРЕБРИК СЕБЕ ГЛАЗА ВЫКАЛОЛ В ЖОПУ УЖАЛЕННЫЙ КОНЧЕННЫЙ ДАУН ПОШЕЛ НАХУЙ",
    "МАСТУРБЕК ОБДРИСТАНЫЙ СУПЕР ЧЕРВИЧЕК ВЫТЕРТЫЙ У ТЕБЯ ЗУБЫ ВО РТУ В ЗАБОР ПОСТРОИЛИСЬ НА ПЕРВЫЙ ВТОРОЙ РОСЩИТАЙСЬ",
    "В ТЕБЯ МАТЬ ПЕРДИТ ТОКСИЧНЫМИ ВЕЩЕСТВАМИ ЕБАНАТ ТЫ РОДИЛСЯ ОТ СУПЕР МАМЫ И ОТ ЧУДО ПАПЫ",
    "ПОЕШЛ НАХАЙ ПРИШЕЛЕЦ ЧУВЫРЛА С 3 НОГОЙ БЕЗНОЖНОЙ НА БОРТУ ДОБРОЕ УТРО РОЗБУДИЛ ПАПОЧКУ МИНЕТОМ",
    "НОРМАЛЬНО СТУКНУЛ СЕБЯ ПЯТКОЙ ПО ЛБУ УШЕЛ НА ЛУНУ Я ТЕБЯ ВЫПОТРОШУ СУЧКА",
    "У ТЕБЯ БАТЯ ЖОПУ ТЕ ПУПКОМ КОВЫРЯЕТ НОГТЬОМ НА МЕЗИНЦЕ Я ТЕБЕ ТВОИ ПРОТЕЗЫ НА ЗЕДНЕЦЫ ВЫКРУЧУ",
    "ХОДЯЩИЯ КУТИКУЛА ЕБАЛЬНИК СВОЙ ВТОПИ",
    "ТЕБЕ ТВОЙ ПАПА БЛЕК НА СОБРАНИЕ МУСУЛЬМАНИНОВ ЖОПУ РВАЛ КОГДА ТЫ МАЛЕНЬКАЯ ЖЕНЩИНА С ФИТ ДЖАБОМ НА БАШКЕ",
    "У ТВОЕЙ МАТЕРИ ПЛАКАТ МАЙКЛ ДЖЕКСОНА В ВАНОЙ ГДЕ ОН СВОЕГО БИЛИДЖИНА НАТИРАЕТ НОСОВЫМ ПЛАТКОМ ТВОЕЙ МАТЕРИ ОДНОРУКОЙ ПИЗДЫ НЕМОЙ",
]

DEFAULT_CONFIG = {
    "DELAY_BETWEEN_LETTERS": [0.01, 0.05],
    "DELAY_BETWEEN_WORDS":   [0.01, 0.02],
    "NEIGHBOR_CHANCE":       0.07,
    "DOUBLE_CHANCE":         0.05,
    "ENTER_AFTER_WORDS_MIN": 6,
    "ENTER_AFTER_WORDS_MAX": 25,
    "START_DELAY":           3.0,
    "ENTER_EXTRA_CHANCE":    0.30,
    "ENTER_EXTRA_MIN":       1,
    "ENTER_EXTRA_MAX":       5,
    "WORD_WEIGHTS":          {},
    "DEFAULT_WORD_WEIGHT":   1.0,
    "NEW_WORD_BONUS":        3.0,
    "REPLICA_CHANCE":        0.15,
    "REPLICAS": [
        "ИДИ НАХУЙ", "ТЫ ЧЁ ТУПОЙ", "ЛОХ ПОЗОРНЫЙ", "СОСИ БОЛЬШЕ",
        "ТЫ ЧЁ ДЕБИЛ", "ИДИ ЛЕЧИСЬ", "ТЫ КОНЧЕНЫЙ", "ТЫ БОЛЬНОЙ",
        "ТЕБЕ ЛЕЧИТЬСЯ НАДО", "ТЫ ЧЁ СОВСЕМ ТУПОЙ", "ИДИ ПРОСПИСЬ",
        "ТЫ ЧЁ АЛКАШ", "ИДИ РАБОТАЙ", "ТЫ ЧЁ НИЩИЙ", "ИДИ МОЙСЯ",
        "ТЫ ЧЁ НЕМЫТЫЙ", "ИДИ УЧИСЬ", "ТЫ ЧЁ ДВОЕШНИК",
        "ИДИ НА ЗАВОД", "ТЫ ЧЁ БЕЗДАРЬ", "ТЫ ЧЁ НОЛЬ",
        "ИДИ ПЛАЧЬ", "ТЫ ЧЁ ПЛАКСА", "ИДИ К МАМЕ", "ТЫ ЧЁ МАЛЕНЬКИЙ",
        "ИДИ СПАТЬ", "ТЫ ЧЁ УСТАЛ", "ИДИ ОТДОХНИ", "ТЫ ЧЁ ВЫГОРЕЛ",
        "ТЫ ЧЁ КЛОУН", "ИДИ ТУДА", "ТЫ ЧЁ ШУТ", "ТЫ ЧЁ ЛОХ",
        "ИДИ ПРОВЕРЬСЯ", "ТЫ ЧЁ БОЛЬНОЙ НА ГОЛОВУ", "ИДИ К ВРАЧУ",
        "ТЫ ЧЁ НЕНОРМАЛЬНЫЙ", "ИДИ СПОКОЙНО", "ТЫ ЧЁ ПСИХ",
        "ИДИ ДОМОЙ", "ТЫ ЧЁ БЕЗ ДОМА", "ИДИ СПИ", "ТЫ ЧЁ НЕ СПАЛ",
        "ИДИ ЕШЬ", "ТЫ ЧЁ ГОЛОДНЫЙ", "ИДИ ПЕЙ", "ТЫ ЧЁ ОБЕЗВОЖЕН",
        "ИДИ ДЫШИ", "ТЫ ЧЁ ЗАДОХСЯ", "ИДИ ЖИВИ", "ТЫ ЧЁ МЁРТВЫЙ",
    ],
    "PUNCH_CHANCE": 0.20,
    "PUNCHES": DEFAULT_PUNCHES,
}

DEFAULT_WORDS = [
    "ТЫ", "БЛЯДЬ", "НАХУЙ", "СУКА", "ХУЕСОС",
    "БОЛЬНОЙ", "ПИДОРАС", "ПИДОРИЩЕ", "ТУПОЙ", "ЧМО",
    "СВИНЬЯ", "МАТЬ", "ДАЛБАЕБ", "ДУРА",
    "ГАНДОНИЩЕ", "ХУЕТА", "ЗАЛУПИЩЕ", "БЛЯДИНА", "МРАЗЬ",
    "ГОВНО", "ТВАРЬ", "ТУПАЯ", "БОЛЬНАЯ",
    "ЧМЫРИЛО", "ЗАЛУПА", "ГОВНОПРИЕМИЩЕ", "ХУЕТЕНЬ", "ПОНОС",
    "УЕБИЩЕ", "УЕБОК", "ДОЛБОЕБ", "МУДИЛА", "ДЕБИЛ",
    "КРЕТИН", "ИДИОТ", "ОЛЕНЬ", "ЛОХ", "ЛОШАРА",
    "НИЩЕБРОД", "ОТБРОС", "ПОМОЙКА", "КЛОУН", "ШУТ",
    "БЫДЛО", "ХАМЛО", "МРАЗОТА", "ПОДСТИЛКА", "ШЛЮХА",
    "ПРОСТИТУТКА", "ШАЛАВА", "БЛЯДИЩЕ", "ПИЗДА", "ПИЗДЕЦ",
    "ПИЗДЮК", "ХУЙ", "ХУЙНЯ", "ХУЙЛО", "ЗАЛУПОК",
    "ЕБЛАН", "ЕБЛО", "ЕБАНАТ", "ЕБУЧИЙ", "ЕБНУТЫЙ",
    "СУЧАРА", "СУЧКА", "СУЧИЙ", "МУДАК", "МУДОЗВОН",
    "ПЕДИК", "ПИДОР", "ПИДРИЛА", "ГОМОСЕК", "ГЕЙ",
    "ТВАРИНА", "СКОТИНА", "ЖИВОТНОЕ", "СВИНОТА", "СКОТ",
    "НЕДОУМОК", "НЕДОНОСОК", "ВЫРОДОК", "УРОД", "УРОДИНА",
    "УБЛЮДОК", "МЕРЗАВЕЦ", "ПОДЛЕЦ", "ГАД", "ГАДИНА",
    "ЗМЕЙ", "КРЫСА", "ПАДАЛЬ", "ПАДЛА", "СТЕРВА",
    "ДЕРЬМО", "ДРЯНЬ", "ШВАЛЬ", "ШУШЕРА", "ШВАБРА",
    "ЛОХУДРА", "ЛОХУШКА", "ЛОХМАТЫЙ", "ОБОРВАНЕЦ", "БОМЖ",
    "АЛКАШ", "ПЬЯНЬ", "НАРКОМАН", "ТОРЧОК", "ДЕБИЛОИД",
    "КУСОК ДЕРЬМА", "МЕШОК С ГОВНОМ", "ХОДЯЧЕЕ ГОВНО",
    "ТУПОЕ ЖИВОТНОЕ", "ЖАЛКОЕ ПОДОБИЕ", "НИЧТОЖЕСТВО",
    "ПУСТОЕ МЕСТО", "НОЛЬ БЕЗ ПАЛОЧКИ", "ОШИБКА ПРИРОДЫ",
    "БРАК ПРОИЗВОДСТВА", "НЕДОРАЗУМЕНИЕ", "ОТХОДЫ ЖИЗНИ",
    "ПОДЗАБОРНАЯ ШЛЮХА", "ДЕШЕВАЯ БЛЯДЬ", "ГРЯЗНАЯ СУКА",
    "ЖАЛКИЙ ЧЕРВЬ", "МЕЛКИЙ ЧЕРВЬ", "ТУПОЙ БАРАН",
    "ЖИРНАЯ СВИНЬЯ", "ГРЯЗНАЯ КРЫСА", "ТРУСЛИВЫЙ ШАКАЛ",
    "ПАРШИВАЯ ОВЦА", "ШЕЛУДИВАЯ СОБАКА", "БЕШЕНАЯ СУКА",
    "КОНЧЕНЫЙ ДЕБИЛ", "ПОЛНЫЙ ИДИОТ", "АБСОЛЮТНЫЙ НОЛЬ",
    "ЖАЛКОЕ НИЧТО", "ЖАЛКИЙ УБЛЮДОК", "ЖАЛКИЙ ЛОХ",
    "КОНЧЕННЫЙ ЛОХ", "ОБЫЧНЫЙ ЛОХ", "ПРОСТО ЧМО",
]

NEIGHBORS = {
    'й': 'цфы', 'ц': 'йувы', 'у': 'цкыв', 'к': 'уеап', 'е': 'кнра',
    'н': 'егпо', 'г': 'ншлр', 'ш': 'гщдл', 'щ': 'шзжд', 'з': 'щхэж',
    'х': 'зъэ', 'ъ': 'хэ',
    'ф': 'йяыц', 'ы': 'фвц', 'в': 'ыуас', 'а': 'впке', 'п': 'арн',
    'р': 'пого', 'о': 'рлшг', 'л': 'одш', 'д': 'лжщш', 'ж': 'дэз',
    'э': 'жх',
    'я': 'чф', 'ч': 'яс', 'с': 'чмв', 'м': 'сит', 'и': 'мьб',
    'т': 'иьн', 'ь': 'тб', 'б': 'ьюи', 'ю': 'б',
    '1': '2', '2': '13', '3': '24', '4': '35', '5': '46',
    '6': '57', '7': '68', '8': '79', '9': '80', '0': '9-',
}

user32 = ctypes.WinDLL('user32', use_last_error=True)
user32.SendInput.argtypes = (wintypes.UINT, ctypes.c_void_p, ctypes.c_int)
user32.SendInput.restype  = wintypes.UINT

INPUT_KEYBOARD    = 1
KEYEVENTF_KEYUP   = 0x0002
KEYEVENTF_UNICODE = 0x0004
VK_RETURN = 0x0D
VK_SPACE  = 0x20
VK_ESC    = 0x1B
VK_F5     = 0x74

ULONG_PTR = ctypes.c_size_t

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk",         wintypes.WORD),
        ("wScan",       wintypes.WORD),
        ("dwFlags",     wintypes.DWORD),
        ("time",        wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx",          wintypes.LONG),
        ("dy",          wintypes.LONG),
        ("mouseData",   wintypes.DWORD),
        ("dwFlags",     wintypes.DWORD),
        ("time",        wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg",    wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]

class _INPUTunion(ctypes.Union):
    _fields_ = [("ki", KEYBDINPUT), ("mi", MOUSEINPUT), ("hi", HARDWAREINPUT)]

class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("union", _INPUTunion)]

def _send(ki):
    inp = INPUT(type=INPUT_KEYBOARD)
    inp.union.ki = ki
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

def type_unicode_char(ch):
    code = ord(ch)
    _send(KEYBDINPUT(wVk=0, wScan=code, dwFlags=KEYEVENTF_UNICODE, time=0, dwExtraInfo=0))
    _send(KEYBDINPUT(wVk=0, wScan=code, dwFlags=KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, time=0, dwExtraInfo=0))

def press_vk(vk):
    _send(KEYBDINPUT(wVk=vk, wScan=0, dwFlags=0, time=0, dwExtraInfo=0))
    _send(KEYBDINPUT(wVk=vk, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=0))

def press_space(): press_vk(VK_SPACE)
def press_enter(): press_vk(VK_RETURN)

def is_key_down(vk):
    return (user32.GetAsyncKeyState(vk) & 0x8000) != 0

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=2)
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==================== АВТООБНОВЛЕНИЕ ====================
def github_raw_url(path):
    return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{path}"

def fetch_text(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return r.read().decode("utf-8")

def check_updates():
    try:
        manifest = json.loads(fetch_text(github_raw_url("manifest.json")))
    except Exception:
        return False

    remote_ver = manifest.get("version", "0.0.0")
    local_ver = globals().get("__version__", "0.0.0")

    if remote_ver == local_ver:
        return False

    print(f"Доступно обновление: {local_ver} -> {remote_ver}")
    ans = input("Обновить? (y/n): ").strip().lower()
    if ans != "y":
        return False

    script_dir = os.path.dirname(os.path.abspath(__file__))
    protected = set(UPDATE_PROTECTED)
    downloaded = []

    try:
        for fname in manifest.get("files", []):
            if fname in protected:
                continue
            url = github_raw_url(fname)
            data = fetch_text(url).encode("utf-8")
            tmp_path = os.path.join(script_dir, fname + ".new")
            with open(tmp_path, "wb") as f:
                f.write(data)
            downloaded.append((tmp_path, os.path.join(script_dir, fname)))
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        for tmp, _ in downloaded:
            try: os.remove(tmp)
            except: pass
        return False

    self_path = os.path.abspath(__file__)
    self_updated = any(dst == self_path for _, dst in downloaded)

    if not self_updated:
        for tmp, dst in downloaded:
            os.replace(tmp, dst)
        print("Обновление установлено. Перезапусти скрипт.")
        return True

    bat_path = os.path.join(script_dir, "_update.bat")
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("timeout /t 2 /nobreak >nul\n")
        for tmp, dst in downloaded:
            f.write(f'move /Y "{tmp}" "{dst}"\n')
        f.write(f'start "" "{sys.executable}" "{self_path}"\n')
        f.write("del \"%~f0\"\n")

    print("Перезапуск для применения обновления...")
    os.startfile(bat_path)
    sys.exit(0)
# =====================================================

config = load_json(CONFIG_FILE, DEFAULT_CONFIG)
words  = load_json(WORDS_FILE, DEFAULT_WORDS)

if not isinstance(config.get("DELAY_BETWEEN_LETTERS"), list) or len(config["DELAY_BETWEEN_LETTERS"]) != 2:
    config["DELAY_BETWEEN_LETTERS"] = DEFAULT_CONFIG["DELAY_BETWEEN_LETTERS"]
if not isinstance(config.get("DELAY_BETWEEN_WORDS"), list) or len(config["DELAY_BETWEEN_WORDS"]) != 2:
    config["DELAY_BETWEEN_WORDS"] = DEFAULT_CONFIG["DELAY_BETWEEN_WORDS"]
for k, v in DEFAULT_CONFIG.items():
    config.setdefault(k, v)
save_json(CONFIG_FILE, config)
if not words:
    words = list(DEFAULT_WORDS)
    save_json(WORDS_FILE, words)

running = False
typing_thread = None
typed_history = collections.Counter()
punch_pool = []

def mutate_letter(letter):
    result = letter
    if random.random() < config["NEIGHBOR_CHANCE"]:
        neighbors = NEIGHBORS.get(letter.lower())
        if neighbors:
            neighbor = random.choice(neighbors)
            if letter.isupper():
                neighbor = neighbor.upper()
            result = neighbor
    if random.random() < config["DOUBLE_CHANCE"]:
        result = result + result
    return result

def type_word(word, on_space=None):
    for ch in word:
        if not running:
            return False
        if ch == " ":
            press_space()
            time.sleep(random.uniform(*config["DELAY_BETWEEN_WORDS"]))
            if on_space is not None:
                on_space()
            continue
        out = mutate_letter(ch)
        for c in out:
            if not running:
                return False
            type_unicode_char(c)
            time.sleep(random.uniform(*config["DELAY_BETWEEN_LETTERS"]))
    press_space()
    time.sleep(random.uniform(*config["DELAY_BETWEEN_WORDS"]))
    return True

def pick_word():
    if not words:
        return None
    weights = []
    for w in words:
        base = config["WORD_WEIGHTS"].get(w, config["DEFAULT_WORD_WEIGHT"])
        if typed_history[w] == 0:
            base *= config["NEW_WORD_BONUS"]
        weights.append(base)
    total = sum(weights)
    if total <= 0:
        return random.choice(words)
    r = random.uniform(0, total)
    acc = 0.0
    for w, wt in zip(words, weights):
        acc += wt
        if r <= acc:
            return w
    return words[-1]

def typing_loop():
    global running, punch_pool
    words_typed = 0
    next_enter_at = random.randint(config["ENTER_AFTER_WORDS_MIN"], config["ENTER_AFTER_WORDS_MAX"])
    force_word_next = False

    def maybe_enter():
        nonlocal words_typed, next_enter_at
        words_typed += 1
        if words_typed >= next_enter_at:
            press_enter()
            words_typed = 0
            next_enter_at = random.randint(config["ENTER_AFTER_WORDS_MIN"], config["ENTER_AFTER_WORDS_MAX"])
            if random.random() < config["ENTER_EXTRA_CHANCE"]:
                next_enter_at += random.randint(config["ENTER_EXTRA_MIN"], config["ENTER_EXTRA_MAX"])

    while running:
        if force_word_next:
            text = pick_word()
            if text is None:
                break
            force_word_next = False
            is_punch = False
        else:
            r = random.random()
            if punch_pool and r < config["PUNCH_CHANCE"]:
                idx = random.randrange(len(punch_pool))
                text = punch_pool.pop(idx)
                is_punch = True
                force_word_next = True
            elif config["REPLICAS"] and r < config["PUNCH_CHANCE"] + config["REPLICA_CHANCE"]:
                text = random.choice(config["REPLICAS"])
                is_punch = False
            else:
                text = pick_word()
                if text is None:
                    break
                is_punch = False

        if is_punch:
            if not type_word(text, on_space=maybe_enter):
                break
            maybe_enter()
        else:
            if not type_word(text):
                break
            maybe_enter()

        typed_history[text] += 1

def start_typing():
    global running, typing_thread, punch_pool
    if running:
        return
    if not words and not config["REPLICAS"] and not config["PUNCHES"]:
        print("НЕТ НИ СЛОВ, НИ РЕПЛИК, НИ ПАНЧЕЙ ДЛЯ ПЕЧАТИ.")
        return
    punch_pool = list(config["PUNCHES"])
    running = True
    time.sleep(config["START_DELAY"])
    if not running:
        return
    typing_thread = threading.Thread(target=typing_loop, daemon=True)
    typing_thread.start()

def stop_typing():
    global running
    running = False

def ask(prompt, default, cast):
    raw = input(f"{prompt} [{default}]: ").strip()
    if raw == "":
        return default
    try:
        return cast(raw)
    except Exception:
        print("НЕВЕРНЫЙ ФОРМАТ, ОСТАВЛЯЮ СТАРОЕ ЗНАЧЕНИЕ.")
        return default

def settings_menu():
    global config, words
    while True:
        clear()
        print("=" * 60)
        print(" НАСТРОЙКИ")
        print("=" * 60)
        print(f" 1. Задержка между буквами (мин/макс), сек: {config['DELAY_BETWEEN_LETTERS']}")
        print(f" 2. Задержка между словами (мин/макс), сек: {config['DELAY_BETWEEN_WORDS']}")
        print(f" 3. Шанс опечатки (соседняя буква), 0..1: {config['NEIGHBOR_CHANCE']}")
        print(f" 4. Шанс двойной буквы, 0..1: {config['DOUBLE_CHANCE']}")
        print(f" 5. Мин. слов до Enter: {config['ENTER_AFTER_WORDS_MIN']}")
        print(f" 6. Макс. слов до Enter: {config['ENTER_AFTER_WORDS_MAX']}")
        print(f" 7. Задержка перед стартом, сек: {config['START_DELAY']}")
        print(f" 8. Шанс 'Enter позже' (0..1): {config['ENTER_EXTRA_CHANCE']}")
        print(f" 9. Мин. доп. слов при 'позже': {config['ENTER_EXTRA_MIN']}")
        print(f"10. Макс. доп. слов при 'позже': {config['ENTER_EXTRA_MAX']}")
        print(f"11. Базовый вес слова: {config['DEFAULT_WORD_WEIGHT']}")
        print(f"12. Бонус новым словам (x раз): {config['NEW_WORD_BONUS']}")
        print(f"13. Веса отдельных слов ({len(config['WORD_WEIGHTS'])} шт.)")
        print(f"14. Редактировать список слов ({len(words)} шт.)")
        print(f"15. Шанс реплики (0..1): {config['REPLICA_CHANCE']}")
        print(f"16. Редактировать реплики ({len(config['REPLICAS'])} шт.)")
        print(f"17. Шанс панча (0..1): {config['PUNCH_CHANCE']}")
        print(f"18. Редактировать панчи ({len(config['PUNCHES'])} шт.)")
        print(" 0. НАЗАД")
        print("=" * 60)
        choice = input("ВЫБОР: ").strip()

        if choice == "0":
            save_json(CONFIG_FILE, config)
            return
        elif choice == "1":
            a = ask("Мин. задержка между буквами (сек)", config["DELAY_BETWEEN_LETTERS"][0], float)
            b = ask("Макс. задержка между буквами (сек)", config["DELAY_BETWEEN_LETTERS"][1], float)
            config["DELAY_BETWEEN_LETTERS"] = [a, b]
        elif choice == "2":
            a = ask("Мин. задержка между словами (сек)", config["DELAY_BETWEEN_WORDS"][0], float)
            b = ask("Макс. задержка между словами (сек)", config["DELAY_BETWEEN_WORDS"][1], float)
            config["DELAY_BETWEEN_WORDS"] = [a, b]
        elif choice == "3":
            config["NEIGHBOR_CHANCE"] = ask("Шанс опечатки (0..1)", config["NEIGHBOR_CHANCE"], float)
        elif choice == "4":
            config["DOUBLE_CHANCE"] = ask("Шанс двойной буквы (0..1)", config["DOUBLE_CHANCE"], float)
        elif choice == "5":
            config["ENTER_AFTER_WORDS_MIN"] = ask("Мин. слов до Enter", config["ENTER_AFTER_WORDS_MIN"], int)
        elif choice == "6":
            config["ENTER_AFTER_WORDS_MAX"] = ask("Макс. слов до Enter", config["ENTER_AFTER_WORDS_MAX"], int)
        elif choice == "7":
            config["START_DELAY"] = ask("Задержка перед стартом (сек)", config["START_DELAY"], float)
        elif choice == "8":
            config["ENTER_EXTRA_CHANCE"] = ask("Шанс 'Enter позже' (0..1)", config["ENTER_EXTRA_CHANCE"], float)
        elif choice == "9":
            config["ENTER_EXTRA_MIN"] = ask("Мин. доп. слов", config["ENTER_EXTRA_MIN"], int)
        elif choice == "10":
            config["ENTER_EXTRA_MAX"] = ask("Макс. доп. слов", config["ENTER_EXTRA_MAX"], int)
        elif choice == "11":
            config["DEFAULT_WORD_WEIGHT"] = ask("Базовый вес слова", config["DEFAULT_WORD_WEIGHT"], float)
        elif choice == "12":
            config["NEW_WORD_BONUS"] = ask("Бонус новым словам (x раз)", config["NEW_WORD_BONUS"], float)
        elif choice == "13":
            weights_menu()
        elif choice == "14":
            words_menu()
        elif choice == "15":
            config["REPLICA_CHANCE"] = ask("Шанс реплики (0..1)", config["REPLICA_CHANCE"], float)
        elif choice == "16":
            replicas_menu()
        elif choice == "17":
            config["PUNCH_CHANCE"] = ask("Шанс панча (0..1)", config["PUNCH_CHANCE"], float)
        elif choice == "18":
            punches_menu()
        save_json(CONFIG_FILE, config)

def weights_menu():
    global config
    while True:
        clear()
        print("=" * 50)
        print(f" ВЕСА СЛОВ ({len(config['WORD_WEIGHTS'])} записей)")
        print("=" * 50)
        for w, wt in config["WORD_WEIGHTS"].items():
            print(f" {w} = {wt}")
        print("=" * 50)
        print(" A. ДОБАВИТЬ/ИЗМЕНИТЬ ВЕС")
        print(" D. УДАЛИТЬ ВЕС")
        print(" R. СБРОСИТЬ ВСЕ ВЕСА")
        print(" 0. НАЗАД")
        print("=" * 50)
        choice = input("ВЫБОР: ").strip().lower()
        if choice == "0":
            save_json(CONFIG_FILE, config)
            return
        elif choice == "a":
            w = input("СЛОВО: ").strip()
            if w:
                try:
                    wt = float(input("ВЕС: ").strip())
                    config["WORD_WEIGHTS"][w] = wt
                    save_json(CONFIG_FILE, config)
                except Exception:
                    print("НЕВЕРНЫЙ ВЕС.")
                    time.sleep(1)
        elif choice == "d":
            w = input("СЛОВО ДЛЯ УДАЛЕНИЯ ВЕСА: ").strip()
            if w in config["WORD_WEIGHTS"]:
                del config["WORD_WEIGHTS"][w]
                save_json(CONFIG_FILE, config)
        elif choice == "r":
            config["WORD_WEIGHTS"] = {}
            save_json(CONFIG_FILE, config)

def words_menu():
    global words
    while True:
        clear()
        print("=" * 50)
        print(f" СЛОВА ({len(words)} ШТ.)")
        print("=" * 50)
        for i, w in enumerate(words, 1):
            print(f" {i}. {w}")
        print("=" * 50)
        print(" A. ДОБАВИТЬ СЛОВО")
        print(" D. УДАЛИТЬ СЛОВО")
        print(" C. ЗАМЕНИТЬ СЛОВО")
        print(" R. СБРОСИТЬ К ДЕФОЛТУ")
        print(" 0. НАЗАД")
        print("=" * 50)
        choice = input("ВЫБОР: ").strip().lower()

        if choice == "0":
            save_json(WORDS_FILE, words)
            return
        elif choice == "a":
            w = input("НОВОЕ СЛОВО: ").strip()
            if w:
                words.append(w)
                save_json(WORDS_FILE, words)
        elif choice == "d":
            try:
                idx = int(input("НОМЕР СЛОВА ДЛЯ УДАЛЕНИЯ: ")) - 1
                if 0 <= idx < len(words):
                    words.pop(idx)
                    save_json(WORDS_FILE, words)
            except Exception:
                pass
        elif choice == "c":
            try:
                idx = int(input("НОМЕР СЛОВА ДЛЯ ЗАМЕНЫ: ")) - 1
                if 0 <= idx < len(words):
                    w = input("НОВОЕ ЗНАЧЕНИЕ: ").strip()
                    if w:
                        words[idx] = w
                        save_json(WORDS_FILE, words)
            except Exception:
                pass
        elif choice == "r":
            words = list(DEFAULT_WORDS)
            save_json(WORDS_FILE, words)

def replicas_menu():
    global config
    while True:
        clear()
        print("=" * 50)
        print(f" РЕПЛИКИ ({len(config['REPLICAS'])} ШТ.)")
        print("=" * 50)
        for i, r in enumerate(config["REPLICAS"], 1):
            print(f" {i}. {r}")
        print("=" * 50)
        print(" A. ДОБАВИТЬ РЕПЛИКУ")
        print(" D. УДАЛИТЬ РЕПЛИКУ")
        print(" C. ЗАМЕНИТЬ РЕПЛИКУ")
        print(" R. СБРОСИТЬ К ДЕФОЛТУ")
        print(" 0. НАЗАД")
        print("=" * 50)
        choice = input("ВЫБОР: ").strip().lower()

        if choice == "0":
            save_json(CONFIG_FILE, config)
            return
        elif choice == "a":
            r = input("НОВАЯ РЕПЛИКА: ").strip()
            if r:
                config["REPLICAS"].append(r)
                save_json(CONFIG_FILE, config)
        elif choice == "d":
            try:
                idx = int(input("НОМЕР РЕПЛИКИ ДЛЯ УДАЛЕНИЯ: ")) - 1
                if 0 <= idx < len(config["REPLICAS"]):
                    config["REPLICAS"].pop(idx)
                    save_json(CONFIG_FILE, config)
            except Exception:
                pass
        elif choice == "c":
            try:
                idx = int(input("НОМЕР РЕПЛИКИ ДЛЯ ЗАМЕНЫ: ")) - 1
                if 0 <= idx < len(config["REPLICAS"]):
                    r = input("НОВОЕ ЗНАЧЕНИЕ: ").strip()
                    if r:
                        config["REPLICAS"][idx] = r
                        save_json(CONFIG_FILE, config)
            except Exception:
                pass
        elif choice == "r":
            config["REPLICAS"] = list(DEFAULT_CONFIG["REPLICAS"])
            save_json(CONFIG_FILE, config)

def punches_menu():
    global config
    while True:
        clear()
        print("=" * 50)
        print(f" ПАНЧИ ({len(config['PUNCHES'])} ШТ.)")
        print("=" * 50)
        for i, p in enumerate(config["PUNCHES"], 1):
            print(f" {i}. {p}")
        print("=" * 50)
        print(" A. ДОБАВИТЬ ПАНЧ")
        print(" D. УДАЛИТЬ ПАНЧ")
        print(" C. ЗАМЕНИТЬ ПАНЧ")
        print(" R. СБРОСИТЬ К ДЕФОЛТУ")
        print(" 0. НАЗАД")
        print("=" * 50)
        choice = input("ВЫБОР: ").strip().lower()

        if choice == "0":
            save_json(CONFIG_FILE, config)
            return
        elif choice == "a":
            p = input("НОВЫЙ ПАНЧ: ").strip()
            if p:
                config["PUNCHES"].append(p)
                save_json(CONFIG_FILE, config)
        elif choice == "d":
            try:
                idx = int(input("НОМЕР ПАНЧА ДЛЯ УДАЛЕНИЯ: ")) - 1
                if 0 <= idx < len(config["PUNCHES"]):
                    config["PUNCHES"].pop(idx)
                    save_json(CONFIG_FILE, config)
            except Exception:
                pass
        elif choice == "c":
            try:
                idx = int(input("НОМЕР ПАНЧА ДЛЯ ЗАМЕНЫ: ")) - 1
                if 0 <= idx < len(config["PUNCHES"]):
                    p = input("НОВОЕ ЗНАЧЕНИЕ: ").strip()
                    if p:
                        config["PUNCHES"][idx] = p
                        save_json(CONFIG_FILE, config)
            except Exception:
                pass
        elif choice == "r":
            config["PUNCHES"] = list(DEFAULT_PUNCHES)
            save_json(CONFIG_FILE, config)

def hotkey_listener():
    global running
    while True:
        if is_key_down(VK_ESC):
            running = False
            os._exit(0)
        if is_key_down(VK_F5):
            time.sleep(0.05)
            if running:
                stop_typing()
                print("\n[STOP] ТАЙПИНГ ОСТАНОВЛЕН")
            else:
                threading.Thread(target=start_typing, daemon=True).start()
                print(f"\n[START] ЧЕРЕЗ {config['START_DELAY']} СЕК НАЧНУ ПЕЧАТАТЬ")
            while is_key_down(VK_F5):
                time.sleep(0.02)
        time.sleep(0.02)

def main():
    global running
    check_updates()
    threading.Thread(target=hotkey_listener, daemon=True).start()

    while True:
        clear()
        print("=" * 50)
        print(" АВТО-ТАЙПЕР")
        print("=" * 50)
        print(f" F5  — СТАРТ/СТОП (ЗАДЕРЖКА {config['START_DELAY']} СЕК)")
        print(f" ESC — ВЫХОД")
        print(f" СЛОВ В БАЗЕ: {len(words)}")
        print(f" РЕПЛИК: {len(config['REPLICAS'])}")
        print(f" ПАНЧЕЙ: {len(config['PUNCHES'])}")
        print(f" СТАТУС: {'РАБОТАЕТ' if running else 'ОСТАНОВЛЕН'}")
        print("=" * 50)
        print(" 1. НАСТРОЙКИ")
        print(" 2. СЛОВА")
        print(" 3. РЕПЛИКИ")
        print(" 4. ПАНЧИ")
        print(" 0. ВЫХОД")
        print("=" * 50)
        choice = input("ВЫБОР: ").strip()

        if choice == "0":
            running = False
            time.sleep(0.2)
            return
        elif choice == "1":
            settings_menu()
        elif choice == "2":
            words_menu()
        elif choice == "3":
            replicas_menu()
        elif choice == "4":
            punches_menu()

if __name__ == "__main__":
    main()
