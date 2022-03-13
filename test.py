from string import ascii_letters
from PIL import ImageFont
myFont2 = ImageFont.truetype('font/Poppins-Medium.ttf', 40)

for char in ascii_letters:
    print(myFont2.getsize(char)[0])