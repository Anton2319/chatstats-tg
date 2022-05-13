# chatstats-tg v1
# Made by aGrIk
# 10.05.2022 - 13.05.2022

from json import loads, dumps
from datetime import datetime
from time import time
from string import punctuation, whitespace, digits

predlogi = "без безо близ в во вместо вне не для до за там из изо изза изпод к ко кроме между меж на над надо о об обо от ото пред перед предо передо по под подо при про ради с со сквозь среди у чрез через".split(" ")
chasticy = "ли разве неужели что а вон вот именно точно раз ровно подлинно как что за тото просто ну прямо еще".split(" ")
mestoimeniya = "я мы ты вы он она оно они себя мой твой ваш все наш меня тебя мною тобою мне тебе нам нас вас свой его ее их то это тот того тем ту тех этот такой таков столько весь всякий сам самый каждый любой иной другой кто что какой какая какие какое каков какова каковы каково чей сколько никто ничто некого нечего никакой ничей нисколько ктото коекто ктонибудь ктолибо чтото коечто чтонибудь чтолибо какойто какойлибо какойнибудь некто нечто некоторый некий".split(" ")
soyuzy = "и да ни тоже также а но однако зато же или либо то ни только если столько сколько сколькими скольких столькими стольких как так хотя но нет что чтобы будто когда пока едва если раз потому ибо дабы хотя хоть пускай как будто словно кто что каков который куда откуда где сколько почему зачем".split(" ")

def deunix(integer):
    return datetime.fromtimestamp(integer).strftime('%Y %m %d %H %M %S').split(" ")

def readableDate(unixtime):
    dex = deunix(unixtime)
    return f"{dex[2]}.{dex[1]}.{dex[0]} {dex[3]}:{dex[4]}:{dex[5]}"

