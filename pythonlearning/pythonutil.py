import math

print(math.sqrt(16)) 

import statistics

print(statistics.mean([1, 2, 3, 4, 5]))

print(statistics.mode([1, 2, 2, 3, 4]))

print(sum([1, 2, 3, 4, 5]))

import datetime

print(datetime.datetime.now())

print(datetime.date.today())
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

print(datetime.datetime.now().time())
import random

print(random.random())  # Random float between 0.0 and 1.0
print(random.choice(['apple', 'banana', 'cherry']))  # Random choice from a list

print(random.choice(["How are you?", "Hello!", "how is the day going?"])) 

print(random.choice(["bye", "see you later", "take care"]))

print(random.sample([1, 2, 3, 4, 5], 3))  # Random sample of 3 elements from the list

#random( randint, randrange, shuffle, choice, sample)

import os

print(os.getcwd())  # Get current working directory
print(os.listdir())  # List files in the current directory

print(os.path.exists("pythonutil.py"))  # Check if a file exists
print(os.path.isfile("pythonutil.py"))  # Check if it's a file
print(os.path.isdir("pythonutil.py"))  # Check if it's a directory 

if os.path.isdir("pythonutil.py"):
    print("It's a directory")
else:
    print("It's not a directory")   
    
print(os.path.join(os.getcwd(), "pythonutil.py"))  # Join path components

import sys
print(sys.version)  # Print Python version



   
def fun1():
    print("This is a function to validate this directory or not:  pythonutil.py")
    if os.path.isdir("pythonutil.py"):
        print("It's a directory")
        sys.exit(0)
    else:
        print("It's not a directory")
        sys.exit(1)

fun1()


    
    
