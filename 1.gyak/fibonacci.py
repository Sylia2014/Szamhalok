#fibonacci.py
#coding=utf-8
import sys

def fibonacci_recursive(n):
    if n <= 1:
        return n
    else:  
        return(fibonacci_recursive(n-1) + fibonacci_recursive(n-2)) 

hanyadik = int(input("Add meg hanyadik szamra vagy kivancsi: "))

print(fibonacci_recursive(hanyadik))



