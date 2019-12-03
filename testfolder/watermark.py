from PIL import Image, ImageDraw, ImageFont

image = Image.open("udanLiris.jpg")
drawing = ImageDraw.Draw(image)

black = (3, 8, 12)
width, height = image.size
text='FPKOMPUTASIAWAN'
font = ImageFont.truetype("./arial.ttf",int(height/15))
w, h = drawing.textsize(text,font=font)
pos=((width-w)/2, (height-h)/2)
drawing.text(pos, text, fill=black,font=font)
image.show()
image.save('watermark.jpg')