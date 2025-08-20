# x = "Hello, World!"
# if not type(x) is int:
#     raise TypeError("x must be an integer")

try:
    x = 5/0
    print(x)
except:
    print("An error occurred")
else:
    print("No error occurred")
finally:
    print("Execution completed") 
    
try:
    with open("datafile.csv", "r") as f:
        data = f.read()
        print(data)
except FileNotFoundError as e:

    print(f"Error details: {e}")
    #exit(1)


try:
    import ntlka    
except ImportError as e:
    print(f"Module not found: {e}")

a = ["apple", "banana", "cherry"]
try:
    print(a[5])
except IndexError as e:
    print(f"Index error: {e}")
    



  
    
    

    
