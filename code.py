import board
import busio
import displayio
import i2cdisplaybus
import adafruit_displayio_ssd1306
import terminalio
from adafruit_display_text import label


displayio.release_displays()

i2c = busio.I2C(board.GP1, board.GP0)
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)









from os import getenv
import ipaddress
import wifi
import socketpool




ssid = getenv("WIFI_SSID")
password = getenv("WIFI_PASSWORD")

print()
print("Connecting to WiFi")

#  connect to your SSID
try:
    wifi.radio.connect(ssid, password)
except TypeError:
    print("Could not find WiFi info. Check your settings.toml file!")
    raise

print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print(f"My IP address is {wifi.radio.ipv4_address}")

#  pings Google
ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))





splash = displayio.Group()
display.root_group = splash

WIDTH = 128
HEIGHT = 32

text = str(wifi.radio.ipv4_address)
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1)
splash.append(text_area)


while True:
    pass
