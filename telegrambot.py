import telebot
from telebot import types
import random
import csv
import get_regular_schedule
import get_news_announces
import get_kafedra
from get_regular_schedule import schedule_regular_sorted
from get_kafedra import kaf_df, fak_df
from get_contacts import contacts_df
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import dataframe_image as dfi
bot = telebot.TeleBot('1796930178:AAFZUChk3App456JxIjSQkvKOzrVjAIApi0')
pd.set_option("display.max_colwidth", 10000)

store_fak_clicked = None
store_course_clicked = None
fak_course_url_final = None
fak_original = None
course_original = None
group_list = None
store_group_clicked = None
schedule_df_final = None
header_list = None

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

def main_menu(message):
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    get_schedule = types.InlineKeyboardButton(text="Графік навчального процесу", callback_data="get-schedule")
    get_news = types.InlineKeyboardButton(text="Новини i анонси", callback_data="get-news-announces")
    get_kafedra = types.InlineKeyboardButton(text="Факультети і кафедри", callback_data="get-kafedra")
    get_contacts = types.InlineKeyboardButton(text="Контакти", callback_data="get-contacts")
    get_chart = types.InlineKeyboardButton(text="Карта", callback_data="get_map")
    keyboardmain.add(get_schedule, get_news, get_kafedra, get_contacts, get_chart)
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
    bot.send_message(message.chat.id, "Виберіть факультет", reply_markup=keyboard_fak)

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
    
@bot.callback_query_handler(func=lambda call: "schedule-regular" and "fak" and "course" in call.data)
def find_fak_course(call):
    global fak_course_url_final
    fak_course_url = schedule_regular_sorted.loc[(schedule_regular_sorted['Факультет'] == fak_original) & (schedule_regular_sorted['Курс'].isin([course_original]))]
    fak_course_url_final = fak_course_url[fak_course_url.columns[2]].to_string(index=False)
    # print(fak_course_url_final)
    # print(type(fak_course_url_final))
    call.data = fak_course_url_final
    # bot.send_message(call.chat.id, fak_course_url_final)
    get_group_list(call)

