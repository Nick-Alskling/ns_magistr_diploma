import pandas as pd
import requests
url="https://knute.edu.ua/file/MjY=/59853384d9a18595639a903a4be3a7d2.xls"
s=requests.get(url).content
excel_file= pd.ExcelFile(s)

for sheet_name in excel_file.sheet_names:
    df = excel_file.parse(sheet_name)
    if sheet_name == "Розклад":
        sheet_names = excel_file.sheet_names# Get all the sheetnames as a list
        sheet_names = [name.lower() for name in sheet_names]# Format the list of sheet names
        index = sheet_names.index(sheet_name.lower())# Get the index that matches our sheet to find
        df = pd.read_excel(excel_file, sheet_name=index)# Feed this index into pandas
        df = df.replace('\n','', regex=True)
        c = df.loc[(df == 'Деньтижня').any(1).idxmax():].iloc[: , 1:].reset_index(drop=True).T.drop_duplicates().T
        new_header = c.iloc[0] #grab the first row for the header
        c = c[1:] #take the data less the header row
        c.columns = new_header #set the header row as the df header
        print(c)
        header_list = list(c.columns)
        header_list1 = header_list

        header_list_final = [s for s in header_list1 if s.endswith('група')]
        print(header_list_final)

        group_number = "4м група"
        x = c[[header_list[0], header_list[1], group_number]].dropna(how='all').reset_index(drop=True)
        print(x)
    elif sheet_name == "Лист1":
        sheet_names = excel_file.sheet_names# Get all the sheetnames as a list
        sheet_names = [name.lower() for name in sheet_names]# Format the list of sheet names
        index = sheet_names.index(sheet_name.lower())# Get the index that matches our sheet to find
        df = pd.read_excel(excel_file, sheet_name=index)# Feed this index into pandas
        df = df.replace('\n','', regex=True)
        c = df.loc[(df == 'Деньтижня').any(1).idxmax():].iloc[: , 1:].reset_index(drop=True).T.drop_duplicates().T
        new_header = c.iloc[0] #grab the first row for the header
        c = c[1:] #take the data less the header row
        c.columns = new_header #set the header row as the df header
        print(c)
        header_list = list(c.columns)
        header_list1 = header_list

        header_list_final = [s for s in header_list1 if s.endswith('група')]
        print(header_list_final)

        group_number = "4 група"
        x = c[[header_list[0], header_list[1], group_number]].dropna(how='all').reset_index(drop=True)
        print(x)
