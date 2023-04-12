'''
#문자열 거꾸로 출력
message = 'This is a sample text.'
translated = ''
i = len(message)-1
while i >= 0:
    translated = translated + message[i]
    print('translated message = ' + translated)
    i = i-1
print('\nFinal Result = ' + translated)

#.find 함수
msg = "abcdefghijklmnopqrstuvwxyz"
print(msg[msg.find("j"):])

#list
animals = [ 'cat', 'dog', 'lion']
animals.append('woman')

print(animals)
print(''.join(animals))

print(3*[1,2,3]+[9])

#dictionary
myDic1 = { 'us' : 'AES', 'kr' : 'LEA', 'jp' : 'MISTY' }
print(myDic1['kr'])

myDic2 = myDic1
myDic2['ru'] = 'GOST'
print(myDic1)
print(myDic2)

#Slice Operator
list1 = ['a', 'b', ['c', 'd']]
list2 = list1[:]
list2[2] = 'CD'
list3 = list1[:]
list3[2][0] = 'A'
print('list1 = ', list1)
print('list2 = ', list2)
print('list3 = ', list3)
'''
#Split & Join
msg = 'This is a sample text'
list_msg = msg.split()
print('list = ', list_msg)

joined_msg = ''.join(list_msg)
print('joined = ', joined_msg)

for k in range(len(list_msg)-1):
    list_msg[k] += ' '
joined_msg2 = ''.join(list_msg)
print('joined2 = ', joined_msg2)


























