#-------------------------
# 암호분석 2022
#-------------------------

import CipherWC8_lib as WC8
import my_lib2 as Common
import random
import copy

'''
#==============
# 평문-암호문 쌍 만들기
num_ptct_pairs = 1<<8  #256
cipher_round = 3 # 라운드 수
ptct_list = []
key = [ i for i in range(cipher_round+1)]  #공격자가 모르는 키

for i in range(num_ptct_pairs):
    #pt = random.randint(0,255)
    pt = i
    ct = WC8.CipherWC8Round_Enc(pt, key, cipher_round)
    ptct_pair = copy.deepcopy([pt,ct])
    ptct_list.append(ptct_pair)
    
ptct_file = '3R_ptct_CipherWC8_256.var'
Common.save_var_to_file(ptct_list, ptct_file)
print('-- CipherWC8R', cipher_round, 'round version')
print(' The num. of pt-ct paris:', num_ptct_pairs)
print(' Saved to file:', ptct_file)
'''

#========================
# 선형공격
#-- 3라운드 암호화:  pt --> [xor k0] --> [S] --> [xor k1] --> [S] --> 
#                          [xor k2] -(y)-> [S] --> [xor k3] --> ct
# Max count = 128+128 (128 --> 4) --- Probability =  1.0
# Max count = 128-20 (4 --> 45) --- Probability =  0.578125
#----------------------------------

ptct_file = '3R_ptct_CipherWC8_256.var'
ptct_list = Common.load_var_from_file(ptct_file)
in_mask = 128
out_mask = 45

score_list = [0] * 256 # 공격대상 암호키 guessing --> 선형식을 만족하는 개수
for key_guess in range(256):
    for i in range(len(ptct_list)):
        pt, ct = ptct_list[i][0], ptct_list[i][1] # [ [pt1, ct1], [pt2, ct2], ...]
        y = WC8.IS[ct^key_guess]    
        x = pt
        if (Common.hw_mod2(in_mask & x)==Common.hw_mod2(out_mask & y)): # ax=by
            score_list[key_guess] += 1

# 키 후보의 카운트를 출력
print(score_list)

#------------
# 확률이 높은 키후보가 앞쪽에 오도록 정렬

#-- 정렬을 위한 기준함수
def MyOrder(x):
    return(x[1])

key_cadid_list = [ [i, abs(score_list[i]-128)] for i in range(256) ]
key_cadid_list.sort(reverse=True, key=MyOrder)
print(key_cadid_list[:10])


# k3 = 3 (원하는 키) --> 실제로는 4위권
# [[109, 26], [16, 24], [81, 24], [3, 20], [27, 18], [53, 18], [206, 18], [232, 18], [4, 16], [17, 16]]




