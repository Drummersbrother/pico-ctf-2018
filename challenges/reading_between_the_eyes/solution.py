from PIL import Image 
 
def ExtractMessage(carrier, channel): 
    c_image = Image.open(carrier) 
    width, height = c_image.size 
    new_array = [] 
 
    for h in range(height): 
        for w in range(width): 
            ip = c_image.getpixel((w,h)) 
            new_array.append(ip[channel] & 2**0) 
    return new_array

filename = "husky.png"
red_lsbs = ExtractMessage(filename, 0)
green_lsbs = ExtractMessage(filename, 1)
blue_lsbs = ExtractMessage(filename, 2)
print(red_lsbs[:100])
print(green_lsbs[:100])
print(blue_lsbs[:100])

reds = red_lsbs[:96]
greens = green_lsbs[:96]
blues = blue_lsbs[:96]

reds = [sum(2**(7-i) for i, y in enumerate(reds[i:i+8]) if y == 1) for i in range(0, 96, 8)]
greens = [sum(2**(7-i) for i, y in enumerate(greens[i:i+8]) if y == 1) for i in range(0, 96, 8)]
blues = [sum(2**(7-i) for i, y in enumerate(blues[i:i+8]) if y == 1) for i in range(0, 96, 8)]

print("".join(chr(x) for x in reds))
print("".join(chr(x) for x in greens))
print("".join(chr(x) for x in blues))
