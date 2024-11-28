import network
import time
from umqtt.simple import MQTTClient

# WiFi og MQTT stillingar
ssid = "TskoliVESM"
password = "Fallegurhestur"
mqtt_server = "10.201.48.67"
mqtt_topic = "act"

# Tengjast WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Connected to WiFi:', wlan.ifconfig())

# MQTT Callback til að vinna með skilaboð
def mqtt_callback(topic, msg):
    print("Received message on topic", topic.decode(), ":", msg.decode())
    try:
        # Athuga hvort skilaboðin séu `true` eða `false`
        if msg.decode() == "true":
            print("Switch is ON!")
        elif msg.decode() == "false":
            print("Switch is OFF!")
        else:
            print("Unexpected message format:", msg.decode())
    except Exception as e:
        # Handlanga allar aðrar villur
        print("Error handling message:", msg.decode(), "| Error:", str(e))

# Tengjast MQTT Broker
def connect_mqtt():
    client = MQTTClient("ESP32Client_Hillary", mqtt_server)
    client.set_callback(mqtt_callback)

    retry_count = 0
    while retry_count < 5:
        try:
            print("Connecting to MQTT broker...")
            client.connect()
            print("Connected to MQTT broker")
            client.subscribe(mqtt_topic)
            return client
        except OSError as e:
            print(f"MQTT connection failed, retrying... Error: {e}")
            retry_count += 1
            time.sleep(5)

    print("Failed to connect to MQTT broker after multiple attempts.")
    return None

# Helsta keyrsla
def main():
    connect_wifi()
    client = connect_mqtt()
    
    if client is None:
        print("Exiting program due to MQTT connection failure.")
        return

    while True:
        client.check_msg()  # Athugar hvort skilaboð hafa borist
        time.sleep(1)

if __name__ == '__main__':
    main()
