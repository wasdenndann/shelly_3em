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

flo_time_glob = []
# interval in seconds for writing to db
interval = 60
world = []
zeit = datetime.timestamp(datetime.now())

def my_world():
    """initialize 6 empty lists in list"""
    global world
    world.clear()
    for i in range(6):
        world.append([])
    return


def on_connect(client, userdata, flags, rc):
    """this time only 2 values each channel needed"""
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("shellies/shellyem3-244CAB41AB64/#")
    # client.subscribe([("shellies/shellyem3-244CAB41AB64/0/power",1),
    #                  ("shellies/shellyem3-244CAB41AB64/0/total",1),
    #                  ("shellies/shellyem3-244CAB41AB64/1/power",1),
    #                  ("shellies/shellyem3-244CAB41AB64/1/total",1),
    #                  ("shellies/shellyem3-244CAB41AB64/2/power",1),
    #                  ("shellies/shellyem3-244CAB41AB64/2/total",1)])


    # The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global energy
    msg.payload = msg.payload.decode('utf-8')
    flo_time = datetime.timestamp(datetime.now())
    flo_time_glob.append(flo_time)
    check_line(msg)
    check_interval()


def check_line(msg):
    global world
    # tag = ['0/power', '0/total', '0/pf', '0/current', '0/voltage', '0/energy',
    #        '1/power', '1/total', '1/pf', '1/current', '1/voltage', '1/energy',
    #        '2/power', '2/total', '2/pf', '2/current', '2/voltage', '2/energy']
    tag = ['0/power', '0/total',
            '1/power', '1/total',
            '2/power', '2/total']
    for c, i in enumerate(tag):
        if msg.topic.endswith(i):
            world[c].append(float(msg.payload))
            return


def check_interval():
    global flo_time_glob, world, zeit
    giveaway = []
    if (flo_time_glob[-1] - zeit) >= interval:
        time = flo_time_glob[-1]
        for c, i in enumerate(world):
            if not i:
                value = ''
            elif c == 1 or c == 3 or c == 5:
                value = i[-1]
            else:
                value = sum(i) / len(i)
            giveaway.append(value)
        write_db(giveaway)
        flo_time_glob = []
        my_world()
        return
    else:
        return


def write_db(giveaway):
    global zeit
    # cols = ['L1_W', 'L2_W', 'L3_W', 'L1_sum', 'L2_sum', 'L3_sum']
    # lines = ['phase_1', 'phase_2', 'phase_3']
    # zeit1 = datetime.fromtimestamp(flo_time_glob[-1])
    # zeit1 = zeit1.strftime('%Y-%m-%d %H:%M:00')
    # zeit2 = datetime.strptime(zeit1, '%Y-%m-%d %H:%M:%S')
    # zeit = str(datetime.fromtimestamp(zeit2))
    zeit3 = datetime.strptime((datetime.fromtimestamp(flo_time_glob[-1])).strftime('%Y-%m-%d %H:%M:00'), '%Y-%m-%d %H:%M:%S')
    zeit = datetime.timestamp(zeit3)
    # zeit =str(datetime.fromtimestamp(int(flo_time_glob[-1])))
    # date = zeit.strftime('%Y-%m-%d')
    # time = zeit.strftime('%H:%M')
    statement = "INSERT INTO em3(time, L1_W, L2_W, L3_W, L1_sum, L2_sum, L3_sum) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    data = (zeit3, giveaway[0], giveaway[2], giveaway[4], giveaway[1],giveaway[3], giveaway[5])
    cursor.execute(statement, data)
    sql.commit()
    return
    # for x in range(3):
    #     statement = "INSERT INTO em3(time, L1_W, L2_W, L3_W, L1_sum, L2_sum, L3_sum) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    #     y = x * 6
    #     # mist = ['a','b','c','d','e','f']
    #     # for a, b in enumerate(mist):
    #     #     b = float(str(giveaway[a+y]))
    #     # data = (date, time, a, b, c, d, e, f)
    #     a = '' if giveaway[0+y] == '' else int(giveaway[0+y])
    #     b = '' if giveaway[1+y] == '' else int(giveaway[1+y])
    #     c = '' if giveaway[2+y] == '' else float(giveaway[2+y])
    #     d = '' if giveaway[3+y] == '' else float(giveaway[3+y])
    #     e = '' if giveaway[4+y] == '' else float(giveaway[4+y])
    #     f = '' if giveaway[5+y] == '' else float(giveaway[5+y])
    #     data = (str(date), str(time), a, b, c, d, e, f)
    #     # data = (date, time, float(giveaway[0+y]), float(giveaway[1+y]), float(giveaway[2+y]), float(giveaway[3+y]), float(giveaway[4+y]), int(giveaway[5+y]))
    #     cursor.execute(statement, data)
    #     sql.commit()
    # return


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
