from pwn import *

# p = remote('localhost', 9020)
p = remote('175.123.252.156', 9999)
dic = {
    '0':'A',
    '1':'B',
    '2':'C'
}

def max_num_place(array, num):
    for i, hanoi in enumerate(array):
        for char in hanoi:
            if int(char) == num:
                return i

for three_time in range(3):
    payload = ""
    print(p.recvuntil(': '))
    tmp = p.recvline().decode()[:-1]
    print(tmp)
    top_list = tmp.split(',')
    max_num = 0
    for i, hanoi in enumerate(top_list):
        for char in hanoi:
            if int(char) > max_num:
                max_num = int(char)

    while True:
        try:
            # print(max_num)
            max_place = max_num_place(top_list, max_num)
            if max_place == 2:
                target_place = 1
            else:
                target_place = 1 - max_place
            iter = len(top_list[2])
            for j in range(iter):
                if int(top_list[2][0]) <= max_num:
                    top_list[target_place] = top_list[2][0] + top_list[target_place]
                    payload += dic['2'] + dic[str(target_place)]
                    top_list[2] = top_list[2][1:]
                else:
                    break
            
            iter = len(top_list[max_place])
            for j in range(iter):
                if int(top_list[max_place][0]) != max_num:
                    top_list[target_place] = top_list[max_place][0] + top_list[target_place]
                    payload += dic[str(max_place)] + dic[str(target_place)]
                    top_list[max_place] = top_list[max_place][1:]
                else:
                    top_list[2] = top_list[max_place][0] + top_list[2]
                    payload += dic[str(max_place)] + dic['2']
                    top_list[max_place] = top_list[max_place][1:]
            
            # print(top_list, payload)
            # input()
            max_num -= 1
            if max_num < 1:
                break
        except:
            max_num -= 1
            if max_num < 1:
                break

    print(payload)
    p.sendline(payload.encode())


p.interactive()

# 1) 3번 타워(C)에 가장 큰 디스크보다 작은 디스크가 존재하는 경우 C 타워를 비우기. 이 때 가장 큰 디스크(=max_num)를 제외하고 모든 디스크를 다른 임의의 한 타워에 넣기.
# 2) 가장 큰 디스크보다 1 작은 디스크를 1번에서 넣은 타워에 넣기.
# 3) 가장 큰 디스크를 C 타워로 옮긴 후 max_num을 1 줄이기
# 4) 1~3의 과정을 반복
# 5) max_num < 1이면 종료