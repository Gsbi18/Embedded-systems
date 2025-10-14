def fibonacci(n):
    a=0
    b=1
    for	i in range(n):
        print(a)
        temp=a+b
        a=b
        b=temp

fibonacci(10)