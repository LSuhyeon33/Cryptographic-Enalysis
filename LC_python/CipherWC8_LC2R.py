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
cipher_round = 2 # 라운드 수
ptct_list = []
key = [ i for i in range(cipher_round+1)]  #공격자가 모르는 키

for i in range(num_ptct_pairs):
    #pt = random.randint(0,255)
    pt = i
    ct = WC8.CipherWC8Round_Enc(pt, key, cipher_round)
    ptct_pair = copy.deepcopy([pt,ct])
    ptct_list.append(ptct_pair)
    
ptct_file = '2R_ptct_CipherWC8_256.var'
Common.save_var_to_file(ptct_list, ptct_file)
print('-- CipherWC8', cipher_round, 'round version')
print(' The num. of pt-ct paris:', num_ptct_pairs)
print(' Saved to file:', ptct_file)
'''


#========================
# 선형공격
#-- 2라운드 암호화:  pt --> [xor k0] --> [S] --> [xor k1] -(y)-> [S] --> [xor k2] --> ct
# Max count = 128+128 (128 --> 4)
# Max_in_mask = 128 Max_out_mask = 4
# Max linear probability = 1.0
#----------------------------------

ptct_file = '2R_ptct_CipherWC8_256.var'
ptct_list = Common.load_var_from_file(ptct_file)
in_mask = 128
out_mask = 4

score_list = [0] * 256 # 공격대상 암호키 guessing --> 선형식을 만족하는 개수
for key_guess in range(256):
    for i in range(len(ptct_list)):
        pt, ct = ptct_list[i][0], ptct_list[i][1] # [ [pt1, ct1], [pt2, ct2], ...]
        y = WC8.IS[ct^key_guess]    
        x = pt
        if (Common.hw_mod2(in_mask & x)==Common.hw_mod2(out_mask & y)): # ax=by
            score_list[key_guess] += 1
print(score_list)

# rk[2] = 2 올바른 키
'''
[136, 112, 256, 112, 124, 120, 132, 132, 128, 120, 124, 136, 
 128, 108, 128, 132, 140, 124, 124, 120, 136, 144, 124, 120, 
 132, 112, 124, 116, 132, 136, 128, 116, 120, 128, 108, 132, 
 128, 112, 120, 120, 140, 152, 156, 120, 128, 124, 108, 132, 
 128, 128, 116, 124, 136, 132, 128, 116, 128, 132, 112, 140, 
 128, 136, 124, 136, 148, 108, 188, 132, 124, 120, 132, 132, 
 112, 136, 140, 136, 128, 108, 128, 132, 152, 124, 136, 112, 
 136, 144, 124, 120, 128, 108, 136, 112, 132, 136, 128, 116, 
 116, 144, 120, 132, 128, 112, 120, 120, 144, 132, 136, 148, 
 128, 124, 108, 132, 120, 124, 116, 112, 136, 132, 128, 116, 
 128, 132, 128, 132, 128, 136, 124, 136, 128, 112, 128, 132, 
 124, 140, 132, 136, 120, 132, 124, 120, 148, 116, 132, 132, 
 124, 144, 120, 136, 128, 128, 116, 128, 132, 124, 124, 124, 
 144, 132, 124, 128, 116, 132, 140, 104, 128, 136, 132, 132,
 144, 92, 148, 120, 132, 140, 132, 128, 124, 116, 136, 108, 
 132, 124, 128, 128, 128, 120, 136, 128, 120, 120, 112, 132, 
 116, 120, 144, 128, 124, 140, 132, 136, 120, 120, 96, 152, 
 148, 116, 132, 132, 128, 144, 120, 124, 128, 128, 116, 128,
 132, 120, 144, 116, 144, 132, 124, 128, 128, 120, 108, 136, 
 128, 136, 132, 132, 132, 120, 148, 104, 132, 140, 132, 128, 
 132, 116, 148, 104, 132, 124, 128, 128, 120, 120, 140, 116, 
 120, 120, 112, 132]
'''

