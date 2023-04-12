
import os, sys

out_file = 'week3_msg.txt'

#- 파일 덮어쓰기 확인
if os.path.exists(out_file):
    print("Overwrite? [Y]es or [Q]uit")
    response = input("> ")
    if response.lower().startwith('q'):
        print("File exits. Quit...")
        sys.exit()

outFileObj = open(out_file, 'w')  #쓰기모드로 열기
print("Write your message here (1 line):")
msg = input()
outFileObj.write(msg)
outFileObj.close()

#-- 결과 확인 메시지
print("Out File was written in ", os.getcwd()) #os.getcwd() 주소 출력
print("Week 3 Msg = ", msg)

in_file = input("Enter input fiel > ")

inFileObj = open(in_file)
msg = inFileObj.read()
inFileObj.close()

print("Message from file - ", in_file)
print(msg)






































































