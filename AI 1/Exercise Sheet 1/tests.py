# def process_number(x):
#     # YOUR CODE HERE
#     original = x
#     x = ((((x + 3) * 2) - 4) - (original * 2))
#     return x

# process_number(5)


# def repeat_int_length(x, y):
#     funkyStr = ""
#     maxL = len(f'x') 
#     j = 0
#     for i in range (y):
#         funkyStr = funkyStr + "f{x[j]}"
#         j += 1
#         if j == maxL:
#             j = 0
#     return funkyStr
#     raise NotImplementedError()

# repeat_int_length(20, 4)

# def divide(x, y):
#     if x < 0 and y < 0:
#         return divide(0 - x, 0 - y)
#     if x < 0 or y < 0:
#         return 0 - 1 - divide(0 - x, y)
#     else:
#         return divide_helper(x, y, 0)
# # who on earth chooses to do this? 
# def divide_helper(x, y, temp):
#     if y >= x:
#         return x
#     else:
#         return divide_helper(x - y, y, temp + 1)

# print(divide(8, 6))

# def reversed_list(in_list):
#     endlist = []
#     for i in range(len(in_list)):
#             endlist.append(in_list[len(in_list) - 1])
#             in_list.pop(len(in_list) - 1) # tried to refactor to be more compact by making it -i but i thikn that's a bit much and its not worth it spending so much time on suhc a rivial queston
#     return endlist

# print(reversed_list([1,2,3]))
# print(reversed_list([1,2]))
# print(reversed_list([]))
# print(reversed_list([1]))
# print(reversed_list([1,5,5,1,23,167,95,1,6,4,3,6,7,8]))


# E2 Q2 

# def reverse_list(in_list):
#     originalSize = len(in_list)
#     j = 1
#     for i in range(originalSize):
#         in_list.append(in_list[len(in_list) - j])
#         j += 2
#     for i in range(originalSize):
#         in_list.pop(0)
    
# test = [1,2,3]
# reverse_list(test)
# print(test)

# test2 = [1,5,5,1,23,167,95,1,6,4,3,6,7,8]
# reverse_list(test2)
# print(test2)

# test3 = [1]
# reverse_list(test3)
# print(test3)

# test4 = []
# reverse_list(test4)
# print(test4)

# test5 = [1,2]
# reverse_list(test5)
# print(test5)

# E2 Q3

# def merge(list1, list2):
#     tupleList = []
#     altIndex = 0 # because man i miss c#'s intuitive-ness
#     for item in list1:
#         curTuple = (item, list2[altIndex])
#         tupleList.append(curTuple)
#         altIndex += 1
#     return tupleList

# print(merge([1,2,3,4,5], [6,7,8,9,10]))
# print(merge([], []))

# def merge_wrap(list1,list2):
#     smallList = []
#     bigList = []
#     endlist = []
#     bigListSwap = False
#     if len(list1) < len(list2):
#         smallList = list1
#         bigList = list2
#     else:
#         smallList = list2
#         bigList = list1
#         bigListSwap = True
#
#     j = 0 # doing everything the long way lol
#     for item in bigList:
#         if bigListSwap == True:
#             tempTuple = (item, smallList[j])    
#         else:
#             tempTuple = (smallList[j], item)
#         endlist.append(tempTuple)
#         j += 1
#         if j == len(smallList):
#             j = 0
#     return endlist

# print(merge_wrap([1, 2], [3, 4, 5]))

# E2 Q5 which took me far longer than it should've

# def merge_wrap_n(*args):
#     # you are not serious
#     maxAmount = -1
#     totalPairs = []
#     pointerCollection = [] # stores the current pointers of each of the args. the index of the pointer relates to the arg
#     for i in range(len(args)):
#         pointerCollection.append(0) # stores pointers etc
#         if len(args[i]) > maxAmount:
#             maxAmount = len(args[i])
#     for i in range(maxAmount): # this loops for as many possible combinations there are to be made
#         curValues = [] # to then be converted into a tuple
#         mainPointer = 0 # this one goes through the collection of the list
#         for j in range(len(args)):
#             curValues.append(args[mainPointer][pointerCollection[mainPointer]])
#             pointerCollection[mainPointer] += 1
#             if (pointerCollection[mainPointer] == len(args[mainPointer])):
#                 pointerCollection[mainPointer] = 0
#             mainPointer += 1
        
#         totalPairs.append(tuple(curValues))
#     # okay not as hard as i thought, just a lot to comprehend.
#     return totalPairs
            
# print(merge_wrap_n([1,2,3,4], [2], [3,5,6], [9,2,3]))

# E2 Q7

# def frequency_analysis(string):
#     frDict = {}    
#     for ch in string:
#         if ord(ch.lower()) > 96 and ord(ch.lower()) < 123:
#             if ch.lower() in frDict:
#                 frDict[ch.lower()] += 1
#             else:
#                 frDict.update({ch.lower() : 1})
    
#     return frDict

# print(frequency_analysis("Hello World!"))

# E2 Q8
# import re

# def count_words(string):
#     theList = re.split("\W+", string)
#     if (theList[len(theList) - 1]) == "":
#         del theList[len(theList) - 1] # there's always a straggler so i gotta get rid of it
#     wrdDict = {}
#     for wrds in theList:
#         wrds = wrds.casefold()
#         if wrds in wrdDict:
#             wrdDict[wrds] += 1
#         else:
#             wrdDict.update({wrds : 1})
#     return wrdDict

