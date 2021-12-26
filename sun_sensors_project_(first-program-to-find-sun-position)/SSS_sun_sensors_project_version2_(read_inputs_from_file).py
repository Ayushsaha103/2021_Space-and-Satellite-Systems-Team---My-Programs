from sympy import symbols, Eq, solve
import csv
import random
from random import randrange


############################### VECTOR EQUATION COEFFICIENT FINDER FUNCTION ###############################

# Function to find the coefficients for the 3 vector dot product equations used to find the final solution
def coef_finder(sensor_label): 
    coef_array = [0, 0, 0]
    
    if sensor_label == 0:
        coef_array = [0.866025403844386, 0, 0.5]
        return coef_array
    elif sensor_label == 1:
        coef_array = [0.866025403844386, 0.5, 0]
        return coef_array
    elif sensor_label == 2:
        coef_array = [0.866025403844386, 0, -0.5]
        return coef_array
    elif sensor_label == 3:
        coef_array = [0.866025403844386, -0.5, 0]
        return coef_array
    elif sensor_label == 4:
        coef_array = [-0.866025403844386, 0, 0.5]
        return coef_array
    elif sensor_label == 5:
        coef_array = [-0.866025403844386, -0.5, 0]
        return coef_array
    elif sensor_label == 6:
        coef_array = [-0.866025403844386, 0, -0.5]
        return coef_array
    elif sensor_label == 7:    
        coef_array = [-0.866025403844386, 0.5, 0]
        return coef_array
    elif sensor_label == 8:
        coef_array = [0, 0.866025403844386, 0.5]
        return coef_array
    elif sensor_label == 9:
        coef_array = [-0.5, 0.866025403844386, 0]
        return coef_array
    elif sensor_label == 10:
        coef_array = [0, 0.866025403844386, -0.5]
        return coef_array
    elif sensor_label == 11:
        coef_array = [0.5, 0.866025403844386, 0]
        return coef_array
    elif sensor_label == 12:
        coef_array = [0, -0.866025403844386, 0.5]
        return coef_array
    elif sensor_label == 13:
        coef_array = [0.5, -0.866025403844386, 0]
        return coef_array
    elif sensor_label == 14:
        coef_array = [0, -0.866025403844386, -0.5]
        return coef_array
    elif sensor_label == 15:
        coef_array = [-0.5, -0.866025403844386, 0]
        return coef_array
    elif sensor_label == 16:
        coef_array = [0, 0.5, 0.866025403844386]
        return coef_array
    elif sensor_label == 17:
        coef_array = [0.5, 0, 0.866025403844386]
        return coef_array
    elif sensor_label == 18:
        coef_array = [0, -0.5, 0.866025403844386]
        return coef_array
    elif sensor_label == 19:
        coef_array = [-0.5, 0, 0.866025403844386]
        return coef_array
    elif sensor_label == 20:
        coef_array = [0, 0.5, -0.866025403844386]
        return coef_array
    elif sensor_label == 21:
        coef_array = [-0.5, 0, -0.866025403844386]
        return coef_array
    elif sensor_label == 22:
        coef_array = [0, -0.5, -0.866025403844386]
        return coef_array
    elif sensor_label == 23:
        coef_array = [0.5, 0, -0.866025403844386]
        return coef_array
    
    return coef_array

################################## INPUT METHOD: READING NUMS FROM CSV FILE ##################################

# Opening the csv data file (note that this is Ayush's modified version of it)
with open('sun_sensor_model_data_as_csv.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='|')

    value1 = 0
    value2 = 0
    value3 = 0
    sensor_labels = ["px1", "px2", "px3", "px4", "nx1", "nx2", "nx3", "nx4", "py1", "py2", "py3", "py4", "ny1",
                    "ny2", "ny3", "ny4", "pz1", "pz2", "pz3", "pz4", "nz1", "nz2", "nz3", "nz4"]

    # Looping thru the csv file rows until reaching the first row (only one run of the for loop)
    t = 0
    for row in spamreader:
        t += 1

        # YOU CAN MODIFY THE BELOW LINE TO MAKE IT ONLY READ A CERTAIN ROW OF THE DATA SET
        if t != 1:
            continue

        # Choosing 3 random valid indexes from the input_floats list
        for i in range(0,100):
            random_idx_1 = randrange(0, 24)
            sensor_label_1 = sensor_labels[random_idx_1]
            value1 = float(row[sensor_label_1])
            if value1 != 0:
                break
        # getting the coefficients for the first equation
        vect_eq1_coefs = coef_finder(random_idx_1)

        # choosing second valid index
        for i in range(0,100):
            random_idx_2 = randrange(0, 24)
            sensor_label_2 = sensor_labels[random_idx_2]
            value2 = float(row[sensor_label_2])
            if value2 != 0 and random_idx_2 != random_idx_1:
                break
        # getting the coefficients for the second equation
        vect_eq2_coefs = coef_finder(random_idx_2)

        # choosing third valid index
        for i in range(0,100):
            random_idx_3 = randrange(0, 24)
            sensor_label_3 = sensor_labels[random_idx_3]
            vect_eq3_coefs = coef_finder(random_idx_3)
            value3 = float(row[sensor_label_3])
            
            # Validating third randomly chosen index:
            # make sure it's not zero or the same as any other index
            if value3 == 0 or random_idx_3 == random_idx_2 or random_idx_3 == random_idx_1:
                continue

            ## make sure the angle value isn't the same among all chosen values
            #if value3 == value2 and value3 == value1:
            #    continue
            
            # check to make sure the equations won't all have the x, y, or z coefficients being 0
            all_coefs_are_same = False
            for i in range(3):
                if vect_eq3_coefs[i] == vect_eq2_coefs[i] and vect_eq3_coefs[i] == vect_eq1_coefs[i] and vect_eq3_coefs[i] == 0:
                    all_coefs_are_same = True
                    break
            if all_coefs_are_same == True:
                continue
            
            # finally, we can break from the big loop
            sensor_label_3 = sensor_labels[random_idx_3]
            break
        
    # These print statements show how I'm accessing the chosen nums
    print("Chosen sensor readings: ")
    print(sensor_label_1 + ': ')
    print(value1)
    print(sensor_label_2 + ': ')
    print(value2)
    print(sensor_label_3 + ': ')
    print(value3)
    print("---------------------------")

    print("Vector coefficients (for equation to use): ")
    print(vect_eq1_coefs)
    print(vect_eq2_coefs)
    print(vect_eq3_coefs)
    print("---------------------------")

    # solving the vector equations
    x, y, z = symbols('x y z')
    eq1 = Eq((vect_eq1_coefs[0] * x) + (vect_eq1_coefs[1] * y) + (vect_eq1_coefs[2] * z), value1)
    eq2 = Eq((vect_eq2_coefs[0] * x) + (vect_eq2_coefs[1] * y) + (vect_eq2_coefs[2] * z), value2)
    eq3 = Eq((vect_eq3_coefs[0] * x) + (vect_eq3_coefs[1] * y) + (vect_eq3_coefs[2] * z), value3)

    sol = solve((eq1, eq2, eq3),(x, y, z))
    print(f'The solution is x = {sol[x]}, y = {sol[y]}, z = {sol[z]}')


csvfile.close()