def convertint(stime):
    days = int(stime // 86400)
    mod = int(stime % 86400)
    hours = mod // 3600
    mod = mod % 3600
    minutes = mod // 60
    seconds = mod % 60

    ret = ""
    if days != 0:
        ret += str(days)
        last_days = days % 10
        if last_days == 0 or 5 <= last_days <= 9 or days // 10 == 1:
            ret += " дней "
        elif last_days == 1:
            ret += " день "
        else:
            ret += " дня "

    if hours != 0:
        ret += str(hours)
        last_hours = hours % 10
        if last_hours == 0 or 5 <= last_hours <= 9 or hours // 10 == 1:
            ret += " часов "
        elif last_hours == 1:
            ret += " час "
        else:
            ret += " часа "

    if minutes != 0:
        ret += str(minutes)
        last_minutes = minutes % 10
        if last_minutes == 0 or 5 <= last_minutes <= 9 or minutes // 10 == 1:
            ret += " минут "
        elif last_minutes == 1:
            ret += " минута "
        else:
            ret += " минуты "

    if ret == "" or seconds != 0:
        ret += str(seconds)
        last_sec = seconds % 10
        if last_sec == 0 or 5 <= last_sec <= 9 or seconds // 10 == 1:
            ret += " секунд"
        elif last_sec == 1:
            ret += " секунда"
        else:
            ret += " секунды"
    return ret

def readff(file):
    try:
        Ff = open(file, 'r', encoding='UTF-8')
        Contents = Ff.read()
        Ff.close()
        return Contents
    except:
        return None

def percent(frst, scnd):
    coef = 100 / frst
    gets = scnd * coef
    return gets

def tounix(time):
    return datetime.timestamp(datetime.strptime(time, "%Y-%m-%dT%H:%M:%S"))

def getdate(date):
    array = date.split("T")
    array = array[0].split("-")
    return f"{array[2]}.{array[1]}.{array[0]}"

def writeto(text, target):
    file = open(str(target), 'w', encoding='utf-8')
    file.write(str(text))
    file.close()

template = {
    "name": "",
    "start_time": 0,
    "end_time": 0,
    "names": [],
    "messages": {
        "total": 0,
        "messages": 0,
        "service": 0,
        "stickers": 0,
        "mentions": {},
        "words": {},
        "dates": {}
    },
    "users": {},
    "usernames": {},
    "members": {
        "total": [],
        "current": 0
    },
    "calls": {
        "total": 0,
        "duration": 0
    },
    "processing_time": 0
}

filename = input("Имя файла: ")
start_time = time()
chat = loads(readff(filename))

print("Запуск обработчика...\n")

template["name"] = chat["name"]
template["start_time"] = tounix(chat["messages"][0]["date"])
template["end_time"] = tounix(chat["messages"][-1]["date"])
template["messages"]["total"] = len(chat["messages"])
processed = 0

# Main
for message in chat["messages"]:
    processed += 1
    print(f"Обработка сообщения: {processed}/{len(chat['messages'])} ({round(percent(len(chat['messages']), processed), 4)}%)")

    if "actor_id" in message.keys():
        if not str(message["actor_id"]).startswith("channel"):
            if message["actor"] is None: message["actor"] = "Deleted Account"
            if message["actor_id"] not in template["users"].keys():
                template["users"][message["actor_id"]] = 0
                template["usernames"][message["actor_id"]] = message["actor"]
            template["users"][message["actor_id"]] += 1
    else:
        if not str(message["from_id"]).startswith("channel"):
            if message["from"] is None: message["from"] = "Deleted Account"
            if message["from_id"] not in template["users"].keys():
                template["users"][message["from_id"]] = 0
                template["usernames"][message["from_id"]] = message["from"]
            template["users"][message["from_id"]] += 1

    if getdate(message["date"]) not in template["messages"]["dates"].keys(): template["messages"]["dates"][getdate(message["date"])] = 0
    template["messages"]["dates"][getdate(message["date"])] += 1

    if message["type"] == "message":
        template["messages"]["messages"] += 1
        if type(message["text"]) is list:
            raw_text = ""
            for element in message["text"]:
                if type(element) is dict:
                    if element["type"] == "mention":
                        if element["text"] not in template["messages"]["mentions"].keys():
                            template["messages"]["mentions"][element["text"]] = 0
                        template["messages"]["mentions"][element["text"]] += 1
                    else: raw_text += element["text"]
                else: raw_text += element
            message["text"] = raw_text
        text = message["text"].replace("\n", " ").lower().replace("ё", "е")
        for punc in list(punctuation): text = text.replace(punc, "")
        for whi in list(whitespace): text = text.replace(whi, " ")
        for dig in list(digits): text = text.replace(dig, " ")

        text = text.strip().split(" ")
        for pre in list(predlogi):
            for x in range(text.count(pre)):
                text.remove(pre)
        for cha in list(chasticy):
            for x in range(text.count(cha)):
                text.remove(cha)
        for mes in list(mestoimeniya):
            for x in range(text.count(mes)):
                text.remove(mes)
        for soy in list(soyuzy):
            for x in range(text.count(soy)):
                text.remove(soy)

        for word in text:
            if word:
                if word not in template["messages"]["words"].keys(): template["messages"]["words"][word] = 0
                template["messages"]["words"][word] += 1

        if "media_type" in message.keys():
            if message["media_type"] == "sticker": template["messages"]["stickers"] += 1

    else:
        template["messages"]["service"] += 1
        if message["action"] == "edit_group_title":
            template["names"].append(message["title"])
        elif message["action"] == "group_call" and "duration" in message.keys():
            template["calls"]["total"] += 1
            template["calls"]["duration"] += message["duration"]
        elif message["action"] == "create_group":
            for member in message["members"]:
                template["members"]["total"].append(member)
                template["members"]["current"] += 1
        elif message["action"] == "invite_members":
            for member in message["members"]:
                if member not in template["members"]["total"]: template["members"]["total"].append(member)
                template["members"]["current"] += 1
        elif message["action"] == "join_group_by_link":
            if message["actor"] not in template["members"]["total"]: template["members"]["total"].append(message["actor"])
            template["members"]["current"] += 1
        elif message["action"] == "remove_members":
            for member in message["members"]:
                template["members"]["current"] -= 1

template["processing_time"] = time() - start_time
writeto(dumps(template, ensure_ascii=False), "lastprocessed.json")
print("Генерация отчёта...")

n = "\n"
ret = f"""{"=" * 10}
Статистика Telegram-чата "{template['name']}"
Дата и время составления: {readableDate(time())}

ОБЩАЯ ИНФОРМАЦИЯ
Анализируемый промежуток времени: {readableDate(template['start_time'])} - {readableDate(template['end_time'])} ({convertint(template['end_time'] - template['start_time'])})
Другие названия чата: {n.join(template['names'])}

УЧАСТНИКИ
Всего участников: {len(template['members']['total'])}
Текущих участников: {template['members']['current']}

СООБЩЕНИЯ
Всего: {template['messages']['total']}
Сообщений: {template['messages']['messages']}
Сервисных сообщений: {template['messages']['service']}
Стикеров: {template['messages']['stickers']}
Словарный запас: {len(template['messages']['words'])}

ЗВОНКИ
Звонков: {template['calls']['total']}
Общая длительность звонков: {convertint(template['calls']['duration'])}

20 самых популярных слов:
"""
for word in sorted(template["messages"]["words"], key=template["messages"]["words"].get, reverse=True)[:20]:
    ret += f"{word} - {template['messages']['words'][word]} раз\n"

ret += "\n10 самых частых упоминаний:\n"
for mention in sorted(template["messages"]["mentions"], key=template["messages"]["mentions"].get, reverse=True)[:10]:
    ret += f"{mention} - {template['messages']['mentions'][mention]} раз\n"

ret += "\n7 дней с наибольшим количеством сообщений:\n"
for date in sorted(template["messages"]["dates"], key=template["messages"]["dates"].get, reverse=True)[:7]:
    ret += f"{date} - сообщений: {template['messages']['dates'][date]}\n"

ret += "\nТоп 20 пользователей:\n"
for user in sorted(template["users"], key=template["users"].get, reverse=True)[:20]:
    ret += f"{template['usernames'][user]} - сообщений: {template['users'][user]}\n"

ret += f"\nДлительность обработки: {convertint(template['processing_time'])}"

print(ret)
print("=" * 10)
print("Статистика в машиночитаемом виде сохранена в файле lastprocessed.json.")