# python3
# -*- coding: utf-8 -*-
from termcolor import *
import colorama
colorama.init()

# Создаем базовые переменные (потом можно и их создавать из ввода)
francev = 0
gorlov = 0
krygin = 0
osipov = 0

# Создаем список для отображения имен в итоговом выводе программы
names = ['Францев Андрей', 'Горлов Андрей', 'Крыгин Юрий', 'Осипов Виктор']

# Создаем цикл, принимающий информацию о тратах и последовательно добавляющий ее в каждой итерации
while True:
    francev += float(input("Сколько внес Францев Андрей (если ничего, то указать 0): "))
    gorlov += float(input("Сколько внес Горлов Андрей (если ничего, то указать 0): "))
    krygin += float(input("Сколько внес Крыгин Юрий (если ничего, то указать 0): "))
    osipov += float(input("Сколько внес Осипов Виктор (если ничего, то указать 0): "))
    iterator = input("\nЕсть ли еще общие расходы? Если имеются еще чеки, наберите 'да'. \n")
    if iterator == 'да':
        continue
    else:
        print('Расспределяем равномерно на всех общие траты... \n')
        break
# Создаем необходимые формулы для рассчета долга
summ = (francev + gorlov + krygin + osipov)
middle_number = (francev + gorlov + krygin + osipov)/4
# Блок вычисления задолженности. Инверсия позволяет нам в цикле показать только должников.
francev = -(francev - middle_number)
gorlov = -(gorlov - middle_number)
krygin = -(krygin - middle_number)
osipov = -(osipov - middle_number)

# Создаем словарь с результатами вычисления задолженности
debt_list ={}
debt_list['francev'] = francev
debt_list['gorlov'] = gorlov
debt_list['krygin'] = krygin
debt_list['osipov'] = osipov
# Показываем общую задолженность
print('Сумма общих трат равна ' + str(summ) + ' ₽\n')
name = -1
for key in debt_list:
    name += 1
    if debt_list[key] > 0:
        cprint(names[name] + " должен " + str(debt_list[key]) + " ₽", 'yellow')
    else:
        cprint(names[name] + ": ему должны " + str(-(debt_list[key])) + " ₽", 'blue')
