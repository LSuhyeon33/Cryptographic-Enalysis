#-------------------------
# 암호분석 2020
#-------------------------

import random 
import WC20R_lib as WC20R 
import my_lib as Common
import copy
import os

'''
#========================
# BSbox의 차분 확률 계산
# 64 --> 64 (확률 p = 132/256 = 0.52)
dx = 64
num_iteration = 100
counter = 0

for i in range(num_iteration):
    P1 = random.randint(0, 255)
    P2 = P1^64
    C1 = WC20R.Sbox[P1]
    C2 = WC20R.Sbox[P2]
    dy = C1^C2
    if dy == 64:
        counter += 1

print('%d --> %d (probability = %5.3f)' %(dx, dx, counter/num_iteration))
# OUTPIT: 64 --> 64 (probability = 0.560)
#========================
'''


#========================
# WC20R 1라운드 차분 특성
# [64, 0, 0, 0] ---> [0, 64, 64, 64]
# 차분확률 p = 0.52
'''
dx = 64
num_iteration = 100
counter = 0
diff_dic = {}
key = [ 1, 2, 3, 4]

for i in range(num_iteration):
    P1 = [ random.randint(0,255), random.randint(0,255), \
           random.randint(0,255), random.randint(0,255)]
    P2 = [ P1[0]^dx, P1[1], P1[2], P1[3]]
    # P1^P2 = [dx, 0, 0, 0]
    C1 = WC20R.WC20R_Enc_Reduced_Round(P1, key, 1)
    C2 = WC20R.WC20R_Enc_Reduced_Round(P2, key, 1)
    dy = [ C1[i]^C2[i] for i in range(4) ]
    dy_int = Common.list2int(dy)
    if dy_int in diff_dic:
        diff_dic[dy_int].append(P1)
    else:
        diff_dic[dy_int] = [ P1 ]
    
    expected_dy = [ 0, 64, 64, 64]
    expected_int = Common.list2int(expected_dy)
    if expected_int == dy_int:
        counter += 1

print('probability =', counter/num_iteration)
print(diff_dic[expected_int])
#========================
'''


#========================
# WC20R  r 라운드 차분 특성
# 예: 3라운드: [64, 0, 0, 0] ---> [0, 64, 64, 64]
# [64, 0, 0, 0] --> [0, 64, 64, 64] --> [64, 0, 0, 0] --> [0, 64, 64, 64]
# 차분확률 p^5 = 0.52^5
'''
dx = 64
num_iteration = 1000
num_round = 4 
counter = 0
diff_dic = {}
key = [ 1, 2, 3, 4]

for i in range(num_iteration):
    P1 = [ random.randint(0,255), random.randint(0,255), \
           random.randint(0,255), random.randint(0,255)]
    P2 = [ P1[0]^dx, P1[1], P1[2], P1[3]]
    # P1^P2 = [dx, 0, 0, 0]
    C1 = WC20R.WC20R_Enc_Reduced_Round(P1, key, num_round)
    C2 = WC20R.WC20R_Enc_Reduced_Round(P2, key, num_round)
    dy = [ C1[i]^C2[i] for i in range(4) ]
    dy_int = Common.list2int(dy)
    if dy_int in diff_dic:
        diff_dic[dy_int].append(P1)
    else:
        diff_dic[dy_int] = [ P1 ]
    
    #expected_dy = [ 0, 64, 64, 64]   # 3 라운드 설정에만 유효한 값
    expected_dy = [ 64, 0, 0, 0]   # 4 라운드 설정에만 유효한 값
    expected_int = Common.list2int(expected_dy)
    if expected_int == dy_int:
        counter += 1

print('Expected probability = %7.5f' %(pow(132/256,8)))
print('probability =', counter/num_iteration)
if counter !=0: # 카운터가 0이 아닌 경우만 출력한다. (오류방지)
    print(diff_dic[expected_int])
#========================
'''

'''
#========================
# (평문, 암호문) 쌍 만들기
dx = 64
num_ptct_pairs = 1<<16
num_round = 4 # 3라운드 특성을 이용한 4라운드 공격
ptct_list = []
key = [ 1, 2, 3, 4]  # 공격자가 찾아야 하는 

for i in range(num_ptct_pairs):
    P1 = [ random.randint(0,255), random.randint(0,255), \
           random.randint(0,255), random.randint(0,255)]
    P2 = [ P1[0]^dx, P1[1], P1[2], P1[3]]
    # P1^P2 = [dx, 0, 0, 0]
    C1 = WC20R.WC20R_Enc_Reduced_Round(P1, key, num_round)
    C2 = WC20R.WC20R_Enc_Reduced_Round(P2, key, num_round)    
    ptct_pair = copy.deepcopy([P1, P2, C1, C2])
    ptct_list.append(ptct_pair)
    # ptct_list = [ [P1, P2, C1, C2], [P1, P2, C1, C2], [P1, P2, C1, C2], ...]

ptct_file = '4R_ptct_65536.var'
# 파일에 (평문, 암호문) 쌍을 저장하기
Common.save_var_to_file(ptct_list, ptct_file)
#========================
'''


#========================
# 4R 차분공격: 3R 특성을 이용한 4R 공격법
# 4번째 라운드: AR(rk3) --> Sbox() ---> LM() ---> AR(rk4) --> CT
# 4번째 라운드: AR(rk3) --> Bbox() ---> AR(IM(rk)) ---> LM() --> CT
# 차분전파: [dx,0,0,0] --(1~3R)--> [0,dx,dx,dx] --(4R) --> CT

# 공격에 필요한 (평문, 암호문) 쌍 가져오기
ptct_file = '4R_ptct_65536.var'
ptct_list = Common.load_var_from_file(ptct_file)  # [P1, P2, C1, C2]

dx = 64
num_round = 4
rkey_dic = {}
for i in range(len(ptct_list)):
    C1 = copy.deepcopy(ptct_list[i][2])
    C2 = copy.deepcopy(ptct_list[i][3])
    state1 = WC20R.LM(C1)
    state2 = WC20R.LM(C2)
    for rk in range(256):  # 라운드키 rk[1]의 후보
        byte1 = WC20R.ISbox[ state1[3] ^ rk ]
        byte2 = WC20R.ISbox[ state2[3] ^ rk ]
        if (byte1 ^ byte2) == dx :
            if rk in rkey_dic:
                rkey_dic[rk] += 1
            else:
                rkey_dic[rk] = 1

max_count = 0
max_rk = 0
for rk in rkey_dic:
    if rkey_dic[rk] > max_count:
        max_count = rkey_dic[rk]
        max_rk = rk

print(max_rk, rkey_dic[max_rk])
print(rkey_dic)                
#========================

'''
LM [1,2,3,4] = [rk0, rk1, rk2, rk3] = [ 5, 6, 7, 0]
2^3^4 = 010 ^ 011 ^ 100 = 101 = 5
1^3^4 = 001 ^ 011 ^ 100 = 110 = 6
1^2^4 = 001 ^ 010 ^ 100 = 111 = 7
1^2^3 = 001 ^ 010 ^ 011 = 000 = 0
'''

            
        
        
        
         
        
