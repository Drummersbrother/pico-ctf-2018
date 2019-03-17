#!/usr/bin/env python
import os, sys
from flask import (Flask, render_template, request)

app = Flask(__name__)

def real_cipher(n):
    with open("flag.txt", "rb") as f:
        flag = f.read().rstrip()

    # Equivalent to just shuffling list(range(256))
    key = os.urandom(20)
    key = [x for x in key]
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % 20]) % 256
        S[i], S[j] = S[j], S[i]

    # Implementing https://gist.github.com/cdleary/188393
    keystream = []
    i, j = 0, 0
    for _ in range(len(flag)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream.append(S[(S[i] + S[j]) % 256])

    if not (0 <= n and n < len(flag)):
        return "invalid rotation"

    flag = flag[-len(flag) + n:] + flag[:n]
    c = ""
    l = []
    for i in range(len(flag)):
        c += chr(flag[i] ^ keystream[i])
        l.append(flag[i] ^ keystream[i])
    return c

    # note to self: https://www.youtube.com/watch?v=3e2KqgoB0TE


@app.route('/cipher')
def cipher():
    return real_cipher(request.args.get('rotation', default = 0, type = int))

@app.route('/')
def index():
    return render_template('index.html')

web = False

if __name__ == '__main__':
    if web:
        app.run()
    else:
        print("Experimenting")

        import base64
        for j in range(100):
            c1 = real_cipher(1)
            c2 = real_cipher(1)
            c1 = [ord(i) for i in c1]
            c2 = [ord(i) for i in c2]

            print([a ^ b for a, b in zip(c1, c2)])