# print(count_words("Hey!"))
# print(count_words("Hello World! You Silly, little Sausages."))
# print(count_words("The Bart, the"))

# E2 Q9

# def sieve(n):
#     mainList = []
#     if n == 2:
#         return 2
#     elif n < 2:
#         return []
#     for i in range (2, n + 1):
#         mainList.append(i)
#     # preliminary checks ^^^
#     multiples = True
#     primes = []
#     j = 0
#     while multiples == True:
#         multiples = False
#         k = mainList[0]
#         primes.append(k)
#         mainList.pop(0)
#         for num in mainList:
#             if (num % k == 0) and (num != k):
#                 mainList.remove(num)
#                 multiples = True

#     return set(primes + mainList)

# print(sieve(0))
# print(sieve(2))
# print(sieve(3))
# print(sieve(10))
# print(sieve(100))

# E2 Q6

# def mean_variance(numbers):
#     def calcul(x):
#         return pow((x - m), 2)
#     m = ( 1 / (numbers[len(numbers) - 1])) * sum(numbers)
#     tList = []
#     for i in numbers:
#         tList.append(calcul(i))
#     s = ( 1 / (numbers[len(numbers) - 1] - 1)) * sum(tList)
#     return (m, s)


# print(mean_variance([1,2,3]))


# E2 Q10

from math import ceil, floor


def rectangle(n, m): # n is the height and m is the width
    curList = []
    for i in range(n):
        if i == 0 or i == (n - 1):
            tempList = []
            for i in range(m):
                tempList.append("#")
            curList.append(tempList)
        else:
            tempList = []
            for i in range(m):
                if i == 0 or i == (m - 1):
                    tempList.append("#")
                else:
                    tempList.append(" ")
            curList.append(tempList)
    return curList

# print(rectangle(2,2))
# print(rectangle(3,3))
# print(rectangle(4,5))
            

# def diamond(n):
#     isOdd = False
#     curList = []
    
#     if n < 3:
#         return "Invalid Input"

#     if n % 2 == 0:
#         isOdd = False
#     else:
#         isOdd = True
    
#     if isOdd:
#         for i in range(n):
#             if i == 0 or i == n - 1:
#                 tempList = []
#                 for i in range(n):
#                     if i == floor(n/2):
#                         tempList.append("#")
#                     else:
#                         tempList.append(" ")
#                 curList.append(tempList)
#             else:
#                 tempList = []
#                 for i in range(n):
#                     tempList.append(" ")
#                 curList.append(tempList)
    # else:
    #     for i in range(n):
    #         if i == 0 or i == n - 1:
    #             tempList = []
    #             for i in range(n):
    #                 if i == 

    return curList

def diamondLineF(n, width):
    tempList = []
    for i in range(width): 
        tempList.append("#")
    alternate = False
    if width != n:
        for i in range(n - width):        
            if alternate == False:
                tempList.append(" ")
                alternate = True
            elif alternate == True:
                tempList.insert(0, " ")
                alternate = False
    return tempList

def diamond(n):
    curList = []
    odd = False
    descending = False

    if n % 2 == 0:
        width = 2
        odd = False
    else:
        width = 1
        odd = True

    for i in range(n):
        curList.append(diamondLineF(n, width))
        if descending == False:
            width += 2
            if width == n:
                descending = True
                if odd == False:
                    curList.append(diamondLineF(n, width)) # you can't direct manipualte i so then i just have to remove this at the end
        elif descending == True:
            width -= 2
            
    if odd == False:
        del curList[len(curList) - 1]

    return curList


# print(diamond(3))
# print(diamond(4))
# print(diamond(5))
# print(diamond(6))
        
def cheqLine(length, width, opposite):
    hashes = False if opposite == True else True
    hCounter = 0
    tempList = []
    for i in range(length):
        if not hashes:
            tempList.append(" ")
            hCounter += 1
        elif hashes:
            tempList.append("#")
            hCounter += 1
        if hCounter == width:
            hCounter = 0
            hashes = not hashes
    
    return tempList

def chequerboard(n, m, c_h, c_w): # height, width, chequerboard height, chequerboard width
    curList = []
    isOpposite = False
    oppCounter = 0
    for i in range (n):    
        curList.append(cheqLine(m, c_w, isOpposite))
        oppCounter += 1
        if oppCounter == c_h:
            oppCounter = 0
            isOpposite = not isOpposite
    return curList

print(chequerboard(6,8,2,2))






# E1 Q10 

# def divide(x, y):
#     if x < 0 and y < 0: # if both numbers are negative recall divide but with positive numbers
#         return divide(0 - x, 0 - y)
#     if x < 0 and y > 0:
#         return 0 - 1 - divide(0 - x, y)
#     if x > 0 and y < 0:
#         return 0 - 1 - divide(x, 0 - y)
#     else:
#         return divide_helper(x, y, 0)

# def divide_helper(x, y, temp):
#     if y >= x:
#         return x
#     else:
#         return divide_helper(x - y, y, temp + 1)

# print(divide(-6, -3))