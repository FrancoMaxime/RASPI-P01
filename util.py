#!/usr/bin/env python

import matplotlib.pyplot as plt


def clean_data(data, facteur=5):
    """Fonction qui permet de lisser des tableau de donnees en enlevant les pics de bruit.

    Args:
        data: les donnees a nettoyer.
        facteur: le facteur de correction, naturel strictement superieur a 1.

    Return:
        Retourne un nouveau tableau contenant les donnees data nettoyees selon le facteur.

    """

    previous_data = []
    new_data = []
    dirty_data = []
    count = []
    is_previous_data = False
    c = 0
    for c_data in data:
        dirty_data.append(c_data)
        if len(new_data) > 0 and not is_previous_data:
            if abs(new_data[-1] - c_data) < 1:
                new_data.append(new_data[-1])
                count.append(count[-1] + 1)
            else:
                is_previous_data = True
                previous_data.append(c_data)

        elif is_previous_data:
            previous_data.append(c_data)
            if abs(new_data[-1] - c_data) < 1:
                for i in previous_data:
                    new_data.append(new_data[-1])
                    count.append(count[-1] + 1)
                previous_data = []
                is_previous_data = False

            elif len(previous_data) > facteur -1:
                is_previous_data = False
                result = []
                for i in range(facteur):
                    result.append(0)

                for i1 in range(len(previous_data)):
                    for i2 in range(i1,len(previous_data)):
                        if abs(previous_data[i1] - previous_data[i2]) < 1:
                            result[i1] += 1
                            result[i2] += 1

                m = max(result)
                new_value = new_data[-1]
                if m > 0:
                    new_value = previous_data[result.index(m)]

                for i in range(0, facteur):
                    new_data.append(new_value)
                    count.append(count[-1] + 1)
                previous_data = []

        elif len(new_data) == 0:
            if c_data < 1:
                new_data.append(0)
            else:
                new_data.append(c_data)
            count.append(0)

        c += 1

    return new_data


def make_report(drink, meal):
    count = []
    data1 = []
    data2 = []
    c = 0

    # variable debut de repas
    start_drink = 0
    start_meal = 0
    is_drink = False
    c_drink = 0
    is_meal = False
    c_meal = 0

    # variable pour les gorgées
    nb_sips = 0
    is_drinking = True
    previous_drink = 0
    value_drink = []
    drink_before = 0
    count_drink = 0

    # variable pour les bouchées
    nb_bites = 0
    previous_meal = 0
    is_biting = False
    meal_before = 0
    value_meal = []

    for i in range(len(drink)):
        count.append(c)
        current_drink = drink[i]
        current_meal = meal[i]

        # repère le poid initial du verre et de l'assiette
        if not is_drink and current_drink > 25.:
            is_drink = True
            start_drink = current_drink
            previous_drink = start_drink
            c_drink = 2
        if not is_meal and current_meal > 25.:
            is_meal = True
            start_meal = current_meal
            c_meal = 2

        if is_drink and c_drink == 0:
            start_drink = current_drink
        if is_meal and c_meal == 0:
            start_meal = current_meal
        c_drink -= 1
        c_meal -= 1

        # repère quand l'utilisateur lève le verre
        if not is_drinking and current_drink < 25:
            drink_before = data1[-2]
            nb_sips += 1
            is_drinking = True

        # repère quand l'utilisateur pose le verre
        if is_drinking and current_drink > 25:
            is_drinking = False
            count_drink = 2

        # calcul la différence de poid après une gorgée
        if count_drink == 1:
            if nb_sips > 0:
                value_drink.append(drink_before - current_drink)

        # repère quand l'utilisateur utilise sa fourchette ou son couteau
        if len(data2) > 3 and current_meal < data2[-1]:
            is_biting = True
            nb_bites += 1
            meal_before = data2[-1]

        if is_biting and current_meal < meal_before and 1 < (meal_before - current_meal) and current_meal < (
                start_meal - 5):
            is_biting = False
            value_meal.append(meal_before - current_meal)

        data1.append(current_drink)
        data2.append(current_meal)
        count_drink -= 1
        c += 1

    print(sum(value_meal))
    report = "Start drink : {0} \nStart meal : {1} \nNumber of sips : {2}\nSips's weight : {3}\nNumber of bites : " \
             "{9}\nBite's weight : {8}\nEnd drink : {4}\nEnd meal : {5}\nDelta drink : {6}\nDelta meal : {7}".format(
             start_drink, start_meal, nb_sips, value_drink, data1[-1], data2[-1], start_drink - data1[-1],
             start_meal - data2[-1], value_meal, nb_bites)

    return report


def make_plot(time, data, name, plotname, namefile):
    plt.figure(figsize=(20, 10))
    for e in range(len(data)):
        plt.plot(time, data[e], linewidth=0.50, label=name[e])
    plt.xlabel('time')
    plt.ylabel('poid')
    plt.title(plotname)
    plt.legend()
    plt.savefig(namefile)
