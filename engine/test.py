def fun(variableName):
    test = 0
    for i in range(0, 4):
        variableName += 2
        test += 1
    return(test)
var1 = 0
var2 = 1
var2 = fun(var1)
print(var1)
print(var2)