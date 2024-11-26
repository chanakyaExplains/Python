def getDigitProduct(n,count):
    n= str(n)
    if  '0' in n:
        return 0 , count + 1    
    else:
        if '5' in n and ('2' in n or '4' in n or '6' in n or '8' in n):
            return 0 , count + 2
        else:
            product = 1
            for char in n:
                product = product * int(char)
            count = count + 1

            return product , count
        

record = 0
for i in range(1,1000000000000000):
    count = 0
    k = i
    while not (k<10):
        k,count = getDigitProduct(k,count)
    
    if count > record:
        print(f"{i} , {count} steps")
        record = count