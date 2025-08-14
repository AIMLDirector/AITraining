# if loop is to deal with condition or decision making.
# if the condition is true then the code will execute otherwise it will not execute.
# if condition :
#     print("condition is true")
# else:
#     print("condition is false")
    
# if condition2:
#     print("condition2 is true")

# #  Testing of our system in performance on cpu, memory and speed  or hackers or virus condition 
# if true:
#     print("this will always execute")
    
# if *.doc:
    
     
    
# if condition1:
#     print("condition1 is true")
# elif condition2:
#     print("condition2 is true")
# else:
#     print("both conditions are false")
    
# if condition1:
#     print("condition1 is true")
#     if condition2:
#         print("condition2 is true")
#         if condition3:
#             print("condition3 is true")
#         else:
#             print("condition3 is false")
#     else:
#         print("condition2 is false")
        
a = 10
if a > 5:
    print("a is greater than 5")
    
    
if a < 5:
    print("a is less than 5")
else:
    print("a is not less than 5")
    
if a > 5 and a < 15 :
    print("a is between 5 and 15")
    
if a < 5 or a > 15 :
    print("a is either less than 5 or greater than 15")

if (a < 5) or (a > 15):
    print("a is either less than 5 or greater than 15")

if (a < 6 and a > 4) or (a > 15):
    print("a is either between 4 and 6 or greater than 15")

# if condition are written with for or while loop 

for i in range(10):
    print(i)
    if i % 2 == 0:
        print(f"{i} is even")
    else:
        print(f"{i} is odd")
        
list1 = [1, 2, 3, 4, 5]

for item in list1:
    if item % 2 == 0:
        print(f"{item} is even")
    else:
        print(f"{item} is odd")
    
evenlist = []
oddlist = []  
for item in list1:
    if item % 2 == 0:
        evenlist.append(item)
    else:
        oddlist.append(item)
        
print("Even numbers:", evenlist)
print("Odd numbers:", oddlist)

        
        
        
        

    


    
    