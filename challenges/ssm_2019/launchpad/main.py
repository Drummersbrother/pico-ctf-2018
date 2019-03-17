#!/usr/bin/env python3
from flag import flag
from hashlib import sha256

def cryptnate(func, plaintext = ['No string provided']):
  if func == 'identity':
    return ' '.join(plaintext)
  if func == 'flagHash':
    plaintext[0] = flag

  if func != 'hash':
    return sha256(' '.join(plaintext).encode()).hexdigest()

if __name__ == '__main__':
  while True:
    line = input().split(' ')
    if len(line) == 1:
      print(cryptnate(line[0]))
    else:
      print(cryptnate(line[0], line[1:]))