# @bot.callback_query_handler(func=lambda call: "schedule-exam" and "fak" and "course" in call.data)
# def find_fak_course(call):
#     global fak_course_url_final
#     fak_course_url = schedule_exam_sorted.loc[(schedule_exam_sorted['Факультет'] == fak_original) & (schedule_exam_sorted['Курс'].isin([course_original]))]
#     fak_course_url_final = fak_course_url[fak_course_url.columns[2]].to_string(index=False)
#     # print(fak_course_url_final)
#     # print(type(fak_course_url_final))
#     call.data = fak_course_url_final
#     # bot.send_message(call.chat.id, fak_course_url_final)
#     get_group_list(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('http'))
def get_group_list(call):
    global group_list
    global schedule_df_final
    global header_list
    schedule_df=requests.get(fak_course_url_final).content
    excel_file= pd.ExcelFile(schedule_df)

    sheet_names = excel_file.sheet_names

    sheet_names = [name.casefold() for name in sheet_names]# Format the list of sheet names

    filtered_schedule_list = list(filter(lambda el: not 'начитка' in el, sheet_names))

    index = sheet_names.index(filtered_schedule_list[0].lower())# Get the index that matches our sheet to find

    if filtered_schedule_list[0] in sheet_names:
        df = pd.read_excel(excel_file, sheet_name = index)# Feed this index into pandas
        df = df.replace('\n','', regex=True)
        df = df.replace('№тижня','Номертижня', regex=True)

        schedule_df_new = df.loc[(df == 'Номертижня').any(1).idxmax():].iloc[: , 0:].reset_index(drop=True).T.drop_duplicates().T
        new_header = schedule_df_new.iloc[0] #grab the first row for the header
        schedule_df_new = schedule_df_new[1:] #take the data less the header row
        schedule_df_new.columns = new_header #set the header row as the df header

        schedule_df_final = schedule_df_new
        schedule_df_final = schedule_df_final[schedule_df_final.iloc[:, 0].ne(schedule_df_final.columns[0])]

        header_list = list(schedule_df_final.columns)
        group_list = [x for x in header_list if x.endswith('група')]

        print_group_schedule(call)




    # for sheet_name in excel_file.sheet_names:
    #     df = excel_file.parse(sheet_name)
    #     if sheet_name == "Розклад":
    #         sheet_names = excel_file.sheet_names# Get all the sheetnames as a list
    #         sheet_names = [name.lower() for name in sheet_names]# Format the list of sheet names
    #         index = sheet_names.index(sheet_name.lower())# Get the index that matches our sheet to find
    #         df = pd.read_excel(excel_file, sheet_name=index)# Feed this index into pandas
    #         df = df.replace('\n','', regex=True)
    #         schedule_df_new = df.loc[(df == 'Деньтижня').any(1).idxmax():].iloc[: , 1:].reset_index(drop=True).T.drop_duplicates().T
    #         print(schedule_df_new)
    #         new_header = schedule_df_new.iloc[0] #grab the first row for the header
    #         schedule_df_new = schedule_df_new[1:] #take the data less the header row
    #         schedule_df_new.columns = new_header #set the header row as the df header
    #         schedule_df_final = schedule_df_new
    #         schedule_df_final = schedule_df_final[schedule_df_final.iloc[:, 0].ne(schedule_df_final.columns[0])]
    #         print(schedule_df_final)
    #         schedule_df_final.to_excel("output1231.xlsx", index = False)
    #         header_list = list(schedule_df_final.columns)
    #         group_list = [x for x in header_list if x.endswith('група')]
    #         # print(group_list)
    #         # print(type(group_list))


        # elif sheet_name == "Лист1":
        #     sheet_names = excel_file.sheet_names# Get all the sheetnames as a list
        #     sheet_names = [name.lower() for name in sheet_names]# Format the list of sheet names
        #     index = sheet_names.index(sheet_name.lower())# Get the index that matches our sheet to find
        #     df = pd.read_excel(excel_file, sheet_name=index)# Feed this index into pandas
        #     df = df.replace('\n','', regex=True)
        #     schedule_df_new = df.loc[(df == 'Деньтижня').any(1).idxmax():].iloc[: , 1:].reset_index(drop=True).T.drop_duplicates().T
        #     new_header = schedule_df_new.iloc[0] #grab the first row for the header
        #     schedule_df_new = schedule_df_new[1:] #take the data less the header row
        #     schedule_df_new.columns = new_header #set the header row as the df header
        #     schedule_df_final = schedule_df_new
        #     schedule_df_final = schedule_df_final[schedule_df_final.iloc[:, 0].ne(schedule_df_final.columns[0])]
        #     schedule_df_final.to_excel("output1231.xlsx", index = False)
        #     header_list = list(schedule_df_final.columns)
        #     group_list = [x for x in header_list if x.endswith('група')]
        #     print_group_schedule(call)

        # elif sheet_name != "Лист1" or "Розклад":

            

        #     sheet_names = excel_file.sheet_names# Get all the sheetnames as a list
        #     sheet_names = [name.lower() for name in sheet_names]# Format the list of sheet names
        #     index = sheet_names.index(sheet_name.lower())# Get the index that matches our sheet to find
        #     df = pd.read_excel(excel_file, sheet_name=index)# Feed this index into pandas
        #     df = df.replace('\n','', regex=True)
        #     schedule_df_new = df.loc[(df == 'Деньтижня').any(1).idxmax():].iloc[: , 1:].reset_index(drop=True).T.drop_duplicates().T
        #     new_header = schedule_df_new.iloc[0] #grab the first row for the header
        #     schedule_df_new = schedule_df_new[1:] #take the data less the header row
        #     schedule_df_new.columns = new_header #set the header row as the df header
        #     schedule_df_final = schedule_df_new
        #     schedule_df_final = schedule_df_final[schedule_df_final.iloc[:, 0].ne(schedule_df_final.columns[0])]
        #     schedule_df_final.to_excel("output1231.xlsx", index = False)
        #     header_list = list(schedule_df_final.columns)
        #     group_list = [x for x in header_list if x.endswith('група')]
        #     print_group_schedule(call)

def print_group_schedule(call):
    keyboard_group = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    for button_content in group_list:
        schedule_btn =  types.KeyboardButton(button_content)
        keyboard_group.add(schedule_btn)
    msg = bot.send_message(call.chat.id, 'Оберіть групу', reply_markup = keyboard_group)
    bot.register_next_step_handler(msg, on_selection)

