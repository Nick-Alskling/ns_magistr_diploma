import telebot
from telebot import types
import random
import csv
import get_schedule
import get_news
from get_schedule import schedule_sorted
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
bot = telebot.TeleBot('1796930178:AAFZUChk3App456JxIjSQkvKOzrVjAIApi0')

legend_fak = {
    "fak_FMTP":"ФМТП",
    "fak_FTM":"ФТМ",
    "fak_FEMP":"ФЕМП",
    "fak_FIT":"ФІТ",
    "fak_FRGTB":"ФРГТБ",
    "fak_FFO":"ФФО"
}
legend_course = {
    "course-1":"1",
    "course-2":"2",
    "course-3":"3",
    "course-4":"4",
    "course-1m":"1м",
    "course-2m":"2м"
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Я інформаційний чатбот. Приємно познайомитися, {message.from_user.first_name}')

@bot.message_handler(content_types=["text"])
def any_msg(message):

    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    get_schedule = types.InlineKeyboardButton(text="Графік навчального процесу", callback_data="get-schedule")
    get_news = types.InlineKeyboardButton(text="Новини", callback_data="get-news")
    get_kafedra = types.InlineKeyboardButton(text="Факультети і кафедри", callback_data="get-kafedra")
    get_contacts = types.InlineKeyboardButton(text="Контакти", callback_data="get-contacts")
    keyboardmain.add(get_schedule, get_news, get_kafedra, get_contacts)
    bot.send_message(message.chat.id, f"Натисніть, аби перейти:", reply_markup=keyboardmain)

def enter_fakulty_name(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    fak_FMTP = types.InlineKeyboardButton(text="ФМТП", callback_data="fak_FMTP")
    fak_FTM = types.InlineKeyboardButton(text="ФТМ", callback_data="fak_FTM")
    fak_FEMP = types.InlineKeyboardButton(text="ФЕМП", callback_data="fak_FEMP")
    fak_FIT = types.InlineKeyboardButton(text="ФІТ", callback_data="fak_FIT")
    fak_FRGTB = types.InlineKeyboardButton(text="ФРГТБ", callback_data="fak_FRGTB")
    fak_FFO = types.InlineKeyboardButton(text="ФФО", callback_data="fak_FFO")
    keyboard.add(fak_FMTP, fak_FTM, fak_FEMP, fak_FIT, fak_FRGTB, fak_FFO)
    bot.send_message(message.chat.id, "Виберіть факультет:", reply_markup=keyboard)

def enter_course_number(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    course_1 = types.InlineKeyboardButton(text="1й курс", callback_data="course-1")
    course_2 = types.InlineKeyboardButton(text="2й курс", callback_data="course-2")
    course_3 = types.InlineKeyboardButton(text="3й курс", callback_data="course-3")
    course_4 = types.InlineKeyboardButton(text="4й курс", callback_data="course-4")
    course_1m = types.InlineKeyboardButton(text="1й-м курс", callback_data="course-1m")
    course_2m = types.InlineKeyboardButton(text="2й-м курс", callback_data="course-2m")
    backbutton = types.InlineKeyboardButton(text="Назад", callback_data="get-schedule")
    keyboard.add(course_1, course_2, course_3, course_4, course_1m, course_2m, backbutton)
    bot.send_message(message.chat.id, "Виберіть курс:", reply_markup=keyboard)

def enter_group_number(message):
    bot.send_message(message.chat.id, 'Введіть номер групи')
    bot.register_next_step_handler(message, group_number)

def group_number(message):
    group = message.text
    print(group)
    if not group.isdigit():
        msg = bot.reply_to(message, 'Введіть число, будь ласка.')
        bot.register_next_step_handler(msg, group_number)
        return

def print_news(message):
    with open('news.csv', 'r', newline='', encoding='utf-8') as csvfile:
        for i in range(3):
            print(csvfile.readline().encode('utf-8'))
            bot.send_message(message.chat.id, csvfile.readline().encode('utf-8'))   

@bot.callback_query_handler(func=lambda call:True)

def callback_inline(call):

    store_fak_clicked = None
    store_course_clicked = None
    group = None
    fak_original = None
    course_original = None
    x = 0
    y = 0

    if "fak" in call.data:
        enter_course_number(call.message)
        store_fak_clicked = call.data
        print(store_fak_clicked)
        for key, fak_original in legend_fak.items():
            if key == store_fak_clicked:
                x=fak_original
                #print(fak_original)
                print(x)
    if "course" in call.data:
        enter_group_number(call.message)
        store_course_clicked = call.data
        print(store_course_clicked)
        for key, course_original in legend_course.items():
            if key == store_course_clicked:
                #print(course_original)
                y = course_original
                print(y)
    value = (schedule_sorted[(schedule_sorted['Факультет']==x) & (schedule_sorted['Курс']==y)]['URL']).array
    print(value)
    

    
###################################################################################################################################################################
    
    if call.data == "mainmenu":
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        get_schedule = types.InlineKeyboardButton(text="Графік навчального процесу", callback_data="get-schedule")
        get_news = types.InlineKeyboardButton(text="Новини", callback_data="get-news")
        get_kafedra = types.InlineKeyboardButton(text="Факультети і кафедри", callback_data="get-kafedra")
        get_contacts = types.InlineKeyboardButton(text="Контакти", callback_data="get-contacts")
        keyboardmain.add(get_schedule, get_news, get_kafedra, get_contacts)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Виберіть необхідне:", reply_markup=keyboardmain)
###################################################################################################################################################################
    
    elif call.data == "get-schedule":
        keyboard = types.InlineKeyboardMarkup()
        schedule_regular = types.InlineKeyboardButton(text="звичайний", callback_data="schedule-regular")
        schedule_exam = types.InlineKeyboardButton(text="екзаменаційний", callback_data="schedule-exam")
        backbutton = types.InlineKeyboardButton(text="Назад", callback_data="mainmenu")
        keyboard.add(schedule_regular, schedule_exam, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Виберіть необхідне:", reply_markup=keyboard)
    elif call.data == "schedule-regular":
        enter_fakulty_name(call.message)
        keyboard3 = types.InlineKeyboardMarkup()
        backbutton = types.InlineKeyboardButton(text="Назад", callback_data="get-schedule")
        keyboard3.add(backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ввести дані або повернутися", reply_markup=keyboard3)
    elif call.data == "schedule-exam":
        keyboard3 = types.InlineKeyboardMarkup()
        backbutton = types.InlineKeyboardButton(text="Назад", callback_data="get-schedule")
        keyboard3.add(backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ввести дані або повернутися", reply_markup=keyboard3)
###################################################################################################################################################################
    
    elif call.data == "get-news":
        keyboard = types.InlineKeyboardMarkup()
        print_news(call.message)
        more_news = types.InlineKeyboardButton(text="Читати більше на сайті", callback_data="read_more")
        backbutton = types.InlineKeyboardButton(text="До головного меню", callback_data="mainmenu")
        keyboard.add(more_news,backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Виведено останні 5 новин:", reply_markup=keyboard)
###################################################################################################################################################################
    
    elif call.data == "get-kafedra":
        keyboard = types.InlineKeyboardMarkup()
        fakultets = types.InlineKeyboardButton(text="Факультети", callback_data="fakultets")
        kafedras = types.InlineKeyboardButton(text="Кафедри", callback_data="kafedras")
        backbutton = types.InlineKeyboardButton(text="Назад", callback_data="mainmenu")
        keyboard.add(fakultets, kafedras, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Виберіть необхідне:", reply_markup=keyboard)    
###################################################################################################################################################################
    
    elif call.data == "get-contacts":
        keyboard = types.InlineKeyboardMarkup()
        rele2 = types.InlineKeyboardButton(text="another layer", callback_data="gg")
        backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
        keyboard.add(rele2,backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="replaced text", reply_markup=keyboard)
###################################################################################################################################################################
if __name__ == "__main__":
    bot.polling(none_stop=True)