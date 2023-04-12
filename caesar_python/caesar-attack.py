#--------------
# 암호분석 2022
#--------------

# 사전을 이용한 Caesar 암호 공격

import CaesarLib as caesar  # 라이브러리 활용
import EngDicLib  # 영어사전 라이브러리

My_Cipher =  "Wklv lv d zhhn 4 sodlqwhaw."

for key in range(0,26): # 0,1,2,...,25
    Decrypted = caesar.Caesar_Dec(My_Cipher, key)
    if EngDicLib.isEnglish(Decrypted):
        print("key =", key, " : ", Decrypted)

'''   
(load_dictionary): Dictionary with 3053 words stored
key = 3  :  This is a week 4 plaintext.

key = 0  :  Wklv lv d zhhn 4 sodlqwhaw.
key = 1  :  Vjku ku c yggm 4 rnckpvgzv.
key = 2  :  Uijt jt b xffl 4 qmbjoufyu.
key = 3  :  This is a week 4 plaintext.
key = 4  :  Sghr hr z vddj 4 okzhmsdws.
key = 5  :  Rfgq gq y ucci 4 njyglrcvr.
key = 6  :  Qefp fp x tbbh 4 mixfkqbuq.
key = 7  :  Pdeo eo w saag 4 lhwejpatp.
key = 8  :  Ocdn dn v rzzf 4 kgvdiozso.
key = 9  :  Nbcm cm u qyye 4 jfuchnyrn.
key = 10  :  Mabl bl t pxxd 4 ietbgmxqm.
key = 11  :  Lzak ak s owwc 4 hdsaflwpl.
key = 12  :  Kyzj zj r nvvb 4 gcrzekvok.
key = 13  :  Jxyi yi q muua 4 fbqydjunj.
key = 14  :  Iwxh xh p lttz 4 eapxcitmi.
key = 15  :  Hvwg wg o kssy 4 dzowbhslh.
key = 16  :  Guvf vf n jrrx 4 cynvagrkg.
key = 17  :  Ftue ue m iqqw 4 bxmuzfqjf.
key = 18  :  Estd td l hppv 4 awltyepie.
key = 19  :  Drsc sc k goou 4 zvksxdohd.
key = 20  :  Cqrb rb j fnnt 4 yujrwcngc.
key = 21  :  Bpqa qa i emms 4 xtiqvbmfb.
key = 22  :  Aopz pz h dllr 4 wshpualea.
key = 23  :  Znoy oy g ckkq 4 vrgotzkdz.
key = 24  :  Ymnx nx f bjjp 4 uqfnsyjcy.
key = 25  :  Xlmw mw e aiio 4 tpemrxibx.
'''