def on_selection(message):
    group_number = message.text
    # print(group_number)
    schedule_df_group = schedule_df_final[[header_list[0], header_list[1], header_list[2], group_number]].dropna(how='all').reset_index(drop=True)

    # schedule_df_group[group_number] = schedule_df_group[group_number] + ' ' + schedule_df_group.shift(-1)[group_number]
    # schedule_df_group = schedule_df_group.dropna(thresh=2).reset_index(drop=True)

    schedule_df_group[[header_list[0], header_list[1], header_list[2]]] = schedule_df_group[[header_list[0], header_list[1], header_list[2]]].fillna(method = 'ffill')
    schedule_df_group = schedule_df_group.dropna(thresh=1)
    schedule_df_group.dropna(subset = [group_number], inplace=True)
    schedule_df_group1 = schedule_df_group.groupby([header_list[0], header_list[1], header_list[2]], sort = False, dropna = True)[group_number].apply(lambda x: ' / '.join(map(str, x))).reset_index()
    schedule_df_group1.dropna(subset = [group_number], inplace=True)

    schedule_df_group_styled = schedule_df_group1.style.background_gradient()
    dfi.export(schedule_df_group_styled,"mytable.png")
    schedule_img = open("mytable.png", 'rb')
    if message != None:
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_photo(message.chat.id, schedule_img, reply_markup=markup)
    back_main_menu_key = types.InlineKeyboardMarkup(row_width=1)
    backbutton = types.InlineKeyboardButton(text="Назад", callback_data="mainmenu")
    back_main_menu_key.add(backbutton)
    bot.send_message(message.chat.id, "Повернутися до головного меню", reply_markup=back_main_menu_key)

##################################################################################################################################################################
@bot.callback_query_handler(func=lambda call: "faculty" in call.data)   
def fakultets_output(call):
    keyboard_fakultet = types.InlineKeyboardMarkup()
    for x, y in fak_df.items():
        faculty_btn = types.InlineKeyboardButton(text=x, url=y)
        # backbutton = types.InlineKeyboardButton(text="Назад", callback_data="mainmenu")
        keyboard_fakultet.add(faculty_btn)
    bot.send_message(call.message.chat.id, 'Оберіть факультет:', reply_markup = keyboard_fakultet)
    
    keyboard_return = types.InlineKeyboardMarkup()
    backbutton = types.InlineKeyboardButton(text="До головного меню", callback_data="mainmenu")
    keyboard_return.add(backbutton)
    bot.send_message(call.message.chat.id, "Натисніть", reply_markup=keyboard_return)


@bot.callback_query_handler(func=lambda call: "kafedras" in call.data)   
def fakultets_output(call):
    keyboard_kafedra = types.InlineKeyboardMarkup()
    for x, y in kaf_df.items():
        kafedra_btn = types.InlineKeyboardButton(text=x, url=y)
        # backbutton = types.InlineKeyboardButton(text="Назад", callback_data="mainmenu")
        keyboard_kafedra.add(kafedra_btn)
    bot.send_message(call.message.chat.id, 'Оберіть кафедру:', reply_markup = keyboard_kafedra)

    keyboard_return = types.InlineKeyboardMarkup()
    backbutton = types.InlineKeyboardButton(text="До головного меню", callback_data="mainmenu")
    keyboard_return.add(backbutton)
    bot.send_message(call.message.chat.id, "Натисніть", reply_markup=keyboard_return)
##################################################################################################################################################################
@bot.callback_query_handler(func=lambda call: "novyny" in call.data)   
def print_news(call):
    with open('news.csv', 'r', newline='', encoding='utf-8') as csvfile:
        for i in range(3):
            # print(csvfile.readline().encode('utf-8'))
            bot.send_message(call.message.chat.id, csvfile.readline()[1:].encode('utf-8'))
    keyboard_news = types.InlineKeyboardMarkup()
    news = types.InlineKeyboardButton(text="Читати більше", url = "https://knute.edu.ua/b/read-news/?uk")
    backbutton = types.InlineKeyboardButton(text="До меню новин", callback_data="get-news-announces")
    keyboard_news.add(news, backbutton)
    bot.send_message(call.message.chat.id, text="Виберіть дію:", reply_markup=keyboard_news)

@bot.callback_query_handler(func=lambda call: "anonsy" in call.data)   
def print_news(call):
    with open('announces.csv', 'r', newline='', encoding='utf-8') as csvfile:
        for i in range(3):
            # print(csvfile.readline().encode('utf-8'))
            bot.send_message(call.message.chat.id, csvfile.readline()[1:].encode('utf-8'))
    keyboard_announces = types.InlineKeyboardMarkup()
    announces = types.InlineKeyboardButton(text="Читати більше", url = "https://knute.edu.ua/b/read-allnnoun/?uk")
    backbutton = types.InlineKeyboardButton(text="До меню новин", callback_data="get-news-announces")
    keyboard_announces.add(announces, backbutton)
    bot.send_message(call.message.chat.id, text="Виберіть дію:", reply_markup=keyboard_announces)

