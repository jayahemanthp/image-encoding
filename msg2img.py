from PIL import Image

img = input("Enter image name with extension: ")
msg = input("Enter text name with extension: ")

image = Image.open(f"input/{img}")

image = image.convert("RGB")
pixels = image.load()

width, height = image.size

def txt2bin(txt):
    return ''.join('{0:08b}'.format(ord(x), 'b') for x in txt)

def bin2txt(bin):
    return ''.join(chr(int(bin[i*8:i*8+8],2)) for i in range(len(bin)//8))

def encode_msg(txt):
    global pixels
    bin = txt2bin(txt)
    c = 0
    l = len(bin)
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]

            if (bin[c] == '1' and r%2==0) or (bin[c] == '0' and r%2==1):
                if r == 0:
                    r = 1
                else:
                    r -= 1
            
            if (bin[c+1] == '1' and g%2==0) or (bin[c+1] == '0' and g%2==1):
                if g == 0:
                    g = 1
                else:
                    g -= 1
            
            if (bin[c+2] == '1' and b%2==0) or (bin[c+2] == '0' and b%2==1):
                if b == 0:
                    b = 1
                else:
                    b -= 1
            
            pixels[x, y] = (r, g, b)
            c+=3

            if c+3 > l:
                break
        else:
            continue
        break
                
    image.save(f"output/encoded_{img.rsplit('.',1)[0]}.png")
    print(l//8, "Saved image")

def decode_msg():
    global pixels
    dec = ""
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]

            if r%2 == 0:
                dec += "0"
            else:
                dec += "1"

            if g%2 == 0:
                dec += "0"
            else:
                dec += "1"
            
            if b%2 == 0:
                dec += "0"
            else:
                dec += "1"
    
    return bin2txt(dec)

def encode():
    with open(f'input/{msg}') as f:
        string = f.read()
        if len(string)%3 == 1:
            string+='\r\n\r\n\r'
        elif len(string)%3 == 2:
            string+='\n\r\n\r'
        else:
            string+='\r\n\r'
        encode_msg(string)

def decode():
    with open(f'output/decoded_{msg}','w') as f:
        dec = decode_msg().split('\r\n\r',1)[0]
        f.write(dec)
        print(len(dec),"Saved txt file")

if input("Encode or Decode? (e/d): ") == 'e':
    encode()
else:
    decode()