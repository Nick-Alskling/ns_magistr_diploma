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
fak_course_url_final = None
fak_original = None
course_original = None
group_list = None
store_group_clicked = None
i = None

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

############################################################################################################################################################################

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
    keyboard_fak = types.InlineKeyboardMarkup(row_width=3)
    fak_FMTP = types.InlineKeyboardButton(text="ФМТП", callback_data="fak_FMTP")
    fak_FTM = types.InlineKeyboardButton(text="ФТМ", callback_data="fak_FTM")
    fak_FEMP = types.InlineKeyboardButton(text="ФЕМП", callback_data="fak_FEMP")
    fak_FIT = types.InlineKeyboardButton(text="ФІТ", callback_data="fak_FIT")
    fak_FRGTB = types.InlineKeyboardButton(text="ФРГТБ", callback_data="fak_FRGTB")
    fak_FFO = types.InlineKeyboardButton(text="ФФО", callback_data="fak_FFO")
    backbutton = types.InlineKeyboardButton(text="Назад", callback_data="mainmenu")
    keyboard_fak.add(fak_FMTP, fak_FTM, fak_FEMP, fak_FIT, fak_FRGTB, fak_FFO, backbutton)
    bot.send_message(message.chat.id, "Виберіть факультет:", reply_markup=keyboard_fak)

def enter_course_number(message):
    keyboard_course = types.InlineKeyboardMarkup(row_width=3)
    course_1 = types.InlineKeyboardButton(text="1й курс", callback_data="course-1")
    course_2 = types.InlineKeyboardButton(text="2й курс", callback_data="course-2")
    course_3 = types.InlineKeyboardButton(text="3й курс", callback_data="course-3")
    course_4 = types.InlineKeyboardButton(text="4й курс", callback_data="course-4")
    course_1m = types.InlineKeyboardButton(text="1й-м курс", callback_data="course-1m")
    course_2m = types.InlineKeyboardButton(text="2й-м курс", callback_data="course-2m")
    backbutton = types.InlineKeyboardButton(text="Назад", callback_data="get-schedule")
    keyboard_course.add(course_1, course_2, course_3, course_4, course_1m, course_2m, backbutton)
    bot.send_message(message.chat.id, "Виберіть курс:", reply_markup=keyboard_course)

##################################################################################################################################################################################

def print_news(message):
    with open('news.csv', 'r', newline='', encoding='utf-8') as csvfile:
        for i in range(3):
            print(csvfile.readline().encode('utf-8'))
            bot.send_message(message.chat.id, csvfile.readline().encode('utf-8'))

############################################################################################################################################################################

@bot.callback_query_handler(func=lambda call: "fak" in call.data )
def fak_find(call):
    global store_fak_clicked
    global fak_original
    store_fak_clicked = call.data
    #print(store_fak_clicked)
    fak_original = legend_fak.get(store_fak_clicked)
    enter_course_number(call.message)
    # print(fak_original, not(fak_original))

@bot.callback_query_handler(func=lambda call: "course" in call.data)
def course_find(call):
    global store_course_clicked
    global course_original
    store_course_clicked = call.data
    #print(store_course_clicked)
    course_original = legend_course.get(store_course_clicked)
    find_fak_course(call.message)
    # print(course_original, not(course_original))
    
@bot.callback_query_handler(func=lambda call: "fak" and "course" in call.data)
def find_fak_course(call):
    global fak_course_url_final
    fak_course_url = schedule_sorted.loc[(schedule_sorted['Факультет'] == fak_original) & (schedule_sorted['Курс'].isin([course_original]))]
    fak_course_url_final = fak_course_url[fak_course_url.columns[2]].to_string(index=False)
    # print(fak_course_url_final)
    # print(type(fak_course_url_final))
    call.data = fak_course_url_final
    # bot.send_message(call.chat.id, fak_course_url_final)
    get_group_list(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('http'))
