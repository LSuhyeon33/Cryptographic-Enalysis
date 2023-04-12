"""
=========================================
BC20R - Bad Cipher (encryption/decryption)

 - version 4:
         Bad Cipher - 취약한 Sbox 사용  (최대차분확률=1)
 - version 3:
            R: Reduced Round (부분 라운드 암호화 기능을 추가)
            Whitening(화이트닝) 추가 - 암호문 생성 직전에 라운드키 XOR 추가
 - version 2: 
      동일한 라운드함수만 사용함
      키 스케줄 없음
      복호화 추가
=========================================
"""

NUM_ROUND = 10

Sbox = [ 0x06,0x97,0x13,0xa1,0xa5,0xb1,0x92,0xb6,0x25,0x27,0xb3,0x00,0x15,0x05,0xb4,0x82,
        0x84,0x32,0xa6,0x87,0x26,0x22,0x86,0xb5,0x33,0x23,0x20,0x03,0x02,0x36,0x24,0x30,
        0x90,0x11,0x01,0x34,0x80,0x96,0x17,0x91,0xa2,0x35,0xa4,0xa0,0x31,0xa3,0xb0,0x95,
        0x21,0x07,0x81,0xb7,0x83,0x12,0x14,0x85,0xb2,0xa7,0x10,0x04,0x94,0x37,0x93,0x16,
        0x4e,0xdf,0x5b,0xe9,0xed,0xf9,0xda,0xfe,0x6d,0x6f,0xfb,0x48,0x5d,0x4d,0xfc,0xca,
        0xcc,0x7a,0xee,0xcf,0x6e,0x6a,0xce,0xfd,0x7b,0x6b,0x68,0x4b,0x4a,0x7e,0x6c,0x78,
        0xd8,0x59,0x49,0x7c,0xc8,0xde,0x5f,0xd9,0xea,0x7d,0xec,0xe8,0x79,0xeb,0xf8,0xdd,
        0x69,0x4f,0xc9,0xff,0xcb,0x5a,0x5c,0xcd,0xfa,0xef,0x58,0x4c,0xdc,0x7f,0xdb,0x5e,
        0x0e,0x9f,0x1b,0xa9,0xad,0xb9,0x9a,0xbe,0x2d,0x2f,0xbb,0x08,0x1d,0x0d,0xbc,0x8a,
        0x8c,0x3a,0xae,0x8f,0x2e,0x2a,0x8e,0xbd,0x3b,0x2b,0x28,0x0b,0x0a,0x3e,0x2c,0x38,
        0x98,0x19,0x09,0x3c,0x88,0x9e,0x1f,0x99,0xaa,0x3d,0xac,0xa8,0x39,0xab,0xb8,0x9d,
        0x29,0x0f,0x89,0xbf,0x8b,0x1a,0x1c,0x8d,0xba,0xaf,0x18,0x0c,0x9c,0x3f,0x9b,0x1e,
        0x46,0xd7,0x53,0xe1,0xe5,0xf1,0xd2,0xf6,0x65,0x67,0xf3,0x40,0x55,0x45,0xf4,0xc2,
        0xc4,0x72,0xe6,0xc7,0x66,0x62,0xc6,0xf5,0x73,0x63,0x60,0x43,0x42,0x76,0x64,0x70,
        0xd0,0x51,0x41,0x74,0xc0,0xd6,0x57,0xd1,0xe2,0x75,0xe4,0xe0,0x71,0xe3,0xf0,0xd5,
        0x61,0x47,0xc1,0xf7,0xc3,0x52,0x54,0xc5,0xf2,0xe7,0x50,0x44,0xd4,0x77,0xd3,0x56]

