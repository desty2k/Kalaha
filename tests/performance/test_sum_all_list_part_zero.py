import random
import timeit
number = 10000

t = timeit.timeit('''\
import random
l = [random.randint(0, 1000)] * 1000
alw1 = range(0, 500)
alw2 = range(500, 1000)

if (sum(l[alw1.start:alw1.stop]) == 0 or sum(l[alw2.start:alw2.stop])):
    pass
''', number=number)
print('sum:', t/number * 1000000, 'microsec/one execution')

t = timeit.timeit('''\
import random
l = [random.randint(0, 1000)] * 1000
alw1 = range(0, 500)
alw2 = range(500, 1000)

if (all(l[x] == 0 for x in alw1) or all(l[x] == 0 for x in alw2)):
    pass
''', number=number)
print('all:', t/number * 1000000, 'microsec/one execution')

