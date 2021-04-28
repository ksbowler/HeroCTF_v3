from Crypto.Util.number import *
#import sympy
from functools import reduce
from operator import mul
from itertools import combinations
import sys
import socket, struct, telnetlib
import string

# --- common funcs ---
def sock(remoteip, remoteport):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((remoteip, remoteport))
	return s, s.makefile('rw')

def read_until(f, delim='\n'):
	data = ''
	while not data.endswith(delim):
		data += f.read(1)
	return data

candi = "ABCDEFGHJIKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890{}_"
FLAG = "Hero{test_flag}" #簡易的なflag。途中msgを出力している際に入力として送る文字列が正しい長さ確認する
flag = "Hero{"
isbreak = False #終了条件
#tempをシフトさせていって1文字ずつbrute forceしていく
temp = "assword : Hero{"
k = len(" !\n\nYour p") #paddingする際の長さ
print(k)
L = 16 #paddingで送る長さ調整。k=16になった時は32にする。
M = 3 #暗号化されたflagが何blockにあたるか
while True:
	printmsg = True
	print("k :",k)
	for i in candi:
		print(i)
		HOST, PORT = "chall0.heroctf.fr", 10000
		s, f = sock(HOST, PORT)
		_ = read_until(f)
		read_until(f,"ID : ")
		account_id = "12" + temp + i + "0"*(L-k)
		_msg = f"""
Welcome back {account_id} !

Your password : {FLAG}

Regards
"""
		#送る入力が正しいものになっているか。特に長さの確認
		if printmsg:
			for j in range(0,len(_msg),16):
				print(j//16,_msg[j:j+16])
		msg = "12" + temp + i + "0"*(L-k)
		s.send(msg.encode()+b"\n")
		ct = read_until(f).strip()
		assert len(ct)%32 == 0
		cip = []
		for j in range(0,len(ct),32):
			cip.append(ct[j:j+32])
		if cip[1] == cip[M]:
			print(i)
			s.close()
			flag += i
			if i == "}":
				print("This is the flag!")
				print(flag)
				isbreak = True
				break
			print(flag)
			temp = temp[1:] + i
			k += 1
			if k == 16:
				L += 16
				M += 1
			break
		s.close()
		printmsg = False
	if isbreak: break
#read_untilの使い方
#返り値があるのでprintするか、何かの変数に入れる
#1行読む：read_until(f)
#特定の文字まで読む：read_until(f,"input")
#配列に格納する：recv_m = read_until(f).split() ot .strip()

#サーバーに何か送るとき
#s.send(b'1\n') : 1を送っている
#バイト列で送ること。str->bytesにするには、変数の後に.encode()
#必ず改行を入れること。終了ポイントが分からなくなる。ex) s.send(flag.encode() + b'\n')

