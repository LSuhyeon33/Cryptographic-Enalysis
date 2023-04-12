#=================
#  암호분석 2022
#=================

'''
## 데이터 출력: 10진, 16진, 2진 포맷
a=13  # 13 = 0x0D = 1101
print(a, hex(a))  #  13 0xd --- hex(13): 문자열
print(a, bin(a), format(a,"#04x"))  # 13 0b1101 0x0d
print(a, format(a,"#04X")) # 13 0X0D

b=45
print(a, bin(a), format(a, "#010b"))
print(b, bin(b), format(b, "#010b"))
'''

#S = [ 0, 1, 3, 2, 6, 7, 5, 4 ]  # linear function
S = [ 0, 1, 7, 2, 3, 4, 5, 6] # nonlinear function

'''
#Sbox 출력하기
for i in range(len(S)):
    #print("S[%d] = %d" %(i, S[i]))
    #print("S[%02x] = %02x" %(i, S[i]))
    print("S[", format(i, "#05b"), "]=", format(S[i],"#05b"))
'''

# 헤밍무게(Hamming weight) - 1의 개수 
# 예: hw(6) = hw(110) = 2
def hw(x):  # x는 32비트 이하의 정수(양수)
    return sum([ x & (1<<i) > 0 for i in range(32) ])  # [1, 1, 0]
'''
for i in range(len(S)):
    print("S[", format(i, "#05b"), "]=", format(S[i],"#05b"), "hw=", hw(S[i]))    

S[ 0b000 ]= 0b000 hw= 0
S[ 0b001 ]= 0b001 hw= 1
S[ 0b010 ]= 0b111 hw= 3
S[ 0b011 ]= 0b010 hw= 1
S[ 0b100 ]= 0b011 hw= 2
S[ 0b101 ]= 0b100 hw= 1
S[ 0b110 ]= 0b101 hw= 2
S[ 0b111 ]= 0b110 hw= 2
'''

# 선형특성표
# 테이블 LTable[a][b]: a x = b S[x]  ( a x : 벡터 a, x의 내적 GF(2)^3)
# a = 011, x = 101 --> a x = (0,1,1) (1,0,1) = 0*1 + 1*0 + 1*1 = 1
# a = 011, x = 111 --> a x = (0,1,1) (1,1,1) = 0*1 + 1*1 + 1*1 = 0

# 테이블 초기화
LTable = []
n = len(S)
for i in range(n):
    LTable.append([0]*n)
#print(LTable)

# 입출력 마스크 a(in_maks),b(out_mask)에 대하여 테이블 만들기
for in_mask in range(n): # in_mask = 000, 001, 010, ... , 111
    for out_mask in range(n): # out_mask = 000, 001, 010, ... , 111
        count = 0
        for x in range(n): #입력 x = 000, 001, ... ,111
            # a x = b S[x] <==> hw(a x) % 2 == hw (b S[x]) % 2  ==> {hw(a x) % 2 == 1 ? a x == 1 : a x == 0}
            # <==> ( hw(a x) - hw(b S[x]) ) %2 == 0
            if (hw(in_mask & x) - hw(out_mask & S[x])) %2 == 0: # a x = b S[x]
                count += 1
        LTable[in_mask][out_mask] = count - n/2

# 선형특성테이블 출력
print('    ', end='')
for i in range(n):
    print("%3d " %(i), end='')
print("\n")
for in_mask in range(n):
    print("%3d " %(in_mask), end='')
    for out_mask in range(n):
        print("%3d " %(LTable[in_mask][out_mask]), end='')
    print("\n")

#최대선형확률 구하기
max_count = 0
max_in_mask, max_out_mask = 0, 0
for in_mask in range(1,n):
    for out_mask in range(n):
        if abs(LTable[in_mask][out_mask]) > max_count:
            max_count = abs(LTable[in_mask][out_mask])
            max_in_mask, max_out_mask = in_mask, out_mask

print('Max count =', max_count)
print('Max_in_mask =', max_in_mask, 'Max_out_mask =', max_out_mask)
print("Max linear probability =", (abs(max_count)+n/2)/n)
    
''' 
Max count = 4.0
Max_in_mask = 1 Max_out_mask = 7
Max linear probability = 1.0
'''
'''
Max count = 2.0
Max_in_mask = 1 Max_out_mask = 1
Max linear probability = 0.75
'''

# 직접 해볼 것
# 8비트 Sbox들에 대하여 최대선형확률을 계산해볼 것
# TC20R, WC20R, BC20R


