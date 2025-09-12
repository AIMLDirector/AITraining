# a = 1 # global variable 
# print(a)
# def func1():
#    b = 2  # local variable 
#    print(b)
  
a = 1
b = 1.5
c = 1j

print(type(a)) 
print(type(b))
print(type(c))

d = 'Hello, World!'
print(type(d))
print(d[0:5])

print("working on python code")

a = 1
b =20
print("value of a is",a, "value of b is",b)

print("value of a is {} value of b is {}".format(a, b))

print(f"value of a is {a} value of b is {b}")

print("value of a is %d value of b is %d" % (a, b))

# single dimension array 
list1 = [1,2,3]
list2 = [4,4.5,4.6]
list3  = [1,4.5,3j]
print(list1)
print(list1[0:2])
list1.append(4)
print(list1)
list1.extend(list2)
print(list1)
list1.insert(3,9)
print(list1)
list1.remove(4)
print(list1)
list1.clear()
print(list1)

list4 = ["apple", "banana", "cherry"]
print(list4)
list4.pop()
print(list4)

#tuple for immutable array with single dimension, tuple are used for fixed data
t1 = (1,2,3)
print(t1)
print(t1[0:2])
#create a list with 6 numbers and reverse the list and print it
#create a list with 6 number print alternative numbers
#create a list with 6 number and print the sum of all numbers

#Dictionary for key value pair

D1= {"name": "John", "age": 30, "city": "New York" }
D2 = {"Brand" : "Ford", "Model": "Mustang", "Year": 1964}

#json and Yaml format 
print(D1)
k1 = D1.keys()
print(k1)
v1  = D1.values()
print(v1)

k2 = D2.keys()
print(k2)
print(D1["name"])
print(D2["Model"])

for key, value in D1.items():
    print(key, ":", value)
    





