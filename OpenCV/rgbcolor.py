import random as rand
import numpy as np

s = []

with open('colors.txt','r') as fin:

    for i in range(sum(1 for line in open('colors.txt'))):
       s.append(fin.readline())

print(s[2])