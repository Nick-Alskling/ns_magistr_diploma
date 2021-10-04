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
pd.set_option("display.max_colwidth", 10000)

store_fak_clicked = None
store_course_clicked = None
group = None
fak_original = None
course_original = None

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
    bot.send_message(message.chat.id, 'Виберіть номер групи')
    bot.register_next_step_handler(message, group_number)
    # buttons_list = []
    # for item in list_button_name:
    #     buttons_list.append([InlineKeyboardButton(text=item, callback_data=item)])

    # keyboard_inline_buttons = InlineKeyboardMarkup(inline_keyboard=buttons_list)


def group_number(message):
    group = message.text
    print(group)
    if not group.isdigit():
        msg = bot.reply_to(message, 'Введіть число, будь ласка.')
        bot.register_next_step_handler(msg, group_number)
        return

# def print_news(message):
#     count = 0
#     a = list()
#     with open('news.csv', 'r', newline='', encoding='utf-8') as csvfile:
#         f_csv = csv.reader(csvfile) 
#         next(f_csv,None)
#         for row in enumerate(f_csv):
#             a.append(row)
#             res = [lis[1] for lis in a]
#             count = count + 1
#             if count == 3:
#                 for i in range(len(res)):
#                     bot.send_message(message.chat.id, res[i])
#                 break

def print_news(message):
    with open('news.csv', 'r', newline='', encoding='utf-8') as csvfile:
        for i in range(3):
            print(csvfile.readline().encode('utf-8'))
            bot.send_message(message.chat.id, csvfile.readline().encode('utf-8'))

# def print_schedule(message):
#     M = schedule_sorted.loc[(schedule_sorted['Факультет'] == fak_original) & (schedule_sorted['Курс'].isin([course_original]))]
#     print(M)
#     N = M[M.columns[2]].to_string(index=False)
#     print(N)
#     bot.send_message(message.chat.id, N)
       
@bot.callback_query_handler(func=lambda call:True)
    
def callback_inline(call):
    
    global store_fak_clicked
    global store_course_clicked
    global group
    global fak_original
    global course_original
    global url
    global group_number
    global header_list_final

    if "fak" in call.data:
        enter_course_number(call.message)
        store_fak_clicked = call.data
        #print(store_fak_clicked)
        fak_original = legend_fak.get(store_fak_clicked)
        print(fak_original, not(fak_original))
    if "course" in call.data:
        enter_group_number(call.message)
        store_course_clicked = call.data
        #print(store_course_clicked)
        course_original = legend_course.get(store_course_clicked)
        # print(course_original, not(course_original))
        M = schedule_sorted.loc[(schedule_sorted['Факультет'] == fak_original) & (schedule_sorted['Курс'].isin([course_original]))]
        # print(M)
        url = M[M.columns[2]].to_string(index=False)
        # print(url)
        bot.send_message(call.message.chat.id, url)
        s=requests.get(url).content
        excel_file= pd.ExcelFile(s)
        sheet_to_find = "Розклад"
        sheet_names = excel_file.sheet_names# Get all the sheetnames as a list
        sheet_names = [name.lower() for name in sheet_names]# Format the list of sheet names
        index = sheet_names.index(sheet_to_find.lower())# Get the index that matches our sheet to find
        df = pd.read_excel(excel_file, sheet_name=index)# Feed this index into pandas
        df = df.replace('\n','', regex=True)
        c = df.loc[(df == 'Деньтижня').any(1).idxmax():].iloc[: , 1:].reset_index(drop=True).T.drop_duplicates().T
        new_header = c.iloc[0] #grab the first row for the header
        c = c[1:] #take the data less the header row
        c.columns = new_header #set the header row as the df header
        # print(c)
        header_list = list(c.columns)
        header_list_final = [s for s in header_list if s.endswith('група')]
        print(header_list_final)
        bot.send_message(call.message.chat.id, header_list_final)
        x = c[[header_list[0], header_list[1], group_number]].dropna(how='all').reset_index(drop=True)
        print(x)
    
###################################################################################################################################################################
    
    if call.data == "mainmenu":
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        get_schedule = types.InlineKeyboardButton(text="Розклад навчального процесу", callback_data="get-schedule")
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
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Виведено останні 3 новини:", reply_markup=keyboard)
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