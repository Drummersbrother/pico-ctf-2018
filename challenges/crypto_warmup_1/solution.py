c = "llkjmlmpadkkc"
k = "thisisalilkey"

m = [ord(x) - ord(k[inx]) for inx, x in enumerate(c)]
m = [chr((x % 26) + 97) for x in m]

print("picoCTF{"+"".join(m).upper()+"}")