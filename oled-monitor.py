import time
import psutil
import socket
from Adafruit_SSD1306 import SSD1306_128_64
from PIL import Image, ImageDraw, ImageFont

# 初始化 OLED
disp = SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
font = ImageFont.load_default()

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "N/A"

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = int(f.read()) / 1000
        return temp
    except:
        return 0

def draw_bar(draw, x, y, w, h, percent, color=255):
    fill_w = int(w * percent / 100)
    draw.rectangle([x, y, x+w, y+h], outline=255, fill=0)
    draw.rectangle([x, y, x+fill_w, y+h], outline=255, fill=color)

def update_oled():
    ip = get_ip()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    ram_percent = psutil.virtual_memory().percent
    swap_percent = psutil.swap_memory().percent
    cpu_temp = get_cpu_temp()

    # CPU TEMP 閃爍
    temp_color = 255
    if cpu_temp >= 80:
        temp_color = 255 if int(time.time()*2) % 2 == 0 else 0

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    # IP
    draw.rectangle((0, 0, width, 12), outline=255, fill=255)
    draw.text((0, 0), f"IP: {ip}", font=font, fill=0)

    bar_width = width // 3

    # CPU
    draw.text((0, 16), f"CPU {cpu_percent:.0f}%", font=font, fill=255)
    draw_bar(draw, 0, 28, bar_width, 6, cpu_percent)

    # TEMP
    right_x = width // 2
    draw.text((right_x, 16), f"TEMP {cpu_temp:.0f}°C", font=font, fill=255)
    draw_bar(draw, right_x, 28, bar_width, 6, min(cpu_temp,80)/80*100, color=temp_color)

    # RAM
    draw.text((0, 36), f"RAM {ram_percent:.0f}%", font=font, fill=255)
    draw_bar(draw, 0, 48, bar_width, 6, ram_percent)

    # SWAP
    draw.text((right_x, 36), f"SWAP {swap_percent:.0f}%", font=font, fill=255)
    draw_bar(draw, right_x, 48, bar_width, 6, swap_percent)

    disp.image(image)
    disp.display()

while True:
    update_oled()
    time.sleep(0.5)
