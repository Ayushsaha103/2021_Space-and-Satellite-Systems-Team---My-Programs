
# Satellite Guidance, Navigation, and Control Systems Simulation Software
# This software simulates a changing sun position vector
# Outliers are thrown in and detected by algorithm, accuracy > 95%
# Program-crash-detection-and-response algorithm equipped

# To stop the program from purposefully throwing in and detecting outliers, comment out the entire
# 'if' statement at line 165 ("if randrange(0, 5) == 1"), AND set max_degree_value at line 97 really high

# Sun position vector function is modifiable (w/ respect to t)
    # NOTE: If you want to modify this, you have to make it include both positive and neg. z values
    # You also must be careful and test any changes
# Decceleration and acceleration rate is included and modifiable
# Angular momentum is included and modifiable
# Discrete time stamps are modifiable
# Duration interval of constant velocity (before decceleration begins) is modifiable
# speed of program running is modifiable (via time_change_rate)

# program is currently set so that usual deg. change per time interval (0.1 sec)
# is about 0.5-5 degs


from itertools import takewhile
from numpy.core.fromnumeric import take
import schedule
import time
from time import time, sleep
import numpy as np
import math
from random import randrange



def magnitude(my_vector):
    val_holder = my_vector ** 2
    mag_val = math.sqrt(np.sum(val_holder))
    #print(my_vector)
    #print(mag_val)
    return mag_val

def unitize(my_vector):
    #my_vector = my_vector / magnitude(my_vector)
    return my_vector

# Setting the variables
sun_vector = np.array([0.0,0.0,0.0])
outlier_vector = np.array([2.5, -32, -0.5])
    #outlier_vector = unitize(outlier_vector)
sun_vect_val_holder = np.array([0.0,0.0,0.0])
original_sun_vector = np.zeros(3)
increase_vals = True
counter = 0

# last_6_deg_change_vals is an array that holds the values of the last 6 degree values
# note that the degree change values are taken per, like, 0.2 sec or something
degree_change_value = 0     #the value of the degree change from the last sun vector to the current one
#last_6_deg_change_vals = np.zeros(6)


# NEW VARIABLES FOR IMPROVED SIMULATION
t = 0.0
t_orig = 0.0
max_pt_reached = False
min_pt_reached = False
crash_upcoming = True
crash_counter = 0
fixation_const_for_crash_counter = 4

# YOU MAY EDIT THE BELOW VARIABLE DECLARATIONS
# Important notes:
# sun vector equation is <0.2*cos(6t), 0.2*sin(6t), t>
# t IS NOT TIME. The value (counter/0.1) is time
# t is set to increase by val (for each run of the while loop)
# The value of t changes discretely, a set number times per sec

time_change_rate = 0.1                 # You may adjust me! (the big while loop runs once per time_change_rate * (1sec))

                                    #val is basically rotational momentum constant
val = 0.01                           # You may adjust me! (just make sure to adjust all 3 of em)
main_val_value_positive = 0.01
main_val_value_negative = -0.01

                            # the t upper and lower bounds mark where (at what t value) the decceleration and acceleration start/end
t_upper_bound = 0.74         # You may adjust me! (just make sure it's a multiple of positive val value)
t_lower_bound = -0.74       # You may adjust me! (just make sure it's a multiple of negative val value)

decc_const_pos = 0.7632                   # You may adjust me to whatever! (decc = decceleration)
acc_const_pos = 1/ decc_const_pos
decc_const_neg = -0.7632                  # You may adjust me to whatever (as long as I'm negative)!
acc_const_neg = 1/ decc_const_neg

decc_peak_const = math.pow(decc_const_pos, 6) * main_val_value_positive     # you can adjust the number in here (it controls the
                                                                            # program's perceived turn around point from
                                                                            # decceleration to acceleration, lower integers
                                                                            # will be more sudden)

max_degree_change_value = 15            # if satellite spins more than 15 deg., we'll consider that an outlier
                                        # this is used for algorithm's low-pass filter


