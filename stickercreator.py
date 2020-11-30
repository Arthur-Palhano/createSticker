from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import urllib.request
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

options = Options()
options.headless = True

def calcBrightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale

def getWord():
    firefox = webdriver.Firefox(options=options)
    firefox.get("https://www.palabrasaleatorias.com/palavras-aleatorias.php?fs=1&fs2=0&Submit=Nova+palavra")
    word = firefox.find_element_by_xpath("/html/body/center/center/table[1]/tbody/tr/td/div")
    word = word.text
    firefox.close()
    return word

def getimage():
    firefox = webdriver.Firefox(options=options)
    firefox.get("https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria")
    key = firefox.find_element_by_id("firstHeading")
    key = key.text

    firefox.get(f"https://www.google.com/search?q={key}%20&tbm=isch&hl=pt-BR&safe=active&tbs=itp:face%2Cisz:l&sa=X&ved=0CAEQpwVqFwoTCMDC5-rjqO0CFQAAAAAdAAAAABAC&biw=1809&bih=978")
    src = firefox.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/a[1]/div[1]/img").get_attribute('src')
    urllib.request.urlretrieve(src, "img.png")

    firefox.close()

def editImage(c):
    img = Image.open("img.png")
    draw = ImageDraw.Draw(img)

    FONTSIZE = 1
    FONTCOLOR = (255, 255, 255, 255) if calcBrightness(img) < 0.5 else (0, 0, 0, 255)
    WP = 0.8
    HP = 0.8
    word = getWord()
    font = ImageFont.truetype("font.ttf", FONTSIZE)
    W, H = img.size

    while draw.textsize(word, font)[0] < WP * W:
        FONTSIZE += 2
        font = ImageFont.truetype("font.ttf", FONTSIZE)
    FONTSIZE -= 1
    font = ImageFont.truetype("font.ttf", FONTSIZE)
    w, h = draw.textsize(word, font)

    draw.text(((W-w)/2, (H-h) * HP),word, font=font,fill=FONTCOLOR)

    img.save(str(c) + 'img.png')

for c in range(0, 30):
    getimage()
    editImage(c)
