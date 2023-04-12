#========================
# Caesar cipher 함수 라이브러리
# CT = Caesar_Enc(PT,key)
# PT = Caesar_Dec(CT,key)
#========================

def Caesar_Enc(PT, key):
    upAlphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowAlphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    CT = ""
    for ch in PT: 
        if ch in upAlphabet:
            idx = upAlphabet.find(ch)
            new_idx = (idx + key) % 26
            cipher_ch = upAlphabet[new_idx]
            CT = CT + cipher_ch
        elif ch in lowAlphabet:
            idx = lowAlphabet.find(ch)
            new_idx = (idx + key) % 26
            cipher_ch = lowAlphabet[new_idx]
            CT = CT + cipher_ch
        else:
            CT = CT + ch
    return CT

def Caesar_Dec(CT, key):
    upAlphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowAlphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    PT = ""
    for ch in CT: 
        if ch in upAlphabet:
            idx = upAlphabet.find(ch)
            new_idx = (idx - key) % 26
            plain_ch = upAlphabet[new_idx]
            PT = PT + plain_ch
        elif ch in lowAlphabet:
            idx = lowAlphabet.find(ch)
            new_idx = (idx - key) % 26
            plain_ch = lowAlphabet[new_idx]
            PT = PT + plain_ch
        else:
            PT = PT + ch
    return PT

#=========
def main():    
    PT = "Hello, Python! Welcome to Caesar Cipher Library!"
    key = 3
    CT = Caesar_Enc(PT, key)
    
    print("Plaintext = ", PT)    
    print("Ciphertext = ", CT)
    
    PT2 = Caesar_Dec(CT, key)
    print("Decrypted = ", PT2)

#========= 라이브러리 테스트용 함수 main() 호출
if __name__ == "__main__":
    main()

