# load packages
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
#110 ton cars
#empty 33 ton/car
#loaded 143 ton/car
#number of cars as variable

#Loaded weight need to be assumed
Route_length = 100 #miles
Mile_to_feet = 5280
Train_Mass = 3500 #tons Empty Train
Rolling_resistance = 5 #lbs/ton
Empty_car_weight = 33 #tons/car
Loaded_car_weight = 143 #tons/car
Number_of_cars = 20 #cars
Locomotive_weight = 196 #tons #reference:https://www.wabteccorp.com/locomotive/alternative-fuel-locomotives/FLXdrive
ton_to_lbs = 2000
Slope = 0.005
Battery_capacity = 4.8 #MWH
Battery_efficiency = 0.8
kg_to_lbs = 2.204
MWh_to_footlb = 2.655 * (10 ** 9)
Speed = 30 #mph

def sindeg(deg):
    return np.sin(deg*np.pi/180)

def X_n_Z_n_updater(t,V,G):
    #t in second, v in mph, G in percentage
    V = V/3600*5280 # in feet/sec
    x = V * t
    z = V * t * G
    return x, z

def energy_needed(W, R, dX, dZ, a=1, b=ton_to_lbs):
    
    W = Train_Mass
    R = Rolling_resistance
    a = 1
    b = ton_to_lbs
    E_n = a * dX * R * W + b * W * dZ
    #Units: E_n: in distance*force format foot-pound
    #dX = feet
    #R = default 5 lbs/ton
    #W = tons
    # b: 2000 lbs/ton
    # dZ: feet
    
    #OR from textbook's tractive resistance formula, from a power(V,G,W)*D perspective
    
    return E_n

def SOC_updater(Num_Loco, SOC, E_n, surplus,efficiency=Battery_efficiency,capacity=Battery_capacity):
    current = Num_Loco * capacity * SOC * MWh_to_footlb #transform to foot-pound
    if E_n > 0:
        update = current - E_n
        SOC = update/capacity/MWh_to_footlb/Num_Loco
    else:
        update = current - E_n * efficiency
        SOC = update/capacity/MWh_to_footlb/Num_Loco
        if SOC >= 1:
            surplus += (SOC-1) * Num_Loco * capacity * MWh_to_footlb
            SOC = 1
    return SOC, update, surplus

#Downhill Initialization
#Uphill one-second energy gain = -7.7E5+7.7E6 = 6.93E6 ft*lb
#Energy Storage at SOC=1 1.274E13 ft*lb per BEL

X_n = X_0 = 0 #feet
Z_n = Z_0 = 0 #feet
SOC = 1
Slope = -0.01
Num_BEL = 1
surplus = 0 # foot-pound
t_total = int(Route_length/Speed*3600) #second
Train_Mass = Locomotive_weight * Num_BEL + Number_of_cars * Loaded_car_weight
print(Train_Mass)
Output = pd.DataFrame(
        np.zeros(shape=(t_total+1, 4)), columns=["Time(sec)","Distance(feet)","SOC","Surplus(Foot-pound)"])

#Simulation Sequence
for t in range(t_total):
    X_t, Z_t = X_n_Z_n_updater(t,Speed,Slope)
    dX = X_t - X_n
    dZ = Z_t - Z_n
    Z_n = Z_t
    X_n = X_t
    E_n = energy_needed(Train_Mass, Rolling_resistance, dX, dZ)
    SOC, update, surplus = SOC_updater(Num_BEL,SOC,E_n,surplus)
    Output.loc[t,"Time(sec)"] = t
    Output.loc[t,"Distance(feet)"] = X_n
    Output.loc[t,"SOC"] = SOC
    Output.loc[t,"Surplus(Foot-pound)"] = surplus

print(Output)