import requests
import time
import subprocess
import math

php = """
<?php
srand(time());
echo rand();
?>
"""

def phpRandom(timestamp):
    with open("phpRandom.php", "w") as f:
        f.write(php.replace("time()", str(timestamp)))
    s = subprocess.Popen(["php", "phpRandom.php"], stdout=subprocess.PIPE)
    nums = s.communicate()[0]
    return int(nums)

buffer = 0.15 # give buffer for correct sync with server
session = requests.session()
url = "http://35.228.19.189:7564/"
captchaRound = 1
requestsPerSecond = 50

def bitLength(i):
    return math.floor(math.log(i, 2) + 1)

while True:
    toWait = 2
    originalTime = math.floor(time.time())
    while True:
        num = phpRandom(originalTime + toWait)
        roundBitLength = bitLength(captchaRound)
        if num >> roundBitLength << roundBitLength == num:
            print("found magic second in %s seconds" % toWait)
            break
        toWait += 1
    
    print("sleeping %ss" % round(((toWait + originalTime) - time.time()) + buffer, 1))
    time.sleep(((toWait + originalTime) - time.time()) + buffer) # wait until magic second + buffer

    initialBitlength = bitLength(captchaRound)
    for i in range(requestsPerSecond):
        if bitLength(captchaRound) != initialBitlength:
            print("quitting second early because round bitlength changed")
            break

        r = session.post(url, data={"num": 0})
        response = r.content.decode()
        if response.startswith("Wr"): # wrong guess
            print("incorrect guess, adjust buffer and requestsPerSecond")
            exit()
        if response.startswith("Correct guess!C"): # got flag
            print(response.replace("Correct guess!CONGRATS! ", ""))
            exit()
        print("correct guess, %s/50" % captchaRound)
        captchaRound += 1
