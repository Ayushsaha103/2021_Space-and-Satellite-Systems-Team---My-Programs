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

################################## INPUT METHOD: USER INPUTS THE NUMS ##################################

# Inputting user input float values
sensor_labels = ["px1", "px2", "px3", "px4", "nx1", "nx2", "nx3", "nx4", "py1", "py2", "py3", "py4", "ny1",
                 "ny2", "ny3", "ny4", "pz1", "pz2", "pz3", "pz4", "nz1", "nz2", "nz3", "nz4"]
# from t = 1 (on data sheet):
input_floats = [0,0,0,0,0.788675135,0.788675135,0.788675135,0.211324865,0,0,0,0,0.211324865,0.211324865,
                0.788675135,0.788675135,0,0,0,0,0.211324865,0.788675135,0.788675135,0.211324865]

# from t = 42 (on data sheet):
#input_floats = [0,0,0,0,0.459107227,0.86466078,0.459107227,0.540217938,0,0,0,0,0.524307875,-0.124577809,
#                0.037643612,0.686529296,0.259242194,0.015910062,0.583685036,0.827017168,0,0,0,0]
# from t = 684 (on data sheet):
#input_floats = [0,0,0,0,0,0,0,0,-0.059915261,0.387298335,0.83451193,0.387298335,0,0,0,0,0,0,0,0,
#                0.998203467,0.774596669,0.550989871,0.774596669]

# These below 2 commented lines can be used to directly input the floats from user (separated by commas)
    # input_str = input("Enter values separated by commas: ")
    # input_floats = [float(idx) for idx in input_str.split(',')]


# Choosing 3 random valid indexes from the input_floats list
#Choosing first index
for i in range(0,100):
    random_idx_1 = randrange(0, 24)
    value1 = input_floats[random_idx_1]
    if value1 != 0:
        sensor_label_1 = sensor_labels[random_idx_1]
        break
# getting the coefficients for the first equation
vect_eq1_coefs = coef_finder(random_idx_1)

# Choosing second index
for i in range(0,100):
  random_idx_2 = randrange(0, 24)
  value2 = input_floats[random_idx_2]
  if value2 != 0 and random_idx_2 != random_idx_1:
      sensor_label_2 = sensor_labels[random_idx_2]
      break
# getting the coefficients for the second equation
vect_eq2_coefs = coef_finder(random_idx_2)

# choosing third valid index
for i in range(0,100):
    random_idx_3 = randrange(0, 24)
    value3 = input_floats[random_idx_3]
    
    # make sure it's not zero or the same as any other index
    if value3 == 0 or random_idx_3 == random_idx_2 or random_idx_3 == random_idx_1:
        continue

    # check to make sure the equations won't all have the x, y, or z coefficients being 0
    vect_eq3_coefs = coef_finder(random_idx_3)
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


# These print statements print the chosen nums
print(sensor_label_1 + ": ")
print(value1)
print(sensor_label_2 + ": ")
print(value2)
print(sensor_label_3 + ": ")
print(value3)
print("---------------------------")


########################################### THE COMPUTATIONS ###########################################

x, y, z = symbols('x y z')
eq1 = Eq(vect_eq1_coefs[0] * x + vect_eq1_coefs[1] * y + vect_eq1_coefs[2] * z, input_floats[random_idx_1])
eq2 = Eq(vect_eq2_coefs[0] * x + vect_eq2_coefs[1] * y + vect_eq2_coefs[2] * z, input_floats[random_idx_2])
eq3 = Eq(vect_eq3_coefs[0] * x + vect_eq3_coefs[1] * y + vect_eq3_coefs[2] * z, input_floats[random_idx_3])

sol = solve((eq1, eq2, eq3),(x, y, z))
print(f'The solution is x = {sol[x]}, y = {sol[y]}, z = {sol[z]}')

