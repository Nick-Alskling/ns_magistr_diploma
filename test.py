import pandas as pd
import requests
import numpy as np
url="https://knute.edu.ua/file/MjY=/59853384d9a18595639a903a4be3a7d2.xls"
schedule_df=requests.get(url).content
excel_file= pd.ExcelFile(schedule_df)
print(excel_file)
for sheet_name in excel_file.sheet_names:
    df = excel_file.parse(sheet_name)
    if sheet_name == "Розклад":
        sheet_names = excel_file.sheet_names# Get all the sheetnames as a list
        sheet_names = [name.lower() for name in sheet_names]# Format the list of sheet names
        index = sheet_names.index(sheet_name.lower())# Get the index that matches our sheet to find
        df = pd.read_excel(excel_file, sheet_name=index)# Feed this index into pandas
        df = df.replace('\n','', regex=True)
        schedule_df_new = df.loc[(df == 'Деньтижня').any(1).idxmax():].iloc[: , 1:].reset_index(drop=True).T.drop_duplicates().T
        new_header = schedule_df_new.iloc[0] #grab the first row for the header
        schedule_df_new = schedule_df_new[1:] #take the data less the header row
        schedule_df_new.columns = new_header #set the header row as the df header
        print(schedule_df_new)
        schedule_df_final = schedule_df_new
        schedule_df_final = schedule_df_final[schedule_df_final.iloc[:, 0].ne(schedule_df_final.columns[0])]
        header_list = list(schedule_df_final.columns)
        header_list_final = [x for x in header_list if x.endswith('група')]
        # print(header_list_final)
        group_number = "4м група"
        schedule_df_group = schedule_df_final[[header_list[-1], header_list[0], header_list[1], group_number]].dropna(how='all').reset_index(drop=True)
        schedule_df_group[schedule_df_group[group_number].str.len().lt(2)]
        print(schedule_df_group)
        schedule_df_group.to_excel("output.xlsx", index = False)
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
        print(schedule_df_new)
        schedule_df_final = schedule_df_new
        schedule_df_final = schedule_df_final[schedule_df_final.iloc[:, 0].ne(schedule_df_final.columns[0])]
        header_list = list(schedule_df_final.columns)
        header_list_final = [x for x in header_list if x.endswith('група')]
        # print(header_list_final)
        group_number = "4 група"
        schedule_df_group = schedule_df_final[[header_list[-1], header_list[0], header_list[1], group_number]].dropna(how='all').reset_index(drop=True)
        schedule_df_group[group_number] = schedule_df_group[group_number] + ' ' + schedule_df_group.shift(-1)[group_number]
        schedule_df_group = schedule_df_group.dropna(thresh=2)


        # if schedule_df_final[header_list[-1].isnull()] and schedule_df_final[header_list[0].isnull()] and schedule_df_final[group_number].isnull():
        #     schedule_df_final = schedule_df_final.dropna()


        print(schedule_df_group)
        schedule_df_group.to_excel("output.xlsx", index = False)