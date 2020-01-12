#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import telebot
from bs4 import BeautifulSoup
from emoji import emojize
from user_agent import generate_user_agent

token = "922159497:AAF7sV5ZirZ4ie8ph3FOy_5G6QM_MXLOK_U"
import pandas as pd

bot = telebot.TeleBot(token)

# Emoji
one = emojize(":one:", use_aliases=True)
two = emojize(":two:", use_aliases=True)
three = emojize(":three:", use_aliases=True)
zero = emojize(":zero:", use_aliases=True)
hun = emojize(":100:", use_aliases=True)
r = emojize(":small_orange_diamond:", use_aliases=True)
b = emojize(":small_blue_diamond:", use_aliases=True)
dol = emojize(":dollar:", use_aliases=True)
eur = emojize(":euro:", use_aliases=True)
voskl = emojize(":bangbang:", use_aliases=True)
dom = emojize(":office:", use_aliases=True)
brr = emojize(":bank:", use_aliases=True)
pal = emojize(":round_pushpin:", use_aliases=True)

# Типы маркапов
user_markup = telebot.types.ReplyKeyboardMarkup(True)
user_markup.row('Лучший курс', 'Курсы банков', 'История курса')
user_markup.row('Конвертор валюты', 'Адреса банков')
user_markup.row('USD', 'Euro', 'RUS')
user_markup.row('Информация')
hist = telebot.types.ReplyKeyboardMarkup(True)
hist.row('7дней', '14дней', '30 дней')
konv = telebot.types.ReplyKeyboardMarkup(True)
konv.row('USD->BYN', 'EURO->BYN', 'RUS->BYN')
konv.row('BYN->USD', 'BYN->EURO', 'BYN->RUS')
konv.row('Меню')
d = telebot.types.ReplyKeyboardMarkup(True)
d.row('Продать доллар', 'Купить доллар', 'Меню')
d.row('USD', 'Euro', 'RUS')
e = telebot.types.ReplyKeyboardMarkup(True)
e.row('Продать евро', 'Купить евро', 'Меню')
e.row('USD', 'Euro', 'RUS')
russ = telebot.types.ReplyKeyboardMarkup(True)
russ.row('Продать рос рубли', 'Купить рос рубли', 'Меню')
russ.row('USD', 'Euro', 'RUS')
b_m = telebot.types.ReplyKeyboardMarkup(True)
b_m.row(pal + 'Меню', 'МТБанк', 'Альфа-Банк')
b_m.row('Белгазпромбанк', 'РРБ-Банк')
b_m.row('Паритетбанк', 'Цептер Банк')
b_m.row('Белинвестбанк', 'БНБ-Банк')
b_m.row('БПС-Сбербанк', 'ВТБ(Беларусь)')
b_m.row('Белагропромбанк', 'Беларусбанк')
b_m.row('Дабрабыт', 'Решение', 'БелВЭБ')
b_m.row('БСБ Банк', 'БТА Банк')
b_m.row('Приорбанк', 'Франсабанк')
b_m.row('Идея Банк', 'Абсолютбанк')
b_m.row('СтатусБанк', 'Технобанк', 'ТК Банк')


