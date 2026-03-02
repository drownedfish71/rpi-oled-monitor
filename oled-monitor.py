import time
import psutil
import socket
from Adafruit_SSD1306 import SSD1306_128_64
from PIL import Image, ImageDraw, ImageFont

# Initialize OLED display
disp = SSD1306_128_64(rst=None)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
font = ImageFont.load_default()

def get_ip():
    """Get local IP address by connecting to Google DNS"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "N/A"

def get_cpu_temp():
    """Read CPU temperature from system file"""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = int(f.read()) / 1000
        return temp
    except:
        return 0

def draw_bar(draw, x, y, w, h, percent, color=255):
    """Draw a progress bar with given percentage"""
    fill_w = int(w * percent / 100)
    draw.rectangle([x, y, x+w, y+h], outline=255, fill=0)
    draw.rectangle([x, y, x+fill_w, y+h], outline=255, fill=color)

def update_oled():
    """Update OLED display with system information"""
    ip = get_ip()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    ram_percent = psutil.virtual_memory().percent
    swap_percent = psutil.swap_memory().percent
    cpu_temp = get_cpu_temp()

    # Blink CPU temperature when over 80°C
    temp_color = 255
    if cpu_temp >= 80:
        temp_color = 255 if int(time.time()*2) % 2 == 0 else 0

    # Create new image
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    # Display IP address
    draw.rectangle((0, 0, width, 12), outline=255, fill=255)
    draw.text((0, 0), f"IP: {ip}", font=font, fill=0)

    bar_width = width // 3

    # Top left - CPU usage
    draw.text((0, 16), f"CPU {cpu_percent:.0f}%", font=font, fill=255)
    draw_bar(draw, 0, 28, bar_width, 6, cpu_percent)

    # Top right - CPU temperature
    right_x = width // 2
    draw.text((right_x, 16), f"TEMP {cpu_temp:.0f}°C", font=font, fill=255)
    draw_bar(draw, right_x, 28, bar_width, 6, min(cpu_temp,80)/80*100, color=temp_color)

    # Bottom left - RAM usage
    draw.text((0, 36), f"RAM {ram_percent:.0f}%", font=font, fill=255)
    draw_bar(draw, 0, 48, bar_width, 6, ram_percent)

    # Bottom right - Swap usage
    draw.text((right_x, 36), f"SWAP {swap_percent:.0f}%", font=font, fill=255)
    draw_bar(draw, right_x, 48, bar_width, 6, swap_percent)

    # Update display
    disp.image(image)
    disp.display()

# Main loop - update every 0.5 seconds
while True:
    update_oled()
    time.sleep(0.5)