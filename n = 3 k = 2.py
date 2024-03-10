import math

print("This program prints all intager solutions for the")
print("equation a²+b²+c²=d² upto a certain value of d.")
print()
o = input("How large do you want d to be: ")
print()
s = input("Where do you want d to start from\n(no response sets it to 0):")
o = int(o) + 1

if s == "":
    s = 0
else:
    s = int(s)

print("\n")
print("*" * 30)
print("\n\n")

for k in range(s, o):
    for i in range(1, k):
        for l in range(1, i):
            n = k  * k
            m = (i  * i) + (l * l)
            if n > m:
                j = math.sqrt(n - m)
                if j.is_integer() and i != j and j != l:
                    j = int(j)
                    if(i<j):
                        print("{0}² + {1}² + {2}² = {3}²".format(l, i, j, k))
                    break

print("Done!\n\n")
input("Press enter to exit.")