def histfunc(kol_dn):
    i = 0
    buy = []
    sell = []
    date = []
    if i == 0:
        ur = 'https://myfin.by/currency/minsk'
        headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
        pag = requests.get(ur, timeout=30, headers=headers)
        t = str(pag.text)
        t = t[t.find("dataProvider"):t.find("window.chart_1.shortMonthNames = [")]
        t = t[t.find("[") + 1:t.find("]")]

        while len(t) > 0:
            d = t[t.find(':"') + 2:t.find('",')]
            t = t[t.find('",') + 2:]
            b = t[t.find(':"') + 2:t.find('",')]
            t = t[t.find('",') + 2:]
            s = t[t.find(':"') + 2:t.find('"}')]
            t = t[t.find('"}') + 2:]
            buy.append(b)
            sell.append(s)
            date.append(d)
    df = pd.DataFrame(columns={'DATA', 'MY', 'BUY', 'SELL'})
    df["DATA"] = date
    df["DATA"].astype(str).str.replace(".", ",")
    df["MY"] = df["DATA"].str[3:]
    df["BUY"] = buy
    df["SELL"] = sell
    df.to_csv('inform.csv', sep=',')
    if kol_dn == 7:
        return df["DATA"][-7:-1], df["BUY"][-7:-1], df["SELL"][-7:-1]
    if kol_dn == 14:
        return df["DATA"][-14:-1], df["BUY"][-14:-1], df["SELL"][-14:-1]
    if kol_dn == 30:
        return df["DATA"][-30:-1], df["BUY"][-30:-1], df["SELL"][-30:-1]



