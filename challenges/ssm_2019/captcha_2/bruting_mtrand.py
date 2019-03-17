import ctypes
from ctypes.util import find_library
from time import time
from math import floor

libc = ctypes.CDLL(find_library('c'))
rand = libc.rand
srand = libc.srand
rand_max = 2147483647
size_lmt = int(10e6)

from datetime import datetime

#time_string = input("Give http time string pls...")
#server_time = int(datetime.strptime(time_string, "%a, %d %b %Y %X %Z").strftime("%s"))
server_time = floor(time())
print("Time difference between you and the server is", round(time() - server_time), "seconds.")

def try_brute(start_time, hint_num):
    srand(server_time)
    first_mask = rand() % rand_max
    mangles = []
    for i in range(7):
        choice = (rand() % 4) + 1
        data = (rand() % size_lmt) + 1
        mangles.append((choice, data))
    mangles = tuple(mangles)


    # Check for each possible mt_rand
    cur_round = 1000000

    for mt_rand in range(1, cur_round+1):
        #print("Trying", mt_rand, "...")
        # Use the first mask
        cur_rand = mt_rand & first_mask
        cur_rand %= size_lmt
        # Do the bitmangling
        cur_answer = cur_rand

        # We continue to mangle to check with the hint number
        for choice, data in mangles:
            if choice == 1:
                cur_rand &= data
            elif choice == 2:
                cur_rand |= data
            elif choice == 3:
                cur_rand ^= data
            elif choice == 4:
                cur_rand += data

        cur_rand %= size_lmt
        if cur_rand == hint_num:
            print("Was equal, answer is:", cur_answer)

range_sz = 4
given_hint_num = int(input("Give hint pls..."))
offset = -20

while True:
    print("Offset now", offset)
    try_brute(offset + server_time, given_hint_num)
    offset += 1
