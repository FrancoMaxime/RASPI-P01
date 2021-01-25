#!/usr/bin/env python

import serial
import datetime
import time
import signal
import util

datetimeformat = "%Y-%m-%d_%H:%M:%S"


def timestamp_to_date(now):
    """Fonction qui transforme une date de format <timestamp POSIX> en format <datetimeformat> (declare a la ligne 4).

    Args:
        now: une date sous format <timestamp POSIX>.

    Return:
        Retourne la date sous le format <datetimeformat>.

    """
    return datetime.datetime.fromtimestamp(int(now)).strftime(datetimeformat)


def signal_handler(sig, frame):
    print("End of the meal")
    global working
    working = False


if __name__ == "__main__":
    DATE = timestamp_to_date(time.time())
    working = True
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler)
    drink = []
    meal = []
    count = []
    max_meal = 0
    min_meal = 0
    max_drink = 0
    min_drink = 0
    start_meal = []
    end_meal = []
    start_drink = []
    end_drink = []

    with open(DATE + ".txt", "w")as file:

        texte = input("entrez nom, repas et boisson \n")
        file.write(texte + '\n')
        ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        while working:
            x = ser.readline().decode('utf-8')
            file.write(x)
            print(x)
            x = x.split("\t")
            if len(x) > 4:
                if max_meal == 0 and len(meal) > 0and meal[-1] > 20:
                    max_meal = float(x[4])
                if max_drink == 0 and len(drink) > 0 and drink[-1] > 20:
                    max_drink = float(x[1])
                drink.append(float(x[1]))
                meal.append(float(x[4]))
                if len(count) == 0:
                    count.append(0)
                else:
                    count.append(count[-1] + 1)

    if not working:
        print("Plotting data")
        min_meal = meal[-1]
        min_drink = drink[-1]
        for e in meal:
            start_meal.append(max_meal)
            end_meal.append(min_meal)
            start_drink.append(max_drink)
            end_drink.append(min_drink)

        util.make_plot(count, [drink, meal, start_meal, end_meal, start_drink, end_drink], ["verre", "assiette", "debut_repas", "fin_repas", "debut verre", "fin verre"], texte, DATE+".png")


