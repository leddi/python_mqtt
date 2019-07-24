# git clone https://github.com/iwanbk/nyamuk.git
# __init__.py

from nyamuk.nyamuk import *

MQTT_SERVER = 127.0.0.1
MQTT_USER   = username
MQTT_PASS   = password
TOPIC       = /topic/topic

def nloop(mqtt_client):
    mqtt_client.packet_write()
    mqtt_client.loop()
    return mqtt_client.pop_event()

def broker_connect_send(topic, message):
    ret = mqtt_client.connect(version=3)
    ret = nloop(mqtt_client)
    if not isinstance(ret, EventConnack) or ret.ret_code != 0:
        print('keine Verbindung zum Server...')
    else:
        mqtt_client.publish(topic, message, qos=0)
    mqtt_client.disconnect()
    
mqtt_client= Nyamuk(CLIENT, server=MQTT_SERVER,username=MQTT_USER, password=MQTT_PASS)
ret = mqtt_client.connect(version=3)
ret = nloop(mqtt_client)
if not isinstance(ret, EventConnack) or ret.ret_code !=0:
    print('Verbindung fehlgeschlagen')
    sys.exit(1)

mqtt_client.subscribe(TOPIC, qos=1)
ret = nloop(mqtt_client)

if not isinstance(ret, EventSuback):
    print('SUBACK nicht empfangen')
    sys.exit(2)
print('QoS is ', ret.granted_qos[0])

try:
    while True:
        evt = nloop(mqtt_client)
        if isinstance(evt, EventPublish):
            print('Msg empfangen: {0} (topic= {1})'.format(evt.msg.payload, evt.msg.topic))
            influxdb_send('benzin',float(evt.msg.payload))
            if evt.msg.qos == 1:
                mqtt_client.puback(evt.msg.mid)
except KeyboardInterrupt:
    print('KeyBoard...')
    pass

mqtt_client.disconnect()
