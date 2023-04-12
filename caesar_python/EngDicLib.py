'''
=======================
 영어사전 라이브러리
=======================
'''

UpAlphabet    = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters_and_space = UpAlphabet + UpAlphabet.lower() + " \t\n"

def load_dictionary():
    dic_file = open('myDic.txt')
    Eng_word = {} # 사전
    word_list = dic_file.read().split('\n')   # 리스트
    count = 0
    for word in word_list: 
        Eng_word[word] = None # { word: None }
        count += 1
    dic_file.close()
    print("(load_dictionary): Dictionary with %d words stored" %(count))
    return Eng_word

# 전역변수 - 영어사전
EnglishDic = load_dictionary()

def Remove_NonLetters(message):
    letters_only = []  
    for ch in message:
        if ch in letters_and_space:
            letters_only.append(ch) 
    return ''.join(letters_only) # 자료형: 문자열
    
# 올바른 영어단어의 비율 = (영어단어수)/(전체단어수)
def percentEngWord(message):
    message = message.lower()
    message = Remove_NonLetters(message)
    word_list = message.split()    
    total_word_count = len(word_list)    
    if total_word_count == 0:
        return 0.0
    eng_word_count = 0
    for word in word_list:
        if word in EnglishDic: 
            eng_word_count += 1    
    return float(eng_word_count)/total_word_count # 비율은 유리수이기 때문에 자료형을 float로 바꿔줌

def isEnglish(message, wordPercentage=20, letterPercentage=80):
    wordMatch = percentEngWord(message)*100 >= wordPercentage # 올바른 영어단어의 비율 >= 20%
    num_letters = len(Remove_NonLetters(message))
    letter_percent = float(num_letters)/len(message)*100 
    letterMatch = letter_percent >= letterPercentage # 올바른 letter 길이의 비율 >= 80%
    
    return wordMatch and letterMatch # 출력: True / False
    
def main():
    import CaesarLib as caesar
    PT = "This is a week 4 plaintext."
    key = 3
    CT = caesar.Caesar_Enc(PT, key)
    print('PT =', PT, isEnglish(PT))
    print('CT =', CT, isEnglish(CT))
    
#========
if __name__ == '__main__':
    main()
    
'''
# 출력    
(load_dictionary): Dictionary with 3053 words stored
PT = This is a week 4 plaintext. True
CT = Wklv lv d zhhn 4 sodlqwhaw. False
'''



