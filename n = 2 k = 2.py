import math 

print("This program prints all intager solutions for the")
print("equation a²+b²=c² upto a certain value of c.")
print()
o = input("How large do you want c to be: ")
print()
s = input("Where do you want c to start from\n(no response sets it to 0):")
o = int(o) + 1

if s == "":
    s = 0
else:
    s = int(s)
print("\n")
print("*"*30)
print("\n\n")

for k in range(s, o):
    for i in range(1, k):
        j = math.sqrt((k*k)-(i*i))
        if (j.is_integer()):
            j = int(j)
            if(j>i):
                print("{0}² + {1}² = {2}²".format(i, j, k))       

print("\n\nDone!\n\n")
input("Press enter to exit.")
