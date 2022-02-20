#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import process_time
from os.path import join, abspath
import sys


# Программа для решения судоку и вывода решения, если оно есть. Если решения нет, вернется None
def solve(sudo):
    sol = [[y for y in x] for x in sudo]
    if solstep(sol):
        return sol


# Функция для пошагового решения судоку
def solstep(sol):
    while True:
        min_pos = None
        for ri in range(9):
            for ci in range(9):
                if sol[ri][ci]: # Если проверяемая ячейка уже заполнена, переходим к следующей
                    continue
                pv = gpv(ri, ci, sol)
                pv_count = len(pv)
                if not pv_count: # Если для ячейки не существует вариантов для заполнения, судоку не имеет решения
                    return False
                if pv_count == 1: # Если для ячейки существует единственный вариант заполнения, вписываем его в ячейку
                    sol[ri][ci] = next(iter(pv))
                if not min_pos or pv_count < len(min_pos[1]): # Если min_pos == None (то есть до достижения текущей ячейки не попадалось незаполненных)
                    # или если количество возможных значений для текущей ячейки меньше, чем минимальное количество
                    # возможных значений из всех уже проверенных ячеек, сохраняем адрес текущей ячейки и возможные значения 
                    min_pos = (ri, ci), pv
        if not min_pos: # Если прошли циклами всё судоку, и осталось min_pos == None, значит незаполненных ячеек больше нет, и судоку решено.
            return True
        elif len(min_pos[1]) >= 2: # Если для незаполненных ячеек судоку не осталось однозначных вариантов заполнения, выходим из цикла while
            break
    (r, c), z = min_pos # На этот момент у нас не осталось однозначных вариантов заполнения ячеек
    # Принимаем в работу ячейку с минимальным количеством вариантов заполнения - берем ее координаты и множество ее возможных значений
    for v in z: # Для каждого из возможных значений создаем копию текущей стадии заполнения судоку, подставляем в нее это возможное значение ячейки и уходим в рекурсию
        sol_copy = [[y for y in x] for x in sol]
        sol_copy[r][c] = v
        if solstep(sol_copy): # Если при установке этого значения ячейки судоку не решается (возвращает False), переходим на следующую итерацию (подставляем следующее значние)
        # Если же судоку решается (возвращает True), копируем полностью решенную копию судоку в самое исходное судоку.
            sol[:] = [[y for y in x] for x in sol_copy]
            return True


# grv - это get_row_value. Для заданного номера строки из матрицы возвращаем множество чисел, которые уже стоят в этой строке.
def grv(ri, sudo):
    return set(sudo[ri])


# gcv - это get_column_value. Для заданного номера столбца из матрицы возвращаем множество чисел, которые уже стоят в этом столбце.
def gcv(ci, sudo):
    return {line[ci] for line in sudo}

# gbv - это get_block_value. Для заданного номера блока из матрицы возвращаем множество чисел, которые уже стоят в этом блоке.
def gbv(ri, ci, sudo):
    brs = 3 * (ri // 3)
    bcs = 3 * (ci // 3)
    return {sudo[brs + x][bcs + y]
            for x in range(3)
            for y in range(3)
            }


# gpv - это get_possible_value. Для заданной ячейки возвращаем множество возможных значений.
def gpv(ri, ci, sudo):
    res = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    res -= grv(ri, sudo)
    res -= gcv(ci, sudo)
    res -= gbv(ri, ci, sudo)
    return res

# Вывод судоку, с границами блоков
def pr_sudok(s, dst=sys.stdout):
    print('+-------+-------+-------+', file=dst)
    for k in range(9):
        print('|', s[k][0], s[k][1], s[k][2], '|',
                   s[k][3], s[k][4], s[k][5], '|',
                   s[k][6], s[k][7], s[k][8], '|', file=dst)
        if k % 3 == 2:
            print('+-------+-------+-------+', file=dst)


# Convsud - это conversion sudoku, функция для перевода строки цифр в список списков
def convsud(strsud):
    result = [list(map(int, strsud[i: i + 9])) for i in range(0, 81, 9)]
    return result

# Указываем относительный и абсолютный путь до файла sudoky100.txt (откуда считываем строки цифр)
tpath = join('..', 'Data', 'sudoky100.txt')
tpath = abspath(tpath)
print(tpath)

# Указываем относительный и абсолютный путь до файла sudoku_solved.txt (куда записываем всю информацию)
spath = join('..', 'Data', 'sudoky_solved.txt')
spath = abspath(spath)
print(spath)

# Открываем на запись файл sudoku_solved.txt и на чтение файл sudoky100.txt
with open(spath, 'wt', encoding='UTF-8') as dst, \
        open(tpath, 'rt', encoding='UTF-8') as src:
    n = 0 # Засекаем время начала решения всех судоку
    tall0 = process_time()
    for line in src:  # Построчно читаем файл sudoky100.txt и удаляем лишние пробелы в начале и конце каждой строки
        line = line.strip()
        if len(line) == 81: # Если строка состоит из 81 символа, преобразуем ее в список списков и записываем в файл
            n += 1
            sudolist = convsud(line)
            pr_sudok(sudolist, dst = dst)
            
            # Засекаем время начала решения каждого судоку, запускаем решение, вычисляем время окончания решения
            t0 = process_time()
            res = solve(sudolist)
            t = process_time() - t0 
            
            if res: # Если судоку имеет решение, записываем в файл решенный вариант и затраченное на решение время
                pr_sudok(res, dst = dst)
                print(f'Судоку {n:3} решена за {t} сек.')
                print(f'Судоку {n:3} решена за {t} сек.\n', file=dst)
            else:  # Иначе записываем в файл только затраченное на решение время.
                print(f'Судоку {n:3} не решена  за {t} сек.')
                print(f'Судоку {n:3} не решена  за {t} сек.\n', file=dst)
    tall = process_time() - tall0 # Вычисляем время окончания решения всех судоку и записываем его в файл
    print(f'\n\nВсе {n} судоку решены за {tall} сек.')
    print(f'\n\nВсе {n} судоку решены за {tall} сек.', file=dst)
