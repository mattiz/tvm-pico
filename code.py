import time
import board
import busio
import displayio
import i2cdisplaybus
import adafruit_displayio_ssd1306
import terminalio
from adafruit_display_text import label
from os import getenv
import ipaddress
import wifi
import ssl
import socketpool
import adafruit_requests
from adafruit_datetime import datetime


url = "https://api.entur.io/journey-planner/v3/graphql"

payload = """{trip(from:{place:"NSR:StopPlace:337"}to:{place:"NSR:StopPlace:716"}numTripPatterns:1 maximumTransfers:1){tripPatterns{expectedStartTime}}}"""

ssl_cert = '''-----BEGIN CERTIFICATE-----
MIIFCzCCAvOgAwIBAgIQf/AFqRVo1jq8IoYWhKpLWjANBgkqhkiG9w0BAQsFADBH
MQswCQYDVQQGEwJVUzEiMCAGA1UEChMZR29vZ2xlIFRydXN0IFNlcnZpY2VzIExM
QzEUMBIGA1UEAxMLR1RTIFJvb3QgUjEwHhcNMjMxMjEzMDkwMDAwWhcNMjkwMjIw
MTQwMDAwWjA7MQswCQYDVQQGEwJVUzEeMBwGA1UEChMVR29vZ2xlIFRydXN0IFNl
cnZpY2VzMQwwCgYDVQQDEwNXUjMwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK
AoIBAQCPNHWHr4RyFI0HEJFvA6zx1Ag1mhnymxiJNGyYj3rU3eoF6N4bfIxUErp5
ivsYDQ18nPO9OOSoXsYzy0aJb0ag6TdjjdzM1ZdOMq17HSMFufV7SUOY0LxXx1N4
GLHtp1SyfIa+8FRFvIe6mVkd9LjbAPuBT0YrYl6xOqUqFyOsor7FjuVe/XEefaS0
I30EUrI00t+ZrIfGTFlf+OZPjnWSwrIwRpLQtg3H5Iln/z9UlCdl4wHISiyEL2Vf
za1c/aatQVvcTD8XlpF9qdg8Uyoc0ObUd+ZDSsK3+Eiiza1jtSVrlnIdgUVvhmnE
5OZ4TDHmoX+nAXMKh++HiXLM08WNAgMBAAGjgf4wgfswDgYDVR0PAQH/BAQDAgGG
MB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjASBgNVHRMBAf8ECDAGAQH/
AgEAMB0GA1UdDgQWBBTHgfX9jojZADxNY6JQMSSgziP+IzAfBgNVHSMEGDAWgBTk
rysmcRorSCeFL1JmLO/wiRNxPjA0BggrBgEFBQcBAQQoMCYwJAYIKwYBBQUHMAKG
GGh0dHA6Ly9pLnBraS5nb29nL3IxLmNydDArBgNVHR8EJDAiMCCgHqAchhpodHRw
Oi8vYy5wa2kuZ29vZy9yL3IxLmNybDATBgNVHSAEDDAKMAgGBmeBDAECATANBgkq
hkiG9w0BAQsFAAOCAgEAnI1DlJQzSKcWbyXXrJSsgKMo6KG74TMqhsuTg67a0FX0
2752+eiJb5YsOJc8DVOHalwpOvbuPdl5BuAEgIK4Va7l9j3J9M1/EjeWjGTM3Ros
zmBJGu82oz6EWi5q75xeF+onJmh2Hm98a/yJAI/mODXq5LofYcQ9AffKP9ZMZu+Y
wW+/qHqyX2JhaOntvl7i8S+l1Y8CcKEqM1NFK4s4EBYPRFjZDawOHX7fSchbSMVP
n5Nu04lrU6xufuZqRosEQw2o0UAyzDoyA52NXzJTWr1G2FVg/0A9hdrQ/6fe9G31
67zKxNqXErs6MpHttEouGbpm2ftzrmcvruYxTfxc4G2GwBi3LFLozNpy042gDfXB
zDyn1staWsy7+QnzMlR59Fz6jBOk5R4LT+ma0+KjnfRhMh5T2ucm69HkvNQtDZlV
a1tLUlzs0zLEdQSehTCjZ6SYsGt2bMVK6dvtxzcyCP0QDUFnNXCwgw12+mGSkAuj
4ORi8kMRpnL8UEjkNbdw9KL1eYbEC3D0GPue2Yk2AGhxkmcdm1BoOp05kYw/Nnqg
h7QV8DKyBTUHbjH0pXlLiOsSOY+CLh1eTM+Do6rSjqGnDQeUXylZmPCmuveaw38I
VnBaa6Eiz6pngZ1u6OeO/1UzfhmyTm0n0G+9JZ3KS2Mq08isNgXHLnhlHJaphpE=
-----END CERTIFICATE-----'''


#
# Configure display
#
def configure_display():
    displayio.release_displays()

    i2c = busio.I2C(board.GP1, board.GP0)
    display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3c)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
    return display


#
# Connect to WiFi
#
def connect_wifi():
    ssid = getenv("WIFI_SSID")
    password = getenv("WIFI_PASSWORD")

    print()
    print("Connecting to WiFi")

    try:
        wifi.radio.connect(ssid, password)
    except TypeError:
        print("Could not find WiFi info. Check your settings.toml file!")
        raise

    print("Connected to WiFi")

    pool = socketpool.SocketPool(wifi.radio)
    return pool


#
# Print information about WiFi connection
#
def debug_wifi():
    print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
    print(f"My IP address is {wifi.radio.ipv4_address}")

    ipv4 = ipaddress.ip_address("8.8.4.4")
    print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))


#
# Update display with text
#
def update_display(display, text):
    print("Updating display")
    splash = displayio.Group()
    display.root_group = splash

    WIDTH = 128
    HEIGHT = 32

    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, scale=3, x=20, y=HEIGHT // 2 - 1)
    splash.append(text_area)


#
# Fetch expected start time from API
#
def fetch_expected_start_time(url, payload, requests):
    print("Fetching text from %s" % url)
    response = requests.post(url, data=payload, headers={"Content-Type": "application/graphql"})
    print("Getting json response")
    json_resp = response.json()

    print("Parsing json response")
    expected_start_time = json_resp["data"]["trip"]["tripPatterns"][0]["expectedStartTime"]

    print("Parsing datetime")
    dt_object = datetime.fromisoformat(expected_start_time)
    time_formatted = f"{dt_object.hour}:{dt_object.minute}"
    print(f"Time: {time_formatted}")
    return time_formatted



display = configure_display()

pool = connect_wifi()

debug_wifi()


ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(cadata=ssl_cert)


requests = adafruit_requests.Session(pool, ssl_context)



while True:
    start_time = fetch_expected_start_time(url, payload, requests)

    update_display(display, start_time)

    time.sleep(60)