# THE BIG WHILE LOOP
while True:
    # control the rate of this program's operation by modifying the two identical
    # numbers (0.03) in the code line below
    sleep(time_change_rate - time() % time_change_rate)

    # iterations counter
    counter = counter +1

    # sun vector value transfer
    original_sun_vector[0] = sun_vector[0]
    original_sun_vector[1] = sun_vector[1]
    original_sun_vector[2] = sun_vector[2]

    # t value transfer
    t_orig = t

    #entire t-changing algorithm (decceleration and acceleration considered)
    if t > t_lower_bound and t < t_upper_bound:
        if increase_vals:
            val = main_val_value_positive
        else:
            val = main_val_value_negative
    else:
        # t is positive and increasing
        if increase_vals== True and t>0:
            val=decc_const_pos*math.fabs(val)
        # t is positive and decreasing
        elif increase_vals== False and t>0:
            val = acc_const_neg*math.fabs(val)
            if max_pt_reached == True:
                val = decc_const_neg*math.fabs(val)
        # t is negative and decreasing
        elif increase_vals== False and t<0:
            val = decc_const_neg*math.fabs(val)
        # t is negative and increasing
        elif increase_vals ==True and t<0:
            val = acc_const_pos*math.fabs(val)
            if min_pt_reached == True:
                val = decc_const_pos*math.fabs(val)
    #change t
    t+=val

    #switch direction of t movement
    max_pt_reached = False
    min_pt_reached = False

    if t < t_lower_bound or t > t_upper_bound:
        # if decceleration has become slow, satellite can switch to turning other direction
        if increase_vals == True and t>0 and t-t_orig < decc_peak_const: #as alternative to (degree_change_value<0.05), you may use (t-t_orig < decc_peak_const)
            increase_vals = False
            max_pt_reached = True
        # if t reached the negative lower bound
        elif increase_vals == False and t<0 and t_orig-t < decc_peak_const: #as alternative to (degree_change_value<0.05), you may use (t-t_orig < decc_peak_const)
            increase_vals = True
            min_pt_reached = True

    # YOU MAY ADJUST THE SUN VECTOR FUNCTION HERE (be careful and test any changes)
    # only requirement is to make sure the function z value goes from negative t val to positive one
    sun_vector[0] = 0.2*math.cos(6*t)
    sun_vector[1] = 0.2*math.sin(6*t)
    sun_vector[2] = t

    #purposefully distort sun vector values (only for minority of cases), [feel free to comment this portion out]
    if randrange(0, 5) == 1:
        ##save values (this functionality is not needed anymore)
        #sun_vect_val_holder[0] = sun_vector[0]
        #sun_vect_val_holder[1] = sun_vector[1]
        #sun_vect_val_holder[2] = sun_vector[2]
        
        #distort values
        f = randrange(-30,30)
        g = randrange(-30,30)
        h = randrange(-30,30)
        sun_vector[0] = f #you may replace f with outlier_vector[0]
        sun_vector[1] = g #you may replace g with outlier_vector[1]
        sun_vector[2] = h #you may replace h with outlier_vector[2]
        outlier_vector = np.array([f,g,h])


    #print sun vector on first iteration
    if counter ==1:
        if np.array_equal(sun_vector, outlier_vector, equal_nan=True):
            print(str(counter) + ": " + str(sun_vector) + "             supposedly ignored")
        else:
            print(str(counter) + ": " + str(sun_vector))

    # calculating degree change
    if counter >= 2:
        
        num = np.dot(sun_vector, original_sun_vector)
        num = num / (magnitude(sun_vector) * magnitude(original_sun_vector))
        
        if num >= 1:            # this is for math.acos() domain error avoidance
            num = 0.999999
        if num <=-1:
            num = -0.999999

        degree_change_value = math.acos(num)
        degree_change_value = math.degrees(degree_change_value)
        
        # printing sun vector and degree change from last sun vector to current one
        if np.array_equal(sun_vector, outlier_vector, equal_nan=True):
            print(str(counter) + ": " + str(sun_vector) + "             supposedly ignored")
            #print(str(counter) + ": " + str(degree_change_value) + "            supposedly ignored")
        else:
            print(str(counter) + ": " + str(sun_vector))
            #print(str(counter) + ": " + str(degree_change_value))

        #reset crash_counter
        if crash_upcoming == True and degree_change_value < 15:
            crash_upcoming = False
            crash_counter = 0

        #print statement to show if program detects outlier vectors (current vector is messed up)
        #set sun vector to the previous one so that upcoming computations don't get ruined
        if degree_change_value > max_degree_change_value:
            crash_counter = crash_counter+1
            crash_upcoming = True
            if crash_counter == fixation_const_for_crash_counter:
                crash_upcoming = False
                crash_counter=0
                #set current sun vector as the new one to calculate degree change off of
                original_sun_vector[0] = sun_vector[0]
                original_sun_vector[1] = sun_vector[1]
                original_sun_vector[2] = sun_vector[2]

            print("detection algorithm predicts this^ vector should be ignored")
            #set sun vector to original
            sun_vector[0] = original_sun_vector[0]
            sun_vector[1] = original_sun_vector[1]
            sun_vector[2] = original_sun_vector[2]
            #print("orig: " + str(sun_vector))


        #-----------------------------------------

        ## storing last 6 degree change values in array (if user decides to use temporary
        ## median for outlier detection los-pass filter instead of the set max_degree_change_value as filter)
        #if counter <= 7:
        #    last_6_deg_change_vals[counter-2] = degree_change_value
        #if counter > 7:
        #    last_6_deg_change_vals = np.roll(last_6_deg_change_vals, -1)
        #    last_6_deg_change_vals[5] = degree_change_value
        
        # #print(last_6_deg_change_vals)

        #-----------------------------------------

    ## NOT NEEDED ANYMORE:
    ## restoring the purposefully messed up vector values (which occur only
    ## like in 15% of cases) to what they should be
    #if np.array_equal(sun_vector, outlier_vector, equal_nan=True):
    #    sun_vector[0] = sun_vect_val_holder[0]
    #    sun_vector[1] = sun_vect_val_holder[1]
    #    sun_vector[2] = sun_vect_val_holder[2]

