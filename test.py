a = [('Магазин', 'railway_fork'),
     ('Игры', 'games'),
     ('Информация о боте', 'menu_item'),
     ('Пополнить счет', 'info')]    
print(*[x[1] for x in a], sep=",")