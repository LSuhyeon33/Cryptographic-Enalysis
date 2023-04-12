#-------------------------
# 암호분석 2022
#
#  BCF 4라운드 Feistel 암호에 대한 선형공격
#
#-------------------------

import BCF_lib as BCF
import my_lib2 as Common
import copy
import random

'''
#===
# BCF test
pt = [1, 2]
key = [ 5,6,7,8 ]
ct = BCF.BCF_Enc(pt, key)
print(ct)
dec_pt = BCF.BCF_Dec(ct, key)
print(dec_pt)
'''

'''
#=======
# 평문-암호문 쌍 만들기

num_ptct_pairs = 1<<12 # 2^12개
ptct_list = []
key = [1,2,3,4]  # 공격자는 모르는 키

for i in range(num_ptct_pairs):
    pt = [random.randint(0,255), random.randint(0,255)]
    ct = BCF.BCF_Enc(pt, key)
    ptct_pair = copy.deepcopy([pt, ct])
    ptct_list.append(ptct_pair)
    
ptct_file = 'BCF_ptct_4096.var'
Common.save_var_to_file(ptct_list, ptct_file)
print('--- Cipher: BCF')
print('The number of pt-ct pairs: ', num_ptct_pairs)
print('File name:', ptct_file)
'''

#=====
# 선형 공격
# pt = [PL, PR], ct = [CL, CR]
# 라운드함수의 선형특성:  a x = b F(x)  <===>  a x = b S[x]
# 1라운드 특성: a (PL ^ k1) = b (PR ^ A)
# 3라운드 출력: [L, R]
# 3라운드 특성: a (R ^ k3) = b (L ^ A)
# 1^3 라운드 특성: a (PL ^ k1 ^ R ^ k3)  = b (PR ^ L)   
#   (중간값 A가 지워짐에 주목하자!!!)
# L = CL, R =  S[CL^k4] ^ CR
# 선형공격에 필요한 식: 
#     a (PL ^ S[CL^k4] ^ CR) ^ b (PR ^ CL) = a (k1 ^ k3)
#     k4를 예측하고, 왼쪽식이 0 또는 1에 크게 치우치는 k4를 올바른 키로 등록한다.
#     우변의 (k1 ^k3)의 값에 따라 0이나 1에 치우친다. (k1, k3는 공격자가 모르는 값)

#-----
# (in_mask-->out_mask)= (a-->b) 확률 = 0.xx
# (64-->64) probability = 0.766
# (64-->68) probability = 0.734
# (128-->4) probability = 1.000
# (192-->64) probability = 0.734
# (192-->68) probability = 0.766

ptct_file = 'BCF_ptct_4096.var'
ptct_list = Common.load_var_from_file(ptct_file)
#in_mask = 128
#out_mask = 4
in_mask = 64
out_mask = 68


score_list = [0]*256 # k4 guessing 00~FF
# 선형식 a (PL ^ S[CL^k4] ^ CR) = b (PR ^ CL) 
print('Run LC', end='')
for key4_guess in range(256): #k4 guessing
    for i in range(len(ptct_list)):
        pt, ct = ptct_list[i][0], ptct_list[i][1]  # ptct_list = [ [pt1, ct1], ...]
        PL, PR, CL, CR = pt[0], pt[1],  ct[0], ct[1]
        lhs = Common.hw_mod2(in_mask & (PL ^ BCF.S[CL^key4_guess] ^CR))
        rhs = Common.hw_mod2(out_mask & (PR ^ CL))        
        if lhs == rhs: # a x = b y
            score_list[key4_guess] += 1
    print('.', end='') 
print('\n')
print(score_list)

#== 정렬을 위한 기준
def MyOrder(x):
    return(x[1])

mid_value = len(ptct_list)/2
key_candid_list = [ [i, abs(score_list[i]-mid_value)] for i in range(256) ]
key_candid_list.sort(reverse=True, key=MyOrder)
print(key_candid_list[:10])

# k4 = 4 
# [[4, 446.0], [44, 276.0], [118, 274.0], [37, 268.0], [6, 267.0], [33, 263.0], [106, 260.0], [73, 258.0], [108, 257.0], [55, 253.0]]








