from datetime import datetime
import paho.mqtt.client as mqtt
import mysql.connector

"""
#    shellies/shellyem3-<deviceid>/emeter/<i>/energy 
		energy counter in Watt-minute (multiply by 0.017 for having kWh)
    shellies/shellyem3-<deviceid>/emeter/<i>/returned_energy 
		energy returned to the grid in Watt-minute
#    shellies/shellyem3-<deviceid>/emeter/<i>/total 
		total energy in Wh (accumulated in device's non-volatile memory)
    shellies/shellyem3-<deviceid>/emeter/<i>/total_returned 
		total energy returned to the grid in Wh (accumulated in device's non-volatile memory)
#    shellies/shellyem3-<deviceid>/emeter/<i>/power 
		instantaneous active power in Watts
#    shellies/shellyem3-<deviceid>/emeter/<i>/voltage 	
		grid voltage in Volts
#    shellies/shellyem3-<deviceid>/emeter/<i>/current 
		current in Amps
#    shellies/shellyem3-<deviceid>/emeter/<i>/pf 
		power factor (dimensionless)
    shellies/shellyem3-<deviceid>/relay/0
		reports status: on, off or overpower
"""

# con = sqlite3.connect('strom.db')
# curs = con.cursor()
# storage lists for average values
flo_time_glob = []
# temp_glob = []
# power_glob = []
# interval in seconds for writing to db
interval = 60
world = []


def my_world():
    """initialize 18 empty lists in world"""
    global world
    world.clear()
    for i in range(18):
        world.append([])
    return


# def write_db(data):
#     # zeit, watt, kwh, temp = data
#     curs.execute("""INSERT INTO shelly
#     (time, power, energy, temperature)
#     VALUES(?,?,?,?)""", data)
#     con.commit()


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
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("shellies/shellyem3-244CAB41AB64/#")
    # client.subscribe("shellies/shellyem3-244CAB41AB64/0/power",
    #                  "shellies/shellyem3-244CAB41AB64/0/total",
    #                  "shellies/shellyem3-244CAB41AB64/0/powerfactor",
    #                  "shellies/shellyem3-244CAB41AB64/0/current",
    #                  "shellies/shellyem3-244CAB41AB64/0/voltage",
    #                  "shellies/shellyem3-244CAB41AB64/0/energy",
    #                  "shellies/shellyem3-244CAB41AB64/1/power",
    #                  "shellies/shellyem3-244CAB41AB64/1/total",
    #                  "shellies/shellyem3-244CAB41AB64/1/powerfactor",
    #                  "shellies/shellyem3-244CAB41AB64/1/current",
    #                  "shellies/shellyem3-244CAB41AB64/1/voltage",
    #                  "shellies/shellyem3-244CAB41AB64/1/energy",
    #                  "shellies/shellyem3-244CAB41AB64/2/power",
    #                  "shellies/shellyem3-244CAB41AB64/2/total",
    #                  "shellies/shellyem3-244CAB41AB64/2/powerfactor",
    #                  "shellies/shellyem3-244CAB41AB64/2/current",
    #                  "shellies/shellyem3-244CAB41AB64/2/voltage",
    #                  "shellies/shellyem3-244CAB41AB64/2/energy")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global energy
    msg.payload = msg.payload.decode('utf-8')
    # flo_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    flo_time = datetime.timestamp(datetime.now())
    flo_time_glob.append(int(flo_time))
    # with open('test.txt', 'a', encoding='utf-8') as file:
    #     file.write(flo_time)
    #     file.write('\t')
    #     file.write(msg.topic)
    #     file.write('\t')
    #     file.write(msg.payload)
    #     file.write('\n')
    check_line(msg)
    check_interval()


def check_line(msg):
    global world
    tag = ['0/power', '0/total', '0/pf', '0/current', '0/voltage', '0/energy',
           '1/power', '1/total', '1/pf', '1/current', '1/voltage', '1/energy',
           '2/power', '2/total', '2/pf', '2/current', '2/voltage', '2/energy']

    for c, i in enumerate(tag):
        if msg.topic.endswith(i):
            if c == 5 or c == 11 or c == 17:
                world[c].append(round(float(msg.payload)*0.017, 3))
            else:
                world[c].append(round(float(msg.payload), 1))
            return


def check_interval():
    global flo_time_glob, world
    giveaway = []
    if (flo_time_glob[-1] - flo_time_glob[0]) >= interval:
        time = datetime.fromtimestamp(flo_time_glob[-1])
        time = time.strftime('%Y-%m-%d;%H:%M')

        # with open('shellies.txt', 'a', encoding='utf-8') as file:
        #     file.write(str(time))
        #     for i in world:
        #         print(i)
        #         value = str(round(sum(i) / len(i), 2))
        #         file.write(';' + value)
        #     file.write('\n')
        #     print()
        for i in world:

            if not i:
                value = ''
            else:
                value = round(sum(i) / len(i), 2)
            giveaway.append(value)
        write_db(giveaway)
        flo_time_glob = []
        my_world()
        return
    else:
        return


def write_db(giveaway):
    # cols = ['power', 'total', 'pf', 'current', 'voltage', 'energy']
    lines = ['phase_1', 'phase_2', 'phase_3']
    zeit = datetime.fromtimestamp(flo_time_glob[-1])
    date = zeit.strftime('%Y-%m-%d')
    time = zeit.strftime('%H:%M')
    for x in range(3):
        statement = "INSERT INTO " + lines[x] + "(date, time, power, total, pf, current, voltage, energy) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        y = x * 6
        # mist = ['a','b','c','d','e','f']
        # for a, b in enumerate(mist):
        #     b = float(str(giveaway[a+y]))
        # data = (date, time, a, b, c, d, e, f)
        a = '' if giveaway[0+y] == '' else int(giveaway[0+y])
        b = '' if giveaway[1+y] == '' else int(giveaway[1+y])
        c = '' if giveaway[2+y] == '' else float(giveaway[2+y])
        d = '' if giveaway[3+y] == '' else float(giveaway[3+y])
        e = '' if giveaway[4+y] == '' else float(giveaway[4+y])
        f = '' if giveaway[5+y] == '' else float(giveaway[5+y])
        data = (str(date), str(time), a, b, c, d, e, f)
        # data = (date, time, float(giveaway[0+y]), float(giveaway[1+y]), float(giveaway[2+y]), float(giveaway[3+y]), float(giveaway[4+y]), int(giveaway[5+y]))
        cursor.execute(statement, data)
        sql.commit()
    return


if __name__ == '__main__':
    sql = mysql.connector.connect(user='root',
                                password='',
                                host='127.0.0.1',
                                database='power')
    cursor = sql.cursor(buffered=True)
    my_world()
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
