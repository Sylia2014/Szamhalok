#szokoev.py
#coding=utf-8
import sys;

ev = int(raw_input("Add meg az evet: "));

if ev % 4 == 0 and ev % 100 <> 0 or ev % 400 == 0:
	print "Az altalad megadott ev szokoev."
else:
	print "Az altalad megadott ev nem szokoev."