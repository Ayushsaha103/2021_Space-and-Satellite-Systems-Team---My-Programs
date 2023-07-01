
# This program continuously generates a low-pass filter for incoming sun vectors
# Simulated real-world sun vector values are termed sun_vector[0], sun_vector[1], and sun_vector[2]
# (AKA, the x, y, and z coordinates)
# The filtered sun vector values are generated as filtered_sun_vector[0], ", "

# The data are printed to a csv file. First column is the counter (time index)
# Next 3 columns are the original sun vector values
# Last 3 columns are the filtered sun vector values


from itertools import takewhile
from numpy.core.fromnumeric import take
import schedule
import time
from time import time, sleep
import numpy as np
import math
import random
from random import randrange
import csv
from decimal import Decimal


# FUNCTIONS
def filter(sun_vector, orig_sun_vector, filtered_sun_vector):
    filtered_sun_vector[0] = (sun_vector[0] + orig_sun_vector[0]) / 2
    filtered_sun_vector[1] = (sun_vector[1] + orig_sun_vector[1]) / 2
    filtered_sun_vector[2] = (sun_vector[2] + orig_sun_vector[2]) / 2

    return filtered_sun_vector


# VARIABLE DECLARATIONS
time_change_rate = 0.1      # You may adjust me! (the big while loop runs once per time_change_rate * (1sec))
sun_vector = np.array([1.2,1.12,1.42])
orig_sun_vector = np.array([1.2,1.12,1.42])
#last_2_sun_vectos = np.array([1.0,1.0,1.0,1.0,1.0,1.0])
filtered_sun_vector = np.array([1.2,1.32,1.84])
random_direction_change = 0
counter = 0
data_holder = np.array([])

# Write the data file headers to csv file
with open('sun_vector_LP_filter.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['counter(*0.1sec)', 'sun_vector_x', 'sun_vector_y', 'sun_vector_z', 'filtered_sun_vector_x', 'filtered_sun_vector_y', 'filtered_sun_vector_z'])
print('sun_vector\t\t\t\t\tfiltered_sun_vector')


# THE BIG WHILE LOOP
while True:
    sleep(time_change_rate - time() % time_change_rate)

    orig_sun_vector[0] = sun_vector[0]
    orig_sun_vector[1] = sun_vector[1]
    orig_sun_vector[2] = sun_vector[2]

    #--------------------SUN VECTOR SIMULATION--------------------
    # Randomly generating x
    random_direction_change = randrange(0, 2)
    if random_direction_change == 1:
        random_value_change = random.uniform(0.0, 1.01)     # you may adjust these parameters (used for random data generation)
    elif random_direction_change == 0:
        random_value_change = random.uniform(0.0, -1.10)    # you may adjust these parameters (used for random data generation)

    #print(random_direction_change)
    #print(random_value_change)
    sun_vector[0] = sun_vector[0] + random_value_change


    #Randomly generating y
    random_direction_change = randrange(0, 2)
    if random_direction_change == 1:
        random_value_change = random.uniform(0.0, 1.01)     # you may adjust these parameters (used for random data generation)
    elif random_direction_change == 0:
        random_value_change = random.uniform(0.0, -1.10)    # you may adjust these parameters (used for random data generation)
    sun_vector[1] = sun_vector[1] + random_value_change

    #Randomly generating z
    random_direction_change = randrange(0, 2)
    if random_direction_change == 1:
        random_value_change = random.uniform(0.0, 1.01)     # you may adjust these parameters (used for random data generation)
    elif random_direction_change == 0:
        random_value_change = random.uniform(0.0, -1.10)    # you may adjust these parameters (used for random data generation)
    sun_vector[2] = sun_vector[2] + random_value_change

    

    #generating the filtered fun vector
    if counter > 0:
        filtered_sun_vector = filter(sun_vector, orig_sun_vector, filtered_sun_vector)
    elif counter == 0:
        filtered_sun_vector[0] = sun_vector[0]
        filtered_sun_vector[1] = sun_vector[1]
        filtered_sun_vector[2] = sun_vector[2]
    
    #round all values
    sun_vector[0] = round(sun_vector[0], 6)
    sun_vector[1] = round(sun_vector[1], 6)
    sun_vector[2] = round(sun_vector[2], 6)
    filtered_sun_vector[0] = round(filtered_sun_vector[0], 6)
    filtered_sun_vector[1] = round(filtered_sun_vector[1], 6)
    filtered_sun_vector[2] = round(filtered_sun_vector[2], 6)

    # Output data to console
    print(str(sun_vector) + '\t\t' + str(filtered_sun_vector))

    # save data to csv file
    if counter % 30 != 0:
        data_holder = np.append(data_holder,np.array([counter,sun_vector[0],sun_vector[1],sun_vector[2],filtered_sun_vector[0],filtered_sun_vector[1],filtered_sun_vector[2]]))
    else:
        np.savetxt('sun_vector_LP_filter.csv', np.split(data_holder, 30), delimiter=',', fmt='%f')
        data_holder = np.array([])
        data_holder = np.append(data_holder,np.array([counter,sun_vector[0],sun_vector[1],sun_vector[2],filtered_sun_vector[0],filtered_sun_vector[1],filtered_sun_vector[2]]))


    # iterations counter
    counter = counter +1
