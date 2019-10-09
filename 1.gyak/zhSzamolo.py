#zhSzamolo.py
# coding=utf-8
import math
f = open("input.txt", "r")
sor = f.readline()
maxTest = float(sor.split(',')[0])
szerzettTeszt = float(sor.split(',')[1])
sor = f.readline()
maxHf = float(sor.split(',')[0])
szerzettHf = float(sor.split(',')[1])
sor = f.readline()
maxZH = float(sor.split(',')[0])


zhSzazalek = 0.4

elegtelen = 0.49
elegseges = 0.5
kozepes = 0.6
jo = 0.75
jeles = 0.85

eddigi = (szerzettTeszt/maxTest) * 0.25 + (szerzettHf/maxHf) * 0.35
print 'Eddigi: ', eddigi

if (elegseges - eddigi) * maxZH / 0.4  > maxZH:
	print '2: Remenytelen'
else: 
	print(math.ceil((elegseges - eddigi) * maxZH / 0.4))
if (kozepes - eddigi) * maxZH / 0.4  > maxZH:
	print '3: Remenytelen'
else:
	print(math.ceil((kozepes - eddigi) * maxZH / 0.4))
if (jo - eddigi) * maxZH / 0.4  > maxZH:
	print '4: Remenytelen'
else:
	print(math.ceil((jo - eddigi) * maxZH / 0.4))
if (jeles - eddigi) * maxZH / 0.4  > maxZH:
	print '5: Remenytelen'
else:
	print(math.ceil((jeles - eddigi) * maxZH / 0.4))