ISbox = [ 0x0b,0x22,0x1c,0x1b,0x3b,0x0d,0x00,0x31,0x8b,0xa2,0x9c,0x9b,0xbb,0x8d,0x80,0xb1,
        0x3a,0x21,0x35,0x02,0x36,0x0c,0x3f,0x26,0xba,0xa1,0xb5,0x82,0xb6,0x8c,0xbf,0xa6,
        0x1a,0x30,0x15,0x19,0x1e,0x08,0x14,0x09,0x9a,0xb0,0x95,0x99,0x9e,0x88,0x94,0x89,
        0x1f,0x2c,0x11,0x18,0x23,0x29,0x1d,0x3d,0x9f,0xac,0x91,0x98,0xa3,0xa9,0x9d,0xbd,
        0xcb,0xe2,0xdc,0xdb,0xfb,0xcd,0xc0,0xf1,0x4b,0x62,0x5c,0x5b,0x7b,0x4d,0x40,0x71,
        0xfa,0xe1,0xf5,0xc2,0xf6,0xcc,0xff,0xe6,0x7a,0x61,0x75,0x42,0x76,0x4c,0x7f,0x66,
        0xda,0xf0,0xd5,0xd9,0xde,0xc8,0xd4,0xc9,0x5a,0x70,0x55,0x59,0x5e,0x48,0x54,0x49,
        0xdf,0xec,0xd1,0xd8,0xe3,0xe9,0xdd,0xfd,0x5f,0x6c,0x51,0x58,0x63,0x69,0x5d,0x7d,
        0x24,0x32,0x0f,0x34,0x10,0x37,0x16,0x13,0xa4,0xb2,0x8f,0xb4,0x90,0xb7,0x96,0x93,
        0x20,0x27,0x06,0x3e,0x3c,0x2f,0x25,0x01,0xa0,0xa7,0x86,0xbe,0xbc,0xaf,0xa5,0x81,
        0x2b,0x03,0x28,0x2d,0x2a,0x04,0x12,0x39,0xab,0x83,0xa8,0xad,0xaa,0x84,0x92,0xb9,
        0x2e,0x05,0x38,0x0a,0x0e,0x17,0x07,0x33,0xae,0x85,0xb8,0x8a,0x8e,0x97,0x87,0xb3,
        0xe4,0xf2,0xcf,0xf4,0xd0,0xf7,0xd6,0xd3,0x64,0x72,0x4f,0x74,0x50,0x77,0x56,0x53,
        0xe0,0xe7,0xc6,0xfe,0xfc,0xef,0xe5,0xc1,0x60,0x67,0x46,0x7e,0x7c,0x6f,0x65,0x41,
        0xeb,0xc3,0xe8,0xed,0xea,0xc4,0xd2,0xf9,0x6b,0x43,0x68,0x6d,0x6a,0x44,0x52,0x79,
        0xee,0xc5,0xf8,0xca,0xce,0xd7,0xc7,0xf3,0x6e,0x45,0x78,0x4a,0x4e,0x57,0x47,0x73 ]

#--------
# AR: Add Roundkey
def AR(in_state, rkey):
    out_state = [0] * len(in_state)
    for i in range(len(in_state)):
        out_state[i] = in_state[i] ^ rkey[i] 
    return out_state

#--------
# SB: Sbox layer
def SB(in_state):
    out_state = [0] * len(in_state)
    for i in range(len(in_state)):
        out_state[i] = Sbox[in_state[i]]
    return out_state

#--------
# LM: Linear Map
def LM(in_state):
    out_state = [0] * len(in_state)
    All_Xor = in_state[0] ^ in_state[1] ^ in_state[2] ^ in_state[3]
    for i in range(len(in_state)):
        out_state[i] = All_Xor ^ in_state[i]
    return out_state

#--------
# Enc_Round
def Enc_Round(in_state, rkey):
    out_state = [0] * len(in_state)
    out_state = AR(in_state, rkey)
    in_state = SB(out_state)
    out_state = LM(in_state)
    return out_state

#--------
# BC20R Encryption (전체 라운드 암호화)
def BC20R_Enc(PT, key):
    NROUND = NUM_ROUND # 라운드 수 = 10
    CT = PT #CT = [0] * len(PT)
    for i in range(NROUND):
        CT = Enc_Round(CT, key)
    #암호문 생성 직전 화이트닝 추가
    CT = AR(CT, key)
    return CT

