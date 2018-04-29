# python3
# -*- coding: utf-8 -*-

from termcolor import *
import colorama
colorama.init()

'''
Эта функция создает словарь участников группы, присваивая каждому нулевое значение.
Она вызывается другой функцией, collect_payments, которая, в свою очередь, вызывается
count_payments .
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

'''
Эта функция собирает информацию о персональных тратах каждого участника группы.
Она перехватывает вывод input_names и создает на его основе свой словарь со значениями.
Для записи зачений используется два цикла - внутренний, аугментирующий информацию
о платежах в словарь, и внешний, отвечающий за возможность повторного прохождения
по циклу, если часть платежей не была внесена (удобно, если есть серии чеков, и
они вводятся последовательно.)
'''

def collect_payments():
    ''' Собирает информацию о платежах каждого члена группы '''
    payment_list = input_names()
    while True:
        for name in payment_list:
            print(name, end=' ')
            payment_list[name] += float(input('внес(ла): '))
        check = input('\nЕсли имеются еще неучтенные платежи, введите "да" \n(в случае их отсутствия просто нажмите Enter):\n')
        if check == '':
            break
    return payment_list


'''
Эта функция уже будет производить все расчеты. А может и не все, там видно будет.
На сегодня хватит кодить.
'''

def count_payments():
    debt_list = collect_payments()
    number_summ = 0
    for number in debt_list.values():
        number_summ += number
    cprint("Общая сумма потрат равна " + str(number_summ) + '₽\n', 'red')
    middle_number = number_summ / len(debt_list)
    for debt in debt_list: # Высчитываем потраты каждого члена группы. Положительный баланс - должны ему, отрицательный - должен он.
        debt_list[debt] = debt_list[debt] - middle_number
    name = -1
    ''' У меня возникла трудность - как сделать так, чтобы вместе со значением
    ключа выводился и сам ключ. Вариант создания списка ключей показался вполне
    удовлетворительным - он должен отражать тот порядок, в соответствии с которым
    Питон упорядочивает словари. Но метод .keys() возвращает (!) строку,
    так что на просторах stackoverflow
    (https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python)
    нашел такое решение. Проверил - работает names = [*debt_list]'''
    names = [*debt_list]

    for key in debt_list:
        name += 1
        if debt_list[key] <= 0:
            cprint(names[name] + " должен (должна) " + str(-(round(debt_list[key], 2))) + " ₽", 'yellow')
        else:
            cprint(names[name] + ": ему (ей) должны " + str((round(debt_list[key], 2))) + " ₽", 'green')


count_payments()
