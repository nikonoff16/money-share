# python3
# -*- coding: utf-8 -*-

# Создаем базовые переменные (потом можно и их создавать из ввода)
def input_names():
    ''' Создает словарь из введенных пользователем имен'''
    names_list = []
    while True:
        name = input("Введите имя участника: ")
        if name != '':
            names_list.append(name)
        else:
            print('Ввод участников завершен, приступаем к занесению информации о платежах... \n')
            break
    names_list = dict.fromkeys(names_list, 0)
    return names_list


def collect_payments():
    ''' Собирает информацию о платежах каждого члена группы '''
    payment_list = input_names()
    while True:
        for name in payment_list:
            print(name, end=' ')
            payment_list[name] += float(input('внес: '))
        check = input('\nЕсли имеются еще неучтенные платежи, введите "да" \n(в случае их отсутствия просто нажмите Enter): ')
        if check == '':
            break
    return payment_list

print(collect_payments())

# for key in debt_list:
#     name += 1
#     if debt_list[key] > 0:
#         print(names[name] + " должен " + str(debt_list[key]) + " ₽")
