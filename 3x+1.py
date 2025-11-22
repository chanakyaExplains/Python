n = int(input("Enter a staring number : "))
x = n
sequence = []

if x < 1:
    print("Seed should be a positive intager")
else:
    while x not in sequence:
        sequence.append(x)
        if x%2 == 0:
            x = int(x/2)
        else:
            x = 3*x +1
    
for number in sequence:
    print(number)
print("Done")

print("The sequence is {} numbers long.".format(len(sequence)))
print("The highest number reached is {}".format(max(sequence)))

input('\n\nPress enter to exit:')
