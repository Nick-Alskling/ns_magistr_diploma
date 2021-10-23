import pandas as pd
import requests
import numpy as np
# url="https://knute.edu.ua/file/MjY=/4b003622256e34d8dbd76cdb3534e75d.xls"#ФІТ 4 курс
url="https://knute.edu.ua/file/MjM=/5316f0095a17159060043bb00917621e.xls"#ФЕМП 1курс
# url = "https://knute.edu.ua/file/MjQ=/5edecec0f0959414f3e1a57c0bcc3b84.xls" #ФФО 1 курс
schedule_df = requests.get(url).content
excel_file = pd.ExcelFile(schedule_df)
print(excel_file)

sheet_names = excel_file.sheet_names
print(sheet_names)

sheet_names = [name.casefold() for name in sheet_names]# Format the list of sheet names
print(sheet_names)

filtered_schedule_list = list(filter(lambda el: not 'начитка' in el, sheet_names))
print(filtered_schedule_list)

index = sheet_names.index(filtered_schedule_list[0].lower())# Get the index that matches our sheet to find
print(index)

all_df_list = [filtered_schedule_list[0], filtered_schedule_list[1]]
print(all_df_list)


















# if filtered_schedule_list[0] in sheet_names:
#     df = pd.read_excel(excel_file, sheet_name = index)# Feed this index into pandas
#     df = df.replace('\n','', regex=True)
#     df = df.replace('№тижня','Номертижня', regex=True)
#     print(df)
#     df.to_excel("output_1.xlsx", index = False)

#     schedule_df_new = df.loc[(df == 'Номертижня').any(1).idxmax():].iloc[: , 0:].reset_index(drop=True).T.drop_duplicates().T
#     new_header = schedule_df_new.iloc[0] #grab the first row for the header
#     schedule_df_new = schedule_df_new[1:] #take the data less the header row
#     schedule_df_new.columns = new_header #set the header row as the df header
   
#     print(schedule_df_new)
#     schedule_df_final = schedule_df_new
#     schedule_df_final = schedule_df_final[schedule_df_final.iloc[:, 0].ne(schedule_df_final.columns[0])]
    
#     print(schedule_df_final)
#     header_list = list(schedule_df_final.columns)
#     header_list_final = [x for x in header_list if x.endswith('група')]
    
#     print(header_list_final)
#     group_number = "10 група"
#     schedule_df_group = schedule_df_final[[header_list[0], header_list[1], header_list[2], group_number]].dropna(how='all').reset_index(drop=True)
#     # schedule_df_group[group_number] = schedule_df_group[group_number] + ' ' + schedule_df_group.shift(-1)[group_number]
#     # schedule_df_group = schedule_df_group.dropna(thresh=2)
    
#     schedule_df_group[[header_list[0], header_list[1], header_list[2]]] = schedule_df_group[[header_list[0], header_list[1], header_list[2]]].fillna(method = 'ffill')
#     schedule_df_group = schedule_df_group.dropna(thresh=1)
#     schedule_df_group.to_excel("output_2.xlsx", index = False)
    
#     schedule_df_group1 = schedule_df_group.groupby([header_list[0], header_list[1], header_list[2]], sort = False, dropna = True)[group_number].apply(lambda x: ' / '.join(map(str, x))).reset_index()
#     print(schedule_df_group1)
#     schedule_df_group1.to_excel("output_3.xlsx", index = False)






# elif filtered_schedule_list[0] in sheet_names:
#     df = pd.read_excel(excel_file, sheet_name=index)# Feed this index into pandas
#     df = df.replace('\n','', regex=True)
#     df = df.replace('№тижня','Номертижня', regex=True)
#     schedule_df_new = df.loc[(df == 'Номертижня').any(1).idxmax():].iloc[: , 0:].reset_index(drop=True).T.drop_duplicates().T
#     new_header = schedule_df_new.iloc[0] #grab the first row for the header
#     schedule_df_new = schedule_df_new[1:] #take the data less the header row
#     schedule_df_new.columns = new_header #set the header row as the df header
#     print(schedule_df_new)
#     schedule_df_final = schedule_df_new
#     schedule_df_final = schedule_df_final[schedule_df_final.iloc[:, 0].ne(schedule_df_final.columns[0])]
#     header_list = list(schedule_df_final.columns)
#     header_list_final = [x for x in header_list if x.endswith('група')]
#     # print(header_list_final)
#     group_number = "1 група"
#     schedule_df_group = schedule_df_final[[header_list[-1], header_list[0], header_list[1], group_number]].dropna(how='all').reset_index(drop=True)
#     schedule_df_group[group_number] = schedule_df_group[group_number] + ' ' + schedule_df_group.shift(-1)[group_number]
#     schedule_df_group = schedule_df_group.dropna(thresh=2)
#     print(schedule_df_group)
#     schedule_df_group.to_excel("output12321313.xlsx", index = False)

# elif "лист1" or "розклад" in sheet_name:
    # sheet_names = excel_file.sheet_names# Get all the sheetnames as a list
    # sheet_names = [name.lower() for name in sheet_names]# Format the list of sheet names
    # index = sheet_names.index(sheet_name.lower())# Get the index that matches our sheet to find

    # print(sheet_name)

#     df = pd.read_excel(excel_file, sheet_name=index)# Feed this index into pandas
#     df = df.replace('\n','', regex=True)
#     schedule_df_new = df.loc[(df == 'Деньтижня').any(1).idxmax():].iloc[: , 1:].reset_index(drop=True).T.drop_duplicates().T
#     new_header = schedule_df_new.iloc[0] #grab the first row for the header
#     schedule_df_new = schedule_df_new[1:] #take the data less the header row
#     schedule_df_new.columns = new_header #set the header row as the df header
#     print(schedule_df_new)
#     schedule_df_final = schedule_df_new
#     schedule_df_final = schedule_df_final[schedule_df_final.iloc[:, 0].ne(schedule_df_final.columns[0])]
#     header_list = list(schedule_df_final.columns)
#     header_list_final = [x for x in header_list if x.endswith('група')]
#     # print(header_list_final)
#     group_number = "4 група"
#     schedule_df_group = schedule_df_final[[header_list[-1], header_list[0], header_list[1], group_number]].dropna(how='all').reset_index(drop=True)
#     schedule_df_group[group_number] = schedule_df_group[group_number] + ' ' + schedule_df_group.shift(-1)[group_number]
#     schedule_df_group = schedule_df_group.dropna(thresh=2)
#     print(schedule_df_group)
#     schedule_df_group.to_excel("output.xlsx", index = False)