###################################################################################################################################################################
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):   
    if call.data == "mainmenu":
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        get_schedule = types.InlineKeyboardButton(text="Розклад навчального процесу", callback_data="get-schedule")
        get_news = types.InlineKeyboardButton(text="Новини і анонси", callback_data="get-news-announces")
        get_kafedra = types.InlineKeyboardButton(text="Факультети і кафедри", callback_data="get-kafedra")
        get_contacts = types.InlineKeyboardButton(text="Контакти", callback_data="get-contacts")
        get_chart = types.InlineKeyboardButton(text="Карта", callback_data="get_map")
        keyboardmain.add(get_schedule, get_news, get_kafedra, get_contacts, get_chart)
        bot.send_message(call.message.chat.id, text="Виберіть необхідне:", reply_markup=keyboardmain)

###################################################################################################################################################################
    elif call.data == "get-schedule":
        keyboard = types.InlineKeyboardMarkup()
        schedule_regular = types.InlineKeyboardButton(text="звичайний", callback_data="schedule-regular")
        schedule_exam = types.InlineKeyboardButton(text="екзаменаційний", callback_data="schedule-exam")
        timetable = types.InlineKeyboardButton(text="розклад дзвінків", callback_data="timetable")
        backbutton = types.InlineKeyboardButton(text="Назад", callback_data="mainmenu")
        keyboard.add(schedule_regular, schedule_exam, timetable, backbutton)
        bot.send_message(call.message.chat.id, text="Виберіть необхідне:", reply_markup=keyboard)

    elif call.data == "schedule-regular":
        enter_fakulty_name(call.message)

    elif call.data == "schedule-exam":
        enter_fakulty_name(call.message)
        
    elif call.data == "timetable":
        keyboard_timetable = types.InlineKeyboardMarkup()
        backbutton = types.InlineKeyboardButton(text="Назад", callback_data="get-schedule")
        keyboard_timetable.add(backbutton)
        timetable_img = open('timetable.PNG', 'rb')
        bot.send_photo(call.message.chat.id, timetable_img, reply_markup=  keyboard_timetable )  

###################################################################################################################################################################
    elif call.data == "get-news-announces":
        keyboard_news_announces = types.InlineKeyboardMarkup()
        news = types.InlineKeyboardButton(text="Новини", callback_data = "novyny")
        announces = types.InlineKeyboardButton(text="Анонси", callback_data = "anonsy")
        backbutton = types.InlineKeyboardButton(text="До головного меню", callback_data="mainmenu")
        keyboard_news_announces.add(news, announces, backbutton)
        bot.send_message(call.message.chat.id, text="Виберіть дію:", reply_markup=keyboard_news_announces)

###################################################################################################################################################################
    elif call.data == "get-kafedra":
        keyboard_kafedra = types.InlineKeyboardMarkup()
        fakultets = types.InlineKeyboardButton(text="Факультети", callback_data="faculty")
        kafedras = types.InlineKeyboardButton(text="Кафедри", callback_data="kafedras")
        backbutton = types.InlineKeyboardButton(text="Назад", callback_data="mainmenu")
        keyboard_kafedra.add(fakultets, kafedras, backbutton)
        bot.send_message(call.message.chat.id, text="Виберіть необхідне:", reply_markup=keyboard_kafedra)   

###################################################################################################################################################################
    elif call.data == "get-contacts":
        keyboard_contacts = types.InlineKeyboardMarkup()
        # with open('contacts.csv', 'r', newline='', encoding='utf-8') as csvfile:
        #     for i in range(3):
        #         bot.send_message(call.message.chat.id, csvfile.readlines()[1:].encode('utf-8'))
        backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
        keyboard_contacts.add(backbutton)
        bot.send_message(call.message.chat.id, text="Перелік контактів", reply_markup=keyboard_contacts)
        for index, row in contacts_df.iterrows():
            bot.send_message(call.message.chat.id,row['Відділ'] + " " + row['Телефон'] + " " +  row['email'])


###################################################################################################################################################################
    elif call.data == "get_map":
        keyboard_map = types.InlineKeyboardMarkup()
        backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
        keyboard_map.add(backbutton)
        map_img = open('map.PNG', 'rb')
        bot.send_photo(call.message.chat.id, map_img)
        bot.send_message(call.message.chat.id, text='''А - вул. Кіото 19 (головний корпус)
Б - вул. Кіото 19 (бібліотечний корпус)
В - вул. Кіото 19 (Конгрес-центр)
Г - вул. Мілютенка 8
Д - вул. Кіото 21
Е - вул. Мілютенка 4
Л - вул. Кіото 23
М - вул. Чигоріна 57
Н - вул. Чигоріна 57а
Р - вул. Раєвського 36''', reply_markup=keyboard_map)

##################################################################################################################################################################
if __name__ == "__main__":
    bot.polling(none_stop=True)