def get_group_list(call):
    global group_list
    schedule_df=requests.get(fak_course_url_final).content
    excel_file= pd.ExcelFile(schedule_df)
    # print(excel_file)
    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)
        if sheet_name == "Розклад":
            sheet_names = excel_file.sheet_names# Get all the sheetnames as a list
            sheet_names = [name.lower() for name in sheet_names]# Format the list of sheet names
            index = sheet_names.index(sheet_name.lower())# Get the index that matches our sheet to find
            df = pd.read_excel(excel_file, sheet_name=index)# Feed this index into pandas
            df = df.replace('\n','', regex=True)
            schedule_df_new = df.loc[(df == 'Деньтижня').any(1).idxmax():].iloc[: , 1:].reset_index(drop=True).T.drop_duplicates().T
            # print(schedule_df_new)
            new_header = schedule_df_new.iloc[0] #grab the first row for the header
            schedule_df_new = schedule_df_new[1:] #take the data less the header row
            schedule_df_new.columns = new_header #set the header row as the df header
            schedule_df_final = schedule_df_new
            schedule_df_final = schedule_df_final[schedule_df_final.iloc[:, 0].ne(schedule_df_final.columns[0])]
            # print(schedule_df_final)
            header_list = list(schedule_df_final.columns)
            group_list = [x for x in header_list if x.endswith('група')]
            print(group_list)
            print(type(group_list))

        elif sheet_name == "Лист1":
            sheet_names = excel_file.sheet_names# Get all the sheetnames as a list
            sheet_names = [name.lower() for name in sheet_names]# Format the list of sheet names
            index = sheet_names.index(sheet_name.lower())# Get the index that matches our sheet to find
            df = pd.read_excel(excel_file, sheet_name=index)# Feed this index into pandas
            df = df.replace('\n','', regex=True)
            schedule_df_new = df.loc[(df == 'Деньтижня').any(1).idxmax():].iloc[: , 1:].reset_index(drop=True).T.drop_duplicates().T
            new_header = schedule_df_new.iloc[0] #grab the first row for the header
            schedule_df_new = schedule_df_new[1:] #take the data less the header row
            schedule_df_new.columns = new_header #set the header row as the df header
            schedule_df_final = schedule_df_new
            schedule_df_final = schedule_df_final[schedule_df_final.iloc[:, 0].ne(schedule_df_final.columns[0])]
            header_list = list(schedule_df_final.columns)
            group_list = [x for x in header_list if x.endswith('група')]
            # print(group_list)
            # print(type(group_list))
            # group_number = "4 група"
            # schedule_df_group = schedule_df_final[[header_list[0], header_list[1], group_number]].dropna(how='all').reset_index(drop=True)
            # schedule_df_group.to_excel("output.xlsx", index = False)

    if group_list != None:
        def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
            menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
            if header_buttons:
                menu.insert(0, header_buttons)
            if footer_buttons:
                menu.append(footer_buttons)
            return menu

        button_list = []
        for each in group_list:
            button_list.append(types.InlineKeyboardButton(each, callback_data = each))
        keyboard_group=types.InlineKeyboardMarkup(build_menu(button_list, n_cols=3)) #n_cols = 1 is for single column and mutliple rows
        bot.send_message(call.chat.id, text='Виберіть групу:', reply_markup=keyboard_group)
        print(call.data == each)

        # global i
        # keyboard = types.InlineKeyboardMarkup()
        # for i in group_list:
        #     button1 = types.InlineKeyboardButton(text=i, callback_data=i[0])
        #     keyboard.add(button1)
        # bot.send_message(call.chat.id, "Выберите автомобиль из списка:", reply_markup=keyboard)
        # print(i)
        # print_group_schedule(call)



# @bot.callback_query_handler(func=lambda call: call.data != None and call.data == each)
# def print_group_schedule(call):
#     print(i)
#     if call.data in group_list:
#         bot.edit_message_text(call.chat.id, text=i)
###################################################################################################################################################################
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):   
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