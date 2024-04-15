# load packages
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
#110 ton cars
#empty 33 ton/car
#loaded 143 ton/car
#number of cars as variable
# Corridor Loader
filename = "Savannah processed corridor.csv"
filename_rev = "Savannah processed corridor_reverse.csv"
#Loaded weight need to be assumed
Route_length = 100 #miles
Mile_to_feet = 5280
Train_Mass = 3500 #tons Empty Train
Rolling_resistance = 5 #lbs/ton
Empty_car_weight = 33 #tons/car
Loaded_car_weight = 143 #tons/car
Number_of_cars = 10 #cars
Locomotive_weight = 196 #tons #reference:https://www.wabteccorp.com/locomotive/alternative-fuel-locomotives/FLXdrive
ton_to_lbs = 2000
Slope = 0.005
Battery_capacity = 4.8 #MWH
Battery_efficiency = 1
kg_to_lbs = 2.204
MWh_to_footlb = 2.655 * (10 ** 9)
Speed = 30 #mph

def sindeg(deg):
    return np.sin(deg*np.pi/180)

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

def SOC_updater(Num_Loco, SOC, E_n, surplus,capacity,efficiency=Battery_efficiency):
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

#Uphill Initialization
#Uphill one-second energy consumption = 2.64E6+1.584E7 = 1.848E7 ft*lb
#Energy Storage at SOC=1 1.274E13 ft*lb per BEL



Number_of_cars = 15
print(Number_of_cars)
X_n = X_0 = 0 #feet
Z_n = Z_0 = 15.5 #feet
SOC = 1
Slope = 0.01
Num_BEL = 1
surplus = 0 # foot-pound
t_total = int(Route_length/Speed*3600) #second
Train_Mass = Locomotive_weight * Num_BEL + Number_of_cars * Empty_car_weight
Loaded_weight = Locomotive_weight * Num_BEL + Number_of_cars * Loaded_car_weight
print(Train_Mass)
Corridor_data = pd.read_csv(filename)
X_n = Corridor_data.loc[0,"Distance(feet)"]
Z_n = Corridor_data.loc[0,"Elevation(feet)"]
Corridor_data.loc[0,"SOC"] = 1
#Simulation Sequence
datalength = len(Corridor_data)
for t in range(1,datalength):
    X_t = Corridor_data.loc[t,"Distance(feet)"]
    Z_t = Corridor_data.loc[t,"Elevation(feet)"]
    dX = X_t - X_n
    dZ = Z_t - Z_n
    Z_n = Z_t
    X_n = X_t
    SOC = Corridor_data.loc[t-1,"SOC"]
    E_n = energy_needed(Train_Mass, Rolling_resistance, dX, dZ)
    # if (E_n > 0) and (E_n/dX > (Num_BEL * Locomotive_weight * ton_to_lbs * 0.35)) and (dX > 10):
    #     print("Not Enough Adhesion Force")
    #     break
    # if (E_n < 0) and (-E_n/dX > 100000) and (dX > 10):
    #     E_n = -100000*dX
    SOC, update, surplus = SOC_updater(Num_BEL,SOC,E_n,surplus,Battery_capacity)
    if SOC <= 0:
        SOC = 0
    Corridor_data.loc[t,"SOC"] = SOC
    Corridor_data.loc[t,"Surplus(Foot-pound)"] = surplus
Corridor_data.loc[datalength,"Time(sec)"] = "Number of Cars"
Corridor_data.loc[datalength,"Distance(feet)"] = Number_of_cars
Corridor_data.loc[datalength,"Time(sec)"] = "Empty Train Mass"
Corridor_data.loc[datalength,"Time(sec)"] = Train_Mass

print(Corridor_data)
Corridor_rev_data = pd.read_csv(filename_rev)
Corridor_rev_data.loc[0,"SOC"] = Corridor_data.loc[int(len(Corridor_data)-2),"SOC"]
datalength = len(Corridor_rev_data)
X_n = Corridor_rev_data.loc[0,"Distance(feet)"]
Z_n = Corridor_rev_data.loc[0,"Elevation(feet)"]
for t in range(1,datalength):
    X_t = Corridor_rev_data.loc[t,"Distance(feet)"]
    Z_t = Corridor_rev_data.loc[t,"Elevation(feet)"]
    dX = X_t - X_n
    dZ = Z_t - Z_n
    Z_n = Z_t
    X_n = X_t
    SOC = Corridor_rev_data.loc[t-1,"SOC"]
    E_n = energy_needed(Loaded_weight, Rolling_resistance, dX, dZ)
    # if (E_n > 0) and (E_n/dX > (Num_BEL * Locomotive_weight * ton_to_lbs * 0.35)) and (dX > 10):
    #     print("Not Enough Adhesion Force")
    #     break
    # if (E_n < 0) and (-E_n/dX > 100000) and (dX > 10):
    #     E_n = -100000*dX
    SOC, update, surplus = SOC_updater(Num_BEL,SOC,E_n,surplus,Battery_capacity)
    if SOC <= 0:
        SOC = 0
    Corridor_rev_data.loc[t,"SOC"] = SOC
    Corridor_rev_data.loc[t,"Surplus(Foot-pound)"] = surplus
    

Corridor_data.to_csv("Savannah Uphill Simulation.csv")
Corridor_rev_data.to_csv("Savannah Downhill Simulation.csv")
print(Corridor_data)
print(Corridor_rev_data)