# BC20R Encryption (부분 라운드 암호화)
def BC20R_Enc_Reduced_Round(PT, key, numRound):
    CT = PT #CT = [0] * len(PT)
    for i in range(numRound):  # 주어진 라운드 수 만큼만 암호화
        CT = Enc_Round(CT, key)
    #암호문 생성 직전 화이트닝 추가
    CT = AR(CT, key)
    return CT

#--------------------------------------
#  Decryption
#--------------------------------------

#-- SB: Sbox layer
def ISB(in_state):
    out_state = [0, 0, 0, 0]
    for i in range(len(in_state)):
        out_state[i] = ISbox[in_state[i]]
    return out_state

#-- Decrypt Round
def Dec_Round(in_state, rkey):
    out_state1 = [0, 0, 0, 0]
    out_state2 = [0, 0, 0, 0]
    out_state3 = [0, 0, 0, 0]
    out_state1 = LM(in_state)
    out_state2 = ISB(out_state1)
    out_state3 = AR(out_state2, rkey)
        
    return out_state3

#-- BC20R Decryption (부분 라운드 복호화)
def BC20R_Dec(input_state, key):
    # 복호화 시작전 화이트닝 추가
    state = AR(input_state, key)
    numRound = NUM_ROUND # 라운드 수
    for i in range(0, numRound):
        state = Dec_Round(state, key)

    return state

#-- BC20R Decryption (전체 라운드 복호화)
def BC20R_Dec_Reduced_Round(input_state, key, numRound):
    # 복호화 시작전 화이트닝 추가
    state = AR(input_state, key)
    for i in range(0, numRound):
        state = Dec_Round(state, key)

    return state
#-----------
# main()
def main():
    '''
    # ISbox 만들기
    ISbox = [0]*len(Sbox)
    for i in range(len(Sbox)):
        ISbox[Sbox[i]] = i
    
    print("ISbox = [ ")
    for i in range(len(Sbox)):
        print(hex(ISbox[i]), end=',')
        if ((i%16)==15):
            print()
    print(']')
    '''
    
    #print('BC20R-full-round-test==>')
    print('BC20R-5-round-test==>')
    message = 'ARIA'
    key = [0, 1, 2, 3]
    #PT = list(message)
    PT = [ ord(ch) for ch in message ]
    print('Message =', message)
    print('PT =', PT)
    #CT = BC20R_Enc(PT, key)
    CT = BC20R_Enc_Reduced_Round(PT, key, 5)
    print('CT =', CT)
    hexPT = [hex(item) for item in PT]
    hexCT = [hex(item) for item in CT]
    print('hexPT =', hexPT)
    print('hexCT =', hexCT)
    bytePT = bytes(PT)
    print('bytePT =', bytePT)
    byteCT = bytes(CT)
    print('byteCT =', byteCT)
        
    input_state = CT
    #output_state = BC20R_Dec(input_state, key)
    output_state = BC20R_Dec_Reduced_Round(input_state, key, 5)
    print('input ciphertext =', input_state)
    print('output plaintext =', output_state)
    

    
#----- Run main()
if __name__ == '__main__':
    main()
    
      
'''  
BC20R-5-round-test==>
Message = ARIA
PT = [65, 82, 73, 65]
CT = [124, 252, 70, 111]
hexPT = ['0x41', '0x52', '0x49', '0x41']
hexCT = ['0x7c', '0xfc', '0x46', '0x6f']
bytePT = b'ARIA'
byteCT = b'|\xfcFo'
input ciphertext = [124, 252, 70, 111]
output plaintext = [65, 82, 73, 65]

BC20R-full-round-test==>
Message = ARIA
PT = [65, 82, 73, 65]
CT = [113, 202, 88, 84]
hexPT = ['0x41', '0x52', '0x49', '0x41']
hexCT = ['0x71', '0xca', '0x58', '0x54']
bytePT = b'ARIA'
byteCT = b'q\xcaXT'
input ciphertext = [113, 202, 88, 84]
output plaintext = [65, 82, 73, 65]
''' 



