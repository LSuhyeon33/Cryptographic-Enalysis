# (2) MITM - Meet in the Middle attack

import TC20_lib as TC20
import pickle

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
# 피클링 -- 변수를 파일로 저장하기
def save_var_to_file(var, filename):
    f = open(filename, 'w+b')
    pickle.dump(var, f)
    f.close()

def load_var_from_file(filename):
    f = open(filename, 'rb')
    var = pickle.load(f)
    f.close()
    return var

def make_enc_dic(pt):
    dic = {} # 빈 사전
    N = 1<<24 # 2^24까지만
    for idx in range(N):
        key1 = int2list(idx)
        mid1 = TC20.TC20_Enc(pt, key1)
        int_mid1 = list2int(mid1)
        # 사전: { (int_mid1, [int_key1, ...]), ... }
        if int_mid1 in dic:
            dic[int_mid1].append(idx) # idx == list2int(key1)
        else:
            dic[int_mid1] = [ idx ]
        if (idx%(1<<18) == 0):
            print('.', end='')
    print('Make_Enc_Dic: Done!')
    return dic

def verify_key_candidate_list(key1_list, key2, PT2, CT2):
    for int_key1 in key1_list:
        key1_guess = int2list(int_key1)
        mid1 = TC20.TC20_Enc(PT2, key1_guess)
        ct2_guess = TC20.TC20_Enc(mid1, key2_guess)
        if CT2 == ct2_guess:
            print("\nKey1 = ", key1_guess, 'Key2 = ', key2_guess)

'''
Double Encryption (이중 암호화)
PT1 - [Enc, key1] -> mid1 - [Enc, key2] -> CT1
PT2 - [Enc, key1] -> mid2 - [Enc, key2] -> CT2

MITM attack:
    Given (PT1, CT1), (PT2, CT2), find (key1, key2) s.t.
    CT1 = Enc( Enc(PT1, key1), key2),
    CT2 = Enc( Enc(PT2, key1), key2)
'''

PT1 = [0, 1, 2, 3]
CT1 = [30, 18, 28, 114]
PT2 = [4, 5, 6, 7]
CT2 = [215, 173, 154, 71]

#===(단계 1)
# PT1 -[Enc, key1_guess] -> mid1 for key1_guess = 0,1,2, ....
#   (key1_guess, mid1) ===> { (mid1, [key1_guess, ... ]), ... } : 사전저장
# 주어진 평문 PT1에 대하여,
#   모든 key1 후보로 암호화한 결과를 사전으로 만든다.

'''
mid_dic = make_enc_dic(PT1)
save_var_to_file(mid_dic, 'TC20_Dic.p')
'''

#===(단계 2)
# CT1 -[Dec, key2_guess] -> mid1 for key2_guess = 0,1,2, ....
#   (key2_guess, mid1) ===> { (mid1, [key2_guess, ... ]), ... } (key_candidate list)
#   Check: CT2 = Enc( Enc(PT2, key1_guess), key2_guess )

mid_dic = load_var_from_file('TC20_Dic.p')

# PT1 ----> mid1 ----> CT1
# key2 = [0,*,*,*] 24비트로 제한
N = 1<<24
for idx in range(N):
    key2_guess = int2list(idx)
    mid1 = TC20.TC20_Dec(CT1, key2_guess)
    int_mid1 = list2int(mid1)
    if int_mid1 in mid_dic:
        list_key_candidate = mid_dic[int_mid1]
        if len(list_key_candidate) > 0:
            verify_key_candidate_list(list_key_candidate, key2_guess, PT2, CT2)
    if (idx%(1<<18) == 0):
        print('.', end='')

print('Make_Enc_Dic: Done!')
