#-------------------------
# 암호분석 2020
#-------------------------

import AES_lib as AES
import my_lib2 as Common
import random
import copy

#-----
# 입력 평문 256개 만들기 
# s256 = [ pt0, pt1, pt2, ... , pt255 ]
def plain_256(col, row):
    s256 = []
    new_state = []
    for i in range(4):
        new_col = [ random.randint(0,255) for j in range(4) ]
        new_state.append(new_col)
    
    for n in range(256):      
        new_state[col][row] = n
        #print(new_state)
        # 아래는 반드시 deepcopy로
        s256.append(copy.deepcopy(new_state))
        
    return s256

#-----
def xor_256_pos(col, row, s256):
    xor_ed = 0
    for n in range(256):
        xor_ed ^= s256[n][col][row]
    return xor_ed

#-----
def xor_256(s256):
    xor_state = []
    for col in range(4):
        xor_col = [ xor_256_pos(col, row, s256) for row in range(4) ]
        xor_state.append(xor_col)
    return xor_state


'''
#===========================================
# 4R AES의 선택평문, 암호문쌍 만들기 
    
round = 4
num_ptct_pairs = 256
key = [i for i in range(16)]  # 공격자가 모르는 암호키
state_key = AES.block2state(key)
rkey = AES.key_schedule_Enc(state_key)
for r in range(round+1):
    print("rk[",r,"]=", rkey[r])

pt256 = plain_256(0,0)  # [0][0] 위치만 P, 나머지는 C

ptct_list = []
for pt in pt256:
    ct = copy.deepcopy(AES.AES_EncR(pt, state_key, round))
    ptct_list.append([pt,ct])
    
ptct_file = 'AES4_ptct_256.var'
Common.save_var_to_file(ptct_list, ptct_file)
print('--- Cipher: AES 4 Round')
print('The number of pt-ct pairs: ', num_ptct_pairs)
print('File name:', ptct_file)
'''

'''
# 라운드키 출력
rk[ 0 ]= [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
rk[ 1 ]= [[214, 170, 116, 253], [210, 175, 114, 250], [218, 166, 120, 241], [214, 171, 118, 254]]
rk[ 2 ]= [[182, 146, 207, 11], [100, 61, 189, 241], [190, 155, 197, 0], [104, 48, 179, 254]]
rk[ 3 ]= [[182, 255, 116, 78], [210, 194, 201, 191], [108, 89, 12, 191], [4, 105, 191, 65]]
rk[ 4 ]= [[71, 247, 247, 188], [149, 53, 62, 3], [249, 108, 50, 188], [253, 5, 141, 253]]
--- Cipher: AES 4 Round
The number of pt-ct pairs:  256
File name: AES4_ptct_256.var
'''


#===========================================
# integral attack on AES 4 Round

ptct_file = 'AES4_ptct_256.var'
ptct_list = Common.load_var_from_file(ptct_file)

rk00_candidate = []
for rk00 in range(256):  # 4라운드 [0][0]위치의 라운드키 예측
    state_xor = 0
    for i in range(len(ptct_list)): 
        ct = ptct_list[i][1]
        state00 = AES.ISbox[rk00^ct[0][0]]
        state_xor ^= state00
    if state_xor == 0:  # Balanced에 만족
        rk00_candidate.append(rk00)

print('rk4[0][0] = ', rk00_candidate)

'''
rk10_candidate = []
for rk10 in range(256):  # 4라운드 [1][0]위치의 라운드키 예측
    state_xor = 0
    for i in range(len(ptct_list)): 
        ct = ptct_list[i][1]
        state10 = AES.ISbox[rk10^ct[1][0]]
        state_xor ^= state10
    if state_xor == 0:
        rk10_candidate.append(rk10)

print('rk4[1][0] = ', rk10_candidate)

rk20_candidate = []
for rk20 in range(256):  # 4라운드 [2][0]위치의 라운드키 예측
    state_xor = 0
    for i in range(len(ptct_list)): 
        ct = ptct_list[i][1]
        state20 = AES.ISbox[rk20^ct[2][0]]
        state_xor ^= state20
    if state_xor == 0:
        rk20_candidate.append(rk20)

print('rk4[2][0] = ', rk20_candidate)
'''