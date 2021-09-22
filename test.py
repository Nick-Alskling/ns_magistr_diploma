import csv
from csv import reader
from get_schedule import schedule_sorted
fak_original = "ФІТ"
course_original = "1м"

# with open('schedule.csv', 'r', newline='', encoding='utf-8') as f:
#     pass the file object to reader() to get the reader object
#     csv_reader = reader(f)
#     Pass reader object to list() to get a list of lists
#     list_of_rows = list(csv_reader)
#     print(list_of_rows)

# for index, list_of_numbers in enumerate(list_of_rows):
#     if 1 == list_of_numbers[0]:
#         print('list[{0:d}][0]'.format(index))

# indecec = [index for (index, list_of_numbers) in enumerate(list_of_rows) if list_of_numbers[0] == 1]
# for index in indecec:
M = schedule_sorted.loc[(schedule_sorted['Факультет'] == fak_original) & (schedule_sorted['Курс'].isin([course_original]))]

print(type(M))
print(M[M.columns[2]].to_string(index=False))
