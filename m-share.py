#! python3

# -*- coding: utf-8 -*-


"""
07/03/2018
In this version:
- All comments were translated in English
- When a new log file created, it now starts with welcome string.
- Some bugs checked
- The code was cleaned from irrelevant comments


Now I satisfied with the script, and I'm not going to maintain it yet.
There is a plenty ways to perform such simple calculations as these.
Obviously, you can take any office spreadsheet app for it. =)

Because I live in Russia and speak Russian, and (the most important) first users of the script were russians
I made all the program output in Russian, except time, date and welcome string.



"""

import time
from termcolor import *
import colorama

colorama.init()

'''
Here we request and collect from input some names. 
It's used in collect_payments function.
'''


def input_names():
    names_list = []
    while True:
        imya = input("Введите имя участника: ")
        if imya != '':
            names_list.append(imya)
        else:
            print('\nВвод участников завершен, приступаем к занесению информации о платежах... \n')
            print(
                'Для пропуска участника в конкретном распределении введите в его поле "-" (знак минус без кавычек).\n')
            break
    names_list = dict.fromkeys(names_list, 0)
    return names_list


'''

As it's shown in function's name, this algorithm collect payments information. 
I love it most.
 
'''


def collect_payments():
    payment_list = input_names()
    """ Two dictionary were created to not overload main function loop. """
    final_list = dict.fromkeys([*payment_list], 0)
    summ = 0
    while True:
        "This loop collects correct input from user"
        for imya in payment_list:
            print(imya, end=' ')
            payment_list[imya] = input("внес(ла): ")
            ''' This is a feature that allows user to exclude someone from counting for a time.
             This may be useful if some of the group would not share in some kind of traits (like alcohol), 
             but still share with community in other payments. '''
            if payment_list[imya] == '-':
                payment_list[imya] = None
            else:
                ''' Here we stop user from input mistake'''
                try:
                    payment_list[imya] = float(payment_list[imya])
                except ValueError:
                    while True:
                        payment_list[imya] = input('Введите данные в численном формате: ')
                        if payment_list[imya].isdigit():  # I don't know why my PyCharm trying to correct me
                            # The code here works fine
                            # But I didn't catch why it's happening :(
                            payment_list[imya] = float(payment_list[imya])
                            break
        ''' Between loops here we use count_payments func to calculate and distribute money.'''
        payment_list, msumm = (count_payments(payment_list))
        summ += msumm
        ''' This loop concatenate data from a session to the final list'''
        for member in final_list:
            if payment_list[member] is None:
                continue
            final_list[member] += payment_list[member]
        check = input("\nЕсли имеются еще неучтенные платежи, введите \"да\" "
                      "\n(в случае их отсутствия просто нажмите Enter):\n")
        if check == '':
            break
    return final_list, summ


""" I love this piece of code. Other code is made to serve this func. """


def count_payments(lst):
    number_of_members = len([*lst])  # That's my personal device! Because I didn't see such things before I write it.
    payments_sum = 0
    for member in lst:
        if lst[member] is None:
            number_of_members -= 1
    for number in lst.values():
        if number is None:
            continue
        payments_sum += number
    middle_number = payments_sum / number_of_members
    for debt in lst:
        if lst[debt] is None:
            continue
        lst[debt] = lst[debt] - middle_number
    return lst, payments_sum


final_dict, summ = collect_payments()

file = open('count_database.txt', 'r+', encoding='utf-8')
if file.read() == '':
    file.write('''
MIT License Copyright (c) 2018 Victor Osipov
Welcome on a new session of MONEY-SHARE App!
            ''')

''' Here we create visual frame for the script session'''
file.write('\n\n')
file.write(time.ctime(time.time()))
file.write('\n')
file.write('\n')

# The last part of the script

name = -1
names = [*final_dict]
print('Общая сумма трат равна: ' + str(summ) + " ₽\n")
for key in final_dict:
    name += 1
    if final_dict[key] < 0:
        cprint(names[name] + ": должен (должна) " + str(-(round(final_dict[key], 2))) + " ₽", 'yellow')
        file.write(names[name] + ": должен (должна) " + str(-(round(final_dict[key], 2))) + " ₽\n")
    elif final_dict[key] == 0:
        print(names[name] + ': ничего не должен(не должна)')
        file.write(names[name] + ': ничего не должен(не должна)\n')
    else:
        cprint(names[name] + ": ему (ей) должны " + str((round(final_dict[key], 2))) + " ₽", 'green')
        file.write(names[name] + ": ему (ей) должны " + str((round(final_dict[key], 2))) + " ₽\n")

file.write('-' * 45)
file.close()
