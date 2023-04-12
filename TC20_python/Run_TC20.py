import TC20_lib as TC20

#-----------
# 정수 <---> 리스트
# 0x00123456 <---> [0x00, 0x12, 0x34, 0x56]

def int2list(n):
    out_list = []
    out_list.append( (n >> 24) & 0xff ) # 0x00 & 0xff
    out_list.append( (n >> 16) & 0xff ) # 0x12 & 0xff
    out_list.append( (n >> 8 ) & 0xff ) # 0x34 & 0xff
    out_list.append( (n      ) & 0xff ) # 0x56 & 0xff
    return out_list

def list2int(l):
    n = 0
    length = len(l)
    for idx in range(length):
        n += l[idx] << 8*(length-idx-1) # 24, 16, 8, 0 
    return n

#-----------
# Brute force attack
# Given PT, CT ----> Find key s.t. CT = Enc(PT, key)
#-----------
PT = [0, 1, 2, 3]
CT = [242, 112, 116, 14]

print('Key seaching', end='')
key_space = 1<<24 # 2^24

for idx in range(key_space): # 0,1,2...,2^24-1
    key_guess = int2list(idx) # 키 예측
    decrypted = TC20.TC20_Dec(CT, key_guess)
    if PT == decrypted:
        print("Key found ", key_guess)
    if (idx%(1<<16) == 0): # 진도를 보여주는 '......'
        print('.', end='')

'''
# main()
def main():
    message = 'ARIA'
    key = [0, 1, 2, 3]

    PT = [ ord(ch) for ch in message ]
    CT = TC20.TC20_Enc(PT, key)

    print('Message =', message)
    print('PT =', PT)
    print('CT =', CT)

    DT = TC20.TC20_Dec(CT, key)

    print('DT =', DT)
    
#----- Run main()
if __name__ == '__main__':
    main()
'''