#! python3
#! /usr/bin/python3
# -*- coding: utf-8 -*-

from termcolor import *
import colorama
colorama.init()

'''
Эта функция создает словарь участников группы, присваивая каждому нулевое значение.

'''

def input_names():
    ''' Создает словарь из введенных пользователем имен'''
    names_list = []
    while True:
        name = input("Введите имя участника: ")
        if name != '':
            names_list.append(name)
        else:
            print('\nВвод участников завершен, приступаем к занесению информации о платежах... \n')
            break
    names_list = dict.fromkeys(names_list, 0)
    return names_list

def collect_payments():
    ''' Собирает информацию о платежах каждого члена группы '''
    payment_list = input_names()
    final_list = dict.fromkeys([*payment_list], 0)
    print(final_list)
    while True:
        for name in payment_list:
            print(name, end=' ')
            payment_list[name] = input('внес(ла): ')
            if payment_list[name] == '-':
                payment_list[name] = None
            else:
                try:
                    payment_list[name] = float(payment_list[name])
                except ValueError:
                    while True:
                        payment_list[name] = input('Введите данные в численном формате: ')
                        if payment_list[name].isdigit() == True:
                            payment_list[name] = float(payment_list[name])
                            break
        payment_list = (count_payments(payment_list))
        for member in final_list:
            if payment_list[member] == None:
                continue
            final_list[member] += payment_list[member]
            # print(final_list, payment_list)
        check = input('\nЕсли имеются еще неучтенные платежи, введите "да" \n(в случае их отсутствия просто нажмите Enter):\n')
        if check == '':
            break
    return final_list




def count_payments(list):
    number_of_members = len([*list])
    payments_summ = 0
    for member in list:
        if list[member] == None:
            number_of_members -= 1
    for number in list.values():
        if number == None:
            continue
        payments_summ += number # По завершению работы над прогой узнать, что за исключение появляется при None
    # cprint("Общая сумма потрат равна " + str(number_summ) + '₽\n', 'red')
    middle_number = payments_summ / number_of_members
    for debt in list: # Высчитываем потраты каждого члена группы. Положительный баланс - должны ему, отрицательный - должен он.
        if list[debt] == None:
            continue
        list[debt] = list[debt] - middle_number
    return list


final_dict = collect_payments()



name = -1
names = [*final_dict]
for key in final_dict:
    name += 1
    if final_dict[key] < 0:
        cprint(names[name] + " должен (должна) " + str(-(round(final_dict[key], 2))) + " ₽", 'yellow')
    elif final_dict[key] == 0:
        print(names[name] + ' ничего не должен(не должна)')
    else:
        cprint(names[name] + ": ему (ей) должны " + str((round(final_dict[key], 2))) + " ₽", 'green')