def getrating():
    url = 'https://myfin.by/currency/minsk'
    headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
    table = []
    while table == []:
        page = requests.get(url, timeout=30, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml')
        table = soup.find_all('div', {'class': 'best-rates big-rates-table'})
    l = 0
    kursprod = []
    kurspokup = []
    g1 = table[0].select('tr')
    for tr in g1:
        tds = tr.select('td')
        for t in tds:
            if t!=[] :
                a = t.text.strip()
                l += 1
                if a.find('+') == -1 or not a == '':
                    if l == 2:
                        kurspokup.append(a)
                    elif l == 3:
                        kursprod.append(a)
                if l == 5:
                    l = 0
    return kurspokup, kursprod


def adress(mode, named, kyr):
    pokup, prodag = getrating()
    url = 'https://myfin.by/currency/minsk'
    headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
    tables = []
    while tables == []:
        page = requests.get(url, timeout=30, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml')
        tables = soup.find_all('table', {'class': 'rates-table-sort'})
    bankk = tables[0].find_all('tr', {'class': 'acc-body'})
    bankkyrsee = tables[0].find_all('tr', {'class': 'tr-tb'})
    ratt = []
    for trr in bankkyrsee:
        rz = []
        tdsss = trr.select('td')
        for ts in tdsss:
            aa = ts.text.strip()
            rz.append(aa)
        ratt.append(rz)
    rat = []
    for tr in bankk:
        if tr != []:
            r = []
            tds = tr.table.select('tr')
            for td in tds:
                rr = []
                st = td.select('td')
                for t in st:
                    a = t.text.strip()
                    rr.append(a)
                r.append(rr)
            rat.append(r)
    bank = []
    for i in range(len(ratt)):
        bank.append(ratt[i][0])
    fil = []
    for br in rat:
        fil.append(br)
    if mode == 1:
        text = dom + "Адреса банков с лучшими курсами:\n"
        l = ""
        for a, b in zip(bank, fil):
            if a == named:
                l = l + brr + "Банк:  " + a + "\n"
                for i in b:
                    if kyr in i:
                        if i[1] in pokup:
                            l = l + voskl + "Лучший курс покупки доллара\n"
                        if i[2] in prodag:
                            l = l + voskl + "Лучший курс продажи доллара\n"
                        if i[3] in pokup:
                            l = l + voskl + "Лучший курс покупки евро\n"
                        if i[4] in prodag:
                            l = l + voskl + "Лучший курс продажи евро\n"
                        if i[5] in pokup:
                            l = l + voskl + "Лучший курс покупка рос рубля\n"
                        if i[6] in prodag:
                            l = l + voskl + "Лучший курс продажи рос рубля\n"
                        adr = pal + "Адрес " + i[0] + "\n"
                        do = "Доллар\n" + "Покупка/Продажа: " + i[1] + '    ' + i[2]
                        eu = "\nЕвро\n" + "Покупка/Продажа: " + i[3] + '    ' + i[4]
                        ru = "\nРос рубль\n" + "Покупка/Продажа: " + i[5] + '    ' + i[6] + '\n\n'
                        l = l + adr + do + eu + ru
        text = text + l
        return text
    if mode == 2:
        return bank, fil


def getall(l):
    url = 'https://myfin.by/currency/minsk'
    tables = []
    while tables == []:
        headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
        page = requests.get(url, timeout=30, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml')
        tables = soup.find_all('table', {'class': 'rates-table-sort'})
    bankkyrse = tables[0].find_all('tr', {'class': 'tr-tb'})
    pokup, prodag = getrating()
    rat = []
    for tr in bankkyrse:
        r = []
        tds = tr.select('td')
        for t in tds:
            a = t.text.strip()
            r.append(a)
        rat.append(r)
    ll = []
    if l == 'usd1':
        a = "Курсы доллара от всех банков:\n"
        for i in rat:
            ba = b + "Банк: " + i[0] + "\n"
            if i[1] in pokup:
                ba = ba + voskl + "Лучший курс покупки\n"
                ll.append(adress(1, i[0], i[1]))
            zz = "Покупка: " + i[1] + '\n\n'
            a = a + ba + zz
    if l == 'usd2':
        a = "Курсы доллара от всех банков:\n"
        for i in rat:
            ba = b + "Банк: " + i[0] + "\n"
            if i[2] in prodag:
                ba = ba + voskl + "Лучший курс продажи\n"
                ll.append(adress(1, i[0], i[2]))
            zz = "Продажa: " + i[2] + '\n\n'
            a = a + ba + zz

    if l == 'euro1':
        a = "Курсы евро от всех банков:\n"
        for i in rat:
            ba = b + "Банк: " + i[0] + "\n"
            if i[3] in pokup:
                ba = ba + voskl + "Лучший курс покупки\n"
                ll.append(adress(1, i[0], i[3]))
            zz = "Покупка: " + i[3] + '\n\n'
            a = a + ba + zz

    if l == 'euro2':
        a = "Курсы евро от всех банков:\n"
        for i in rat:
            ba = b + "Банк: " + i[0] + "\n"
            if i[4] in prodag:
                ba = ba + voskl + "Лучший курс продажи\n"
                ll.append(adress(1, i[0], i[4]))
            zz = "Продажa: " + i[4] + '\n\n'
            a = a + ba + zz

    if l == 'rus1':
        a = "Курсы рос рубля от всех банков:\n"
        for i in rat:
            ba = b + "Банк: " + i[0] + "\n"
            if i[5] in pokup:
                ba = ba + voskl + "Лучший курс покупки\n"
                ll.append(adress(1, i[0], i[5]))
            zz = "Прокупка: " + i[5] + '\n\n'
            a = a + ba + zz

    if l == 'rus2':
        a = "Курсы рос рубля от всех банков:\n"
        for i in rat:
            ba = b + "Банк: " + i[0] + "\n"
            if i[6] in prodag:
                ba = ba + voskl + "Лучший курс продажи\n"
                ll.append(adress(1, i[0], i[6]))
            zz = "Продажа: " + i[6] + '\n\n'
            a = a + ba + zz

    if l == 'all':
        a = "Курсы валют от всех банков:\n"
        for i in rat:
            ba = b + "Банк: " + i[0] + "\n"
            if i[1] in pokup:
                ba = ba + voskl + "Лучший курс покупки доллара\n"
            if i[2] in prodag:
                ba = ba + voskl + "Лучший курс продажи доллара\n"
            if i[3] in pokup:
                ba = ba + voskl + "Лучший курс покупки евро\n"
            if i[4] in prodag:
                ba = ba + voskl + "Лучший курс продажи евро\n"
            if i[5] in pokup:
                ba = ba + voskl + "Лучший курс покупки рос рубля\n"
            if i[6] in prodag:
                ba = ba + voskl + "Лучший курс продажи рос рубля\n"
            do = "Доллар\n" + "Покупка/Продажа: " + i[1] + '    ' + i[2]
            eu = "\nЕвро\n" + "Покупка/Продажа: " + i[3] + '    ' + i[4]
            ru = "\nРос рубль\n" + "Покупка/Продажа: " + i[5] + '    ' + i[6] + '\n\n'
            a = a + ba + do + eu + ru
    return a, ll


@bot.message_handler(commands=['start'])
def handle_text(message):
    bot.send_message(message.chat.id, "Добро пожаловать!\n"
                                      "Использую команду 'Информация' вы можете ознакомиться со всем функционалом бота.\n"
                                      "Только актуальная информация о валюте!", reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    # Конвертор валюты
    if message.text == 'Конвертор валюты':
        qt = "Выберите варианты конвертации:\n" \
             "*Любые команды описанные ниже являются фаст-командами.\n" \
             "Это означает что вы можете воспользоваться ими из лбого раздела\n" \
             "Например посмотреть сколько будет рублей в долларах из раздела 'Лучший курс'."
        bot.send_message(message.chat.id, qt, reply_markup=konv)
    if message.text == 'USD->BYN':
        rr = "Введите данные следющим образом:\n" \
             "Шаблон:ustoby(деньги)\n" \
             "Пример:ustoby20\n"
        bot.send_message(message.chat.id, rr, reply_markup=konv)
    if message.text == 'EURO->BYN':
        rr = "Введите данные следющим образом:\n" \
             "Шаблон:ertoby(деньги)\n" \
             "Пример:ertoby20\n"
        bot.send_message(message.chat.id, rr, reply_markup=konv)
    if message.text == 'RUS->BYN':
        rr = "Введите данные следющим образом:\n" \
             "Шаблон:rutoby(деньги)\n" \
             "Пример:rutoby20\n"
        bot.send_message(message.chat.id, rr, reply_markup=konv)
    if message.text == 'BYN->RUS':
        rr = "Введите данные следющим образом:\n" \
             "Шаблон:bytoru(деньги)\n" \
             "Пример:bytoru20\n"
        bot.send_message(message.chat.id, rr, reply_markup=konv)
    if message.text == 'BYN->EURO':
        rr = "Введите данные следющим образом:\n" \
             "Шаблон:bytoer(деньги)\n" \
             "Пример:bytoer20\n"
        bot.send_message(message.chat.id, rr, reply_markup=konv)
    if message.text == 'BYN->USD':
        rr = "Введите данные следющим образом:\n" \
             "Шаблон:bytous(деньги)\n" \
             "Пример:bytous20\n"
        bot.send_message(message.chat.id, rr, reply_markup=konv)
    if message.text[:6] == 'bytous':
        pokup, prodag = getrating()
        form = float(message.text[6:])
        kon = round(form / float(prodag[0]), 2)
        te = str(form) + " рублей в долларах = " + str(kon)
        bot.send_message(message.chat.id, te, reply_markup=konv)
    if message.text[:6] == 'bytoer':
        pokup, prodag = getrating()
        form = float(message.text[6:])
        kon = round(form / float(prodag[1]), 2)
        te = str(form) + " рублей в евро = " + str(kon)
        bot.send_message(message.chat.id, te, reply_markup=konv)
    if message.text[:6] == 'bytoru':
        pokup, prodag = getrating()
        form = float(message.text[6:])
        kon = round(form / float(prodag[2]) * 100, 2)
        te = str(form) + " рублей в рос рублях = " + str(kon)
        bot.send_message(message.chat.id, te, reply_markup=konv)
    if message.text[:6] == 'ustoby':
        pokup, prodag = getrating()
        form = float(message.text[6:])
        kon = round(form * float(pokup[0]), 2)
        te = str(form) + " долларов в рублях = " + str(kon)
        bot.send_message(message.chat.id, te, reply_markup=konv)
    if message.text[:6] == 'ertoby':
        pokup, prodag = getrating()
        form = float(message.text[6:])
        kon = round(form * float(pokup[1]), 2)
        te = str(form) + " евро в рублях = " + str(kon)
        bot.send_message(message.chat.id, te, reply_markup=konv)
    if message.text[:6] == 'rutoby':
        pokup, prodag = getrating()
        form = float(message.text[6:])
        kon = round(form / 100 * float(pokup[2]), 2)

    # Лучший курс
    if message.text == 'Лучший курс':
        pok, prod = getrating()
        t1 = "Лучшие курс на данный момент:\n"
        t2 = dol + "Доллар США:\n" + r + "Покупка: %r\n" % pok[0] + b + "Продажа: %r\n" % prod[0]
        t3 = eur + "Евро:\n" + r + "Покупка: %r\n" % pok[1] + b + "Продажа: %r\n" % prod[1]
        t4 = hun + " Российских рублей:\n" + r + "Покупка: %r\n" % pok[2] + b + "Продажа: %r\n" % prod[2]
        t5 = one + zero + " Злотых:\n" + r + "Покупка: %r\n" % pok[3] + b + "Продажа: %r\n" % prod[3]
        t6 = hun + " Гривен:\n" + r + "Покупка: %r\n" % pok[4] + b + "Продажа: %r\n" % prod[4]
        text = t1 + t2 + t3 + t4 + t5 + t6
        bot.send_message(message.chat.id, text, reply_markup=user_markup)
    # Курсы банков
    if message.text == 'Курсы банков':
        t = getall('all')
        bot.send_message(message.chat.id, t, reply_markup=user_markup)
    # Menu
    if message.text == 'Меню' or message.text == pal + 'Меню':
        bot.send_message(message.chat.id, 'Выберите необходимое действие в Меню', reply_markup=user_markup)
    # Menu
    if message.text == 'История курса':
        bot.send_message(message.chat.id, 'История курсов за какой промежуток?', reply_markup=hist)
    if message.text == '7дней':
        kdn = 7
        da, bu, se = histfunc(kdn)
        text1 = "Курс за последние %d дней:\n" % kdn
        text = ''
        for d1, b1, s1 in zip(da, bu, se):
            text = d1 + " :    " + b1 + "  " + s1 + "\n" + text
        t2 = "          DATA :   BUY    SELL\n"
        text = text1 + t2 + text
        bot.send_message(message.chat.id, text, reply_markup=user_markup)
    if message.text == '14дней':
        kdn = 14
        da, bu, se = histfunc(kdn)
        text1 = "Курс за последние %d дней:\n" % kdn
        text = ''
        for d1, b1, s1 in zip(da, bu, se):
            text = d1 + " :    " + b1 + "  " + s1 + "\n" + text
        t2 = "          DATA :   BUY    SELL\n"
        text = text1 + t2 + text
        bot.send_message(message.chat.id, text, reply_markup=user_markup)
    if message.text == '30 дней':
        kdn = 30
        da, bu, se = histfunc(kdn)
        text1 = "Курс за последние %d дней:\n" % kdn
        text = ''
        for d1, b1, s1 in zip(da, bu, se):
            text = d1 + " :    " + b1 + "  " + s1 + "\n" + text
        t2 = "          DATA :    BUY    SELL\n"
        text = text1 + t2 + text
        bot.send_message(message.chat.id, text, reply_markup=user_markup)

    # Информация
    if message.text == 'Информация':
        inf = dom + "Адреса банков - показывает адреса всех отделений опредёленного банка\n" \
              + dol + "Лучший курс - показывает лучшие курсы на данный момент\n" \
              + brr + "Курсы банков - показывает все курсы каждого банка\n" \
              + voskl + "Конвертор валют - конвертирует необходимое количство валюты\n" \
              + pal + "Информация - информация о всех функциях бота\n" \
              + one + "USD - иноформация о курсах данной валюты\n" \
              + two + "EURO - иноформация о курсах данной валюты\n" \
              + three + "RUS - иноформация о курсах данной валюты\n"

        bot.send_message(message.chat.id, inf, reply_markup=user_markup)

    name_bank, adresa_otd = adress(2, 'r', 5)
    # Адрес
    if message.text == 'Адреса банков':
        bot.send_message(message.chat.id, 'Выберите банк:', reply_markup=b_m)
    if message.text in name_bank:
        pokup, prodag = getrating()
        l = ""
        l1 = 0
        ppp = 0
        for nb, ao in zip(name_bank, adresa_otd):
            if nb == message.text:
                l = "Банк: " + nb + "\n"
                bot.send_message(message.chat.id, l, reply_markup=user_markup)
                for i in ao:
                    if len(i) > 0:
                        if i[1] in pokup:
                            l = l + voskl + "Лучший курс покупки доллара\n"
                        if i[2] in prodag:
                            l = l + voskl + "Лучший курс продажи доллара\n"
                        if i[3] in pokup:
                            l = l + voskl + "Лучший курс покупки евро\n"
                        if i[4] in prodag:
                            l = l + voskl + "Лучший курс продажи евро\n"
                        if i[5] in pokup:
                            l = l + voskl + "Лучший курс покупка рос рубля\n"
                        if i[6] in prodag:
                            l = l + voskl + "Лучший курс продажи рос рубля\n"
                        adr = pal + "Адрес " + i[0] + "\n"
                        do = "Доллар\n" + "Покупка/Продажа: " + i[1] + '    ' + i[2]
                        eu = "\nЕвро\n" + "Покупка/Продажа: " + i[3] + '    ' + i[4]
                        ru = "\nРос рубль\n" + "Покупка/Продажа: " + i[5] + '    ' + i[6] + '\n\n'
                        l = adr + do + eu + ru
                        bot.send_message(message.chat.id, l, reply_markup=user_markup)

    # USD
    z = []
    if message.text == 'USD':
        bot.send_message(message.chat.id, "Вы хотите купить или продать доллар?", reply_markup=d)
    if message.text == 'Продать доллар':
        val = 'usd1'
        t, z = getall(val)
        bot.send_message(message.chat.id, t, reply_markup=d)
        for iter in z:
            bot.send_message(message.chat.id, iter, reply_markup=d)
    if message.text == 'Купить доллар':
        val = 'usd2'
        t, z = getall(val)
        bot.send_message(message.chat.id, t, reply_markup=d)
        for iter in z:
            bot.send_message(message.chat.id, iter, reply_markup=d)
    # EURO
    if message.text == 'Euro':
        bot.send_message(message.chat.id, "Вы хотите купить или продать евро?", reply_markup=e)
    if message.text == 'Продать евро':
        val = 'euro1'
        t, z = getall(val)
        bot.send_message(message.chat.id, t, reply_markup=e)
        for iter in z:
            bot.send_message(message.chat.id, iter, reply_markup=d)
    if message.text == 'Купить евро':
        val = 'euro2'
        t, z = getall(val)
        bot.send_message(message.chat.id, t, reply_markup=e)
        for iter in z:
            bot.send_message(message.chat.id, iter, reply_markup=d)
    # RUS
    if message.text == 'RUS':
        bot.send_message(message.chat.id, "Вы хотите купить или продать рус рубли?", reply_markup=russ)
    if message.text == 'Продать рос рубли':
        val = 'rus1'
        t, z = getall(val)
        bot.send_message(message.chat.id, t, reply_markup=russ)
        for iter in z:
            bot.send_message(message.chat.id, iter, reply_markup=d)
    if message.text == 'Купить рос рубли':
        val = 'rus2'
        t, z = getall(val)
        bot.send_message(message.chat.id, t, reply_markup=russ)
        for iter in z:
            bot.send_message(message.chat.id, iter, reply_markup=d)


bot.polling(none_stop=True, interval=1)
