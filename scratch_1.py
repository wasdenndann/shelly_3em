# import tkinter as tk
from sqlite3 import OperationalError
# from tkinter import ttk
# from tkinter import messagebox
# from functools import partial
from datetime import datetime
import paho.mqtt.client as mqtt
import sqlite3

con = sqlite3.connect('strom.db')
curs = con.cursor()
# storage lists for average values
flo_time_glob = []
temp_glob = []
power_glob = []
# interval in seconds for writing to db
interval = 120


def create_db():
    statement = """
            CREATE TABLE IF NOT EXISTS shelly (
            id INTEGER PRIMARY KEY,
            time DATE,
            power FLOAT(4),
            energy FLOAT(6),
            temperature FLOAT(4));
            """
    curs.execute(statement)


def write_db(data):
    # zeit, watt, kwh, temp = data
    curs.execute("""INSERT INTO shelly
    (time, power, energy, temperature)
    VALUES(?,?,?,?)""", data)
    con.commit()


def write_csv(data):
    zeit, watt, kwh, temp = data
    with open('strom.csv', 'a', encoding='utf-8') as komma:
        komma.write(str(zeit) + ',')
        komma.write(str(watt) + ',')
        komma.write(str(kwh) + ',')
        komma.write(str(temp))
        komma.write('\n')


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("shellies/shellyplug-s-C129F0/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global energy
    msg.payload = msg.payload.decode('utf-8')

    print(msg.topic + '--' + msg.payload)

    # if msg.topic.endswith('/temperature'):
    #     temp_glob.append((round(float(msg.payload), 1)))
    # elif msg.topic.endswith('power'):
    #     power_glob.append((round(float(msg.payload), 1)))
    # elif msg.topic.endswith('energy'):
    #     energy = (round(int(msg.payload) * 0.017 / 1000, 4))
    # else:
    #     return
    # flo_time = datetime.timestamp(datetime.now())
    # flo_time_glob.append(int(flo_time))
    # check_interval()


def check_interval():
    global flo_time_glob, energy, power_glob, temp_glob
    if (flo_time_glob[-1] - flo_time_glob[0]) >= interval:
        time = str(datetime.fromtimestamp(flo_time_glob[-1]))
        power = round((sum(power_glob) / len(power_glob)), 1)
        energy = energy
        temperature = round((sum(temp_glob) / len(temp_glob)), 1)
        with open('shellies.txt', 'a', encoding='utf-8') as file:
            file.write(time + ' - ' + str(len(temp_glob)) + str(temp_glob) + str(temperature) + '\n')
            file.write('\t' * 4 + str(len(power_glob)) + str(power_glob) + str(power))
            file.write('\n' * 2)
        data = time, power, energy, temperature
        write_db(data)
        write_csv(data)
        power_glob = []
        flo_time_glob = []
        temp_glob = []
        return
    else:
        return


def test():
    create_db()
    data = ('2022', 100, 1, 38)
    write_db(data)


if __name__ == '__main__':
    create_db()

    client = mqtt.Client(clean_session=True)
    # Client(client_id="", clean_session=True)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.178.132", 1883, 20)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
    # test()