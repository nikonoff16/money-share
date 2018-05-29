#! python3
#! /usr/bin/python3
# -*- coding: utf-8 -*-


'''
В этой версии:
- Появилась запись результатов в файл.
- Каждая запись сопровождается временем своего создания.

Очередная  часть планированных изменений сделана. Далее нужно:
- Добавить возможность считывания результатов из предыдущего исчисления (безумная идея, но может выйдет)
- Разбить файл на отдельные модули, для удобства чтения.


'''
import os
import time
from termcolor import *
import colorama
colorama.init()

def exists(path):
    ''' Спасибо ребятам с русского Stackoverfow за этот кусок кода
        https://ru.stackoverflow.com/questions/414593/Как-проверить-существование-файла'''
    try:
        os.stat(path)
    except OSError:
        return False
    return True

'''
Эта функция создает словарь участников группы, присваивая каждому нулевое значение.
Она используется в collect_payments.
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
            print('Для пропуска участника в конкретном распределении введите в его поле "-" (знак минус без кавычек).\n')
            break
    names_list = dict.fromkeys(names_list, 0)
    return names_list
'''
Это центральная функция в скрипте. Ее вызов запускает его, и в нем используются остальные функции. 
Независим от него только вывод информации на экран. 
'''
def collect_payments():
    ''' Собирает информацию о платежах каждого члена группы '''
    payment_list = input_names()
    """ Два словаря создаются для того, чтобы словарь в циклах не перегружать ненужными операциями. 
    После завершения циклов значения внутреннего словаря аугменитурются по ключам к внешнему, final_dictionary. 
    Во время прохождения нового цикла старые значения внутреннего словаря затираются новыми, и конфликтов не возникает"""
    final_list = dict.fromkeys([*payment_list], 0) # Создал отдельный словарь, чтобы не использовать
    #print(final_list)                             # одинаковые ячейки памяти (это было проблемой, пока не решил
                                                   # прочие проблемы этого куска кода.
    summ = 0
    while True:
        "Первый цикл, собирающий информацию и контролирующий ввод."
#         print('''\nВведите информацию о платежах в численном формате. Можно ввести все данные за один подход
# (может так проще будет), или за несколько, в соответствии с событиями, записями или сериями чеков
# что иногда очень удобно, особенно если на некоторых этапах кто-то за что-то отказался платить).
# ЕСЛИ НУЖНО УКАЗАТЬ, ЧТО ЧЕЛОВЕК В ДАННОМ СЛУЧАЕ НЕ УЧАСТВУЕТ В РАЗДЕЛЕ ДЕНЕГ, В ЕГО ГРАФЕ НУЖНО
# ВВЕСТИ СИМВОЛ МИНУСА "-" (БЕЗ ВСЯКИХ КАВЫЧЕК И ПРОБЕЛОВ). Скрипт прогинорирует его в рассчетах
# на этот проход, сохранив его предыдущие данные. ''')
        for name in payment_list:
            print(name, end=' ')
            payment_list[name] = input('внес(ла): ')
            ''' Здесь скрипт контролирует ввод. По знаку "-" в обрабатываемый ключ словаря записывается значение
            None, которое служит триггером для исключения значения в последующих операциях. '''
            if payment_list[name] == '-':
                payment_list[name] = None
            else:
                ''' Не допускаем пользователю ввести неправильные символы (пока не все тесты на дурака провел еще)'''
                try:
                    payment_list[name] = float(payment_list[name])
                except ValueError:
                    while True:
                        payment_list[name] = input('Введите данные в численном формате: ')
                        if payment_list[name].isdigit() == True: # PyCharm подчеркивает здесь .isdigit как неверно
                                                                 # поставленный элемент. Но он не прав здесь.
                                                                 # Все хорошо работает, без ошибок.
                            payment_list[name] = float(payment_list[name])
                            break
        ''' Между циклами применяем функцию рассчета и распределения денег к сформированному нами словарю'''
        payment_list, msumm = (count_payments(payment_list))
        summ +=msumm
        ''' Второй цикл конкатенирует значения словарей, учитывая триггеры None. Поскольку в финальном словаре таких 
        записей нет, на месте пропусков там либо остается ноль, либо прежнее значение.'''
        for member in final_list:
            if payment_list[member] == None:
                continue
            final_list[member] += payment_list[member]
            # print(final_list, payment_list)
        check = input('\nЕсли имеются еще неучтенные платежи, введите "да" \n(в случае их отсутствия просто нажмите Enter):\n')
        if check == '':
            break
    return final_list, summ


""" Цикл рассчетов - пока самая любимая часть кода в скрипте. Он рассчитывает количетсво участников, определяет 
общую сумму и среднее значение траты на включенного участника, и производит расчет для каждого из этих участников,
сохраняя его в исходном списке. """

def count_payments(list):
    number_of_members = len([*list]) # это почти персональное изобретение (в том плане, что сам подобрал этот способ)))
    payments_summ = 0
    for member in list:
        if list[member] == None:
            number_of_members -= 1
    for number in list.values():
        if number == None:
            continue
        payments_summ += number #
    # cprint("Общая сумма потрат на данном этапе равна " + str(number_summ) + '₽\n', 'red')
    middle_number = payments_summ / number_of_members
    for debt in list: # Высчитываем потраты каждого члена группы. Положительный баланс - должны ему, отрицательный - должен он.
        if list[debt] == None:
            continue
        list[debt] = list[debt] - middle_number
    return list, payments_summ


final_dict, summ = collect_payments()

try:
    file = open('count_database.txt', 'a', encoding='utf-8')
except IOError as e:
    print('Файл записи отсутствует, создаю новый... ')
    file = open('count_database.txt', 'a', encoding='utf-8')
    file.write('''
    MIT License Copyright (c) 2018 Victor Osipov
    Welcome on a new session of MONEY-SHARE programm!
    ''')
''' Создаем обрамление записи'''
file.write('\n\n')
file.write(time.ctime(time.time()))
file.write('\n')
file.write('\n')

# Собственно последний блок программы. Результаты выводятся как в файл, так и на экран.
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