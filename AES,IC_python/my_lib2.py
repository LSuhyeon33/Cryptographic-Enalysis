#-------------------------
# 암호분석 2022
#-------------------------
import pickle    # 변수 저장
import random    # 난수 생성
import copy      # 딥 카피 (깊은 복사) 


#============================================================
# 이전에 만든 함수들
#============================================================
#--- int(4bytes) to list 0x12345678 -> [ 0x12, 0x34, 0x56, 0x78 ]
def int2list(n):
    out_list = []
    out_list.append( (n >> 24) & 0xff )
    out_list.append( (n >> 16) & 0xff )
    out_list.append( (n >>  8) & 0xff )
    out_list.append( (n      ) & 0xff )

    return out_list

#--- list to int [ 0x12, 0x34, 0x56, 0x78 ] -> 0x12345678
def list2int(l):
    n = 0
    num_byte = len(l)
    for i in range(len(l)):
        n += l[i] << 8*(num_byte - i -1)
        
    return n

#- 변수를 파일에 저장하기
def save_var_to_file(var, filename):
    f = open(filename, 'w+b')
    pickle.dump(var, f)
    f.close()
    
#- 파일에서 변수를 가져오기
def load_var_from_file(filename):
    f = open(filename, 'rb')
    var = pickle.load(f)
    f.close()
    return var
#============================================================
#== Hamming weight : 주어진 데이터를 이진수로 표현할 때, 1의 개수
# 예: hw(7) = hw(0111) = 3, hw(5) = hw(101) = 2
#== hamming weight
def hw(x):
    count = sum( [ x & (1<<i) >0 for i in range(32)])
    return count

def hw_mod2(n):
    return hw(n) % 2


def main():
    a = 20
    print("a= ",a, bin(a), "hw(a)=", hw(a), "hw_mod2(a)=", hw_mod2(a))

# Run main()

if __name__ == '__main__'    :
    main()
    