from Crypto.Util.number import *
f = open("output.txt")
a = f.readlines()
ans = ""
for i in a:
	if i.strip() == "PING": ans += "1"
	else: ans += "0"
print(ans)
for i in range(0,len(ans),8):
	print(chr(int(ans[i:i+8],2)),end="")
print()
