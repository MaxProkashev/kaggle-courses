# ------------------------------------------------------------
# |                                                          |
# |                   введение в python                      |
# |                                                          |
# ------------------------------------------------------------
#
#
# СПИСКИ, можно менять, добавлять
primes = [2, 3, 5, 7]
planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
hands = [
    ['J', 'Q', 'K'],
    ['2', '2', '2'],
    ['6', 'A', 'K'],
]

# СРЕЗЫ
planets[0:3]    # ['Mercury', 'Venus', 'Earth']
planets[:3]     # ['Mercury', 'Venus', 'Earth']
planets[3:]     # ['Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
planets[1:-1]   # ['Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus']
planets[-3:]    # ['Saturn', 'Uranus', 'Neptune']

planets[:3] = ['Mur', 'Vee', 'Ur']  # присваивает сразу нескольким

len(planets)    # длина
sorted(planets) # сортировка
sum(primes)     # сумма
max(primes)     # максимум
min(primes)     # минимум


# комплексное число
c = 12 + 3j
c.imag      # attribute

# функция, прикрепленная к объекту, называется МЕТОД.
# нефункциональные вещи, прикрепленные к объекту, например изображения, называются АТРИБУТАМИ.

# методы списков
planets.append('Pluto')     # изменяет список, добавляя элемент в конец
planets.pop()               # возвращает и удаляет последний элемент списка
planets.index('Earth')      # возвращает индекс объекта

"Earth" in planets          # есть ли элемент в списке


# КОРТЕЖИ, нельзя менять
t = (1, 2, 3)

# ЦИКЛЫ
for planet in planets:      # проход по списку planets
    print(planet, end=' ')

# имя переменной для использования (в данном случае, planet)
# набор значений для цикла (в данном случае, planets)

for i in range(5):          # range() - это функция, которая возвращает последовательность чисел
    print(i)

# list comprehensions
# составление списка
squares = [n**2 for n in range(10)]     # циклы внутри задания списка
# или
squares = []
for n in range(10):
    squares.append(n**2)

# условие внутри создания среза по списку (можно сразу что то сделать с выбранными по условию элементами)
short_planets = [planet for planet in planets if len(planet)<6]                         # ['Venus', 'Earth', 'Mars']
loud_short_planets = [planet.upper() + '!' for planet in planets if len(planet) < 6]    # ['VENUS!', 'EARTH!', 'MARS!']

def count_negatives(nums):
    return len([num for num in nums if num < 0])     # или return sum([num < 0 for num in nums])

# СТРОКИ
claim = "Pluto is a planet!"
claim.upper()                   # 'PLUTO IS A PLANET!'
claim.lower()                   # 'pluto is a planet!'
claim.index('plan')             # 11
claim.startswith(planet)        # True
claim.endswith('dwarf planet')  # False

# .split()
words = claim.split()           # ['Pluto', 'is', 'a', 'planet!']

# .join()
datestr = '1956-01-31'
year, month, day = datestr.split('-')
'/'.join([month, day, year])    # '01/31/1956'
' 👏 '.join([word.upper() for word in words])   # 'PLUTO 👏 IS 👏 A 👏 PLANET!'

# .format()
planet + ', we miss you.'
planet + ", you'll always be the " + str(9) + "th planet to me."

"{}, you'll always be the {}th planet to me.".format(planet, 9)
"Pluto's a {0}.\nNo, it's a {1}.\n{0}!\n{1}!".format('planet', 'dwarf planet')

# СЛОВАРИ
numbers = {'one':1, 'two':2, 'three':3}
numbers['eleven'] = 11
numbers['one'] = 'Pluto'
for k in numbers:
    print("{} = {}".format(k, numbers[k]))

# создание словаря циклом
planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
planet_to_initial = {planet: planet[0] for planet in planets}

# округление
from math import pi
"{:.4}".format(pi)

# submodels
import numpy
rolls = numpy.random.randint(low=1, high=6, size=10)        # array([4, 1, 2, 2, 1, 3, 1, 1, 5, 2])
type(rolls)     # numpy.ndarray
rolls.mean()    # среднее
