from PIL import Image
img = Image.open('bonas.png','r')
pix = img.getdata()
bins = ""
outfile = open("steg.rar","wb")

for i in pix:
    # extract LSB
    bins += bin(i)[-1]

xs = bytearray()
for j in range(0, len(bins), 8):
    c = int(bins[j:j+8],2)
    xs.append(c)
outfile.write(xs)


