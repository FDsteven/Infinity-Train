import numpy as np
import pandas as pd
import random as rd
# TO find the critical grade for each car weight combination
# No Charging station available along the route

Locomotive_weight = 196 #tons #reference:https://www.wabteccorp.com/locomotive/alternative-fuel-locomotives/FLXdrive
Route_length = 100 #miles
Empty_car_weight = 31.5 #tons/car
Loaded_car_weight = 131.5 #tons/car
Rolling_resistance = 5 #lbs/ton
Number_of_cars = 20 #cars
Battery_capacity = 4.8 #MWH
Battery_efficiency = 0.8
kg_to_lbs = 2.204
ton_to_lbs = 2000
MWh_to_footlb = 2.655 * (10 ** 9)
Speed = 30 #mph

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

List_of_trials = pd.DataFrame(
            np.zeros(shape=(0, 6)), columns=["Number of Cars","Empty Weight","Loaded Weight","Downhill Surplus(Foot-pound)", "Uphill SOC", "Grade"])
# trial range can be changed
for trial in range(50):
    # Change Empty_car_weight and Loaded_car_weight for different setups here
    Empty_car_weight = 33 #tons/car
    Loaded_car_weight = 143 #tons/car
    # This would need a good guess on what the feasible region might be
    # Plus and minus sign for upper limit and lower limit
    Number_of_cars = 20
    X_n = X_0 = 0 #feet
    Z_n = Z_0 = 0 #feet
    SOC = 1
    Num_BEL = 1
    # Change Slope, and Battery Capacity here
    Slope = 0.01 - trial * 0.0005
    Battery_capacity = 14.5 #MWH
    
    surplus = 0 # foot-pound
    t_total = int(Route_length/Speed*3600) #second
    Train_Mass = Locomotive_weight * Num_BEL + Number_of_cars * Empty_car_weight
    print(Slope)
    Output_up = pd.DataFrame(
            np.zeros(shape=(t_total+1, 4)), columns=["Time(sec)","Distance(feet)","SOC","Surplus(Foot-pound)"])
    if Train_Mass * 2000 * Slope + Train_Mass * Rolling_resistance > 137200:
        Output_down_storage.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH " + str(Slope) +" 100 MIle " + str(Loaded_car_weight) + "-ton-car Downhill Critical Profile.csv")
        Output_up_storage.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH " + str(Slope) +" 100 MIle " + str(Loaded_car_weight) + "-ton-car Uphill Critical Profile.csv")
        List_of_trials.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH " + str(Slope) +" 100 MIle " + str(Loaded_car_weight) + "-ton-car List of Trials.csv")
        print("Not enough traction force")
        break
    #Simulation Sequence
    for t in range(t_total):
        X_t, Z_t = X_n_Z_n_updater(t,Speed,Slope)
        dX = X_t - X_n
        dZ = Z_t - Z_n
        Z_n = Z_t
        X_n = X_t
        E_n = energy_needed(Train_Mass, Rolling_resistance, dX, dZ)
        SOC, update, surplus = SOC_updater(Num_BEL,SOC,E_n,surplus,Battery_capacity)
        if SOC <= 0:
            SOC = 0
        Output_up.loc[t,"Time(sec)"] = t
        Output_up.loc[t,"Distance(feet)"] = X_n
        Output_up.loc[t,"SOC"] = SOC
        Output_up.loc[t,"Surplus(Foot-pound)"] = surplus
    Output_up.loc[t_total,"Time(sec)"] = "Number of Cars"
    Output_up.loc[t_total,"Distance(feet)"] = Number_of_cars
    Output_up.loc[t_total,"SOC"] = "Uphill Slope"
    Output_up.loc[t_total,"Surplus(Foot-pound)"] = Slope
    ["Number of Cars","Empty Weight","Loaded Weight","Downhill Surplus(Foot-pound)", "Uphill SOC", "Grade"]
    List_of_trials.loc[trial,"Grade"] = Slope
    List_of_trials.loc[trial,"Number of Cars"] = Number_of_cars
    List_of_trials.loc[trial,"Empty Weight"] = Train_Mass
    List_of_trials.loc[trial,"Uphill SOC"] = Output_up.loc[t_total-1,"SOC"]
    # print(Output_up)
    if Output_up.loc[t_total-2,"SOC"] == 0:
        Output_down_storage.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH " + str(Slope) +" 100 MIle " + str(Loaded_car_weight) + "-ton-car Downhill Critical Profile.csv")
        Output_up_storage.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH " + str(Slope) +" 100 MIle " + str(Loaded_car_weight) + "-ton-car Uphill Critical Profile.csv")
        List_of_trials.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH " + str(Slope) +" 100 MIle " + str(Loaded_car_weight) + "-ton-car List of Trials.csv")
        print("Battery depleted")
        break
    else:
        Output_up_storage = Output_up.copy()
    
    #Downhill Initialization
    X_n = X_0 = 0 #feet
    Z_n = Z_0 = 0 #feet
    SOC = Output_up.loc[len(Output_up)-2,"SOC"]
    Slope_down = -Slope
    surplus = 0 # foot-pound
    t_total = int(Route_length/Speed*3600) #second
    Train_Mass = Locomotive_weight * Num_BEL + Number_of_cars * Loaded_car_weight
    print(Slope_down)
    Output_down = pd.DataFrame(
            np.zeros(shape=(t_total+1, 4)), columns=["Time(sec)","Distance(feet)","SOC","Surplus(Foot-pound)"])
    if Train_Mass * 2000 * Slope - Train_Mass * Rolling_resistance > 100000 * Num_BEL:
        Output_down_storage.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH " + str(Slope) +" 100 MIle " + str(Loaded_car_weight) + "-ton-car Downhill Critical Profile.csv")
        Output_up_storage.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH " + str(Slope) +" 100 MIle " + str(Loaded_car_weight) + "-ton-car Uphill Critical Profile.csv")
        List_of_trials.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH " + str(Slope) +" 100 MIle " + str(Loaded_car_weight) + "-ton-car List of Trials.csv")
        print("Unable to brake")
        break
    #Simulation Sequence
    for t in range(t_total):
        X_t, Z_t = X_n_Z_n_updater(t,Speed,Slope_down)
        dX = X_t - X_n
        dZ = Z_t - Z_n
        Z_n = Z_t
        X_n = X_t
        E_n = energy_needed(Train_Mass, Rolling_resistance, dX, dZ)
        SOC, update, surplus = SOC_updater(Num_BEL,SOC,E_n,surplus,Battery_capacity)
        Output_down.loc[t,"Time(sec)"] = t
        Output_down.loc[t,"Distance(feet)"] = X_n
        Output_down.loc[t,"SOC"] = SOC
        Output_down.loc[t,"Surplus(Foot-pound)"] = surplus
    Output_down.loc[t_total,"Time(sec)"] = "Number of Cars"
    Output_down.loc[t_total,"Distance(feet)"] = Number_of_cars
    Output_down.loc[t_total,"SOC"] = "Downhill Slope"
    Output_down.loc[t_total,"Surplus(Foot-pound)"] = Slope_down
    List_of_trials.loc[trial,"Downhill Surplus(Foot-pound)"] = Output_down.loc[t_total-1,"Surplus(Foot-pound)"]
    List_of_trials.loc[trial,"Loaded Weight"] = Train_Mass
    # print(Output_down.loc[t_total-1,"SOC"])
    if Output_down.loc[t_total-2,"SOC"] != 1:
        Output_down_storage.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH " + str(Slope) +" 100 MIle " + str(Loaded_car_weight) + "-ton-car Downhill Critical Profile.csv")
        Output_up_storage.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH "+ str(Slope) + " 100 MIle " + str(Loaded_car_weight) + "-ton-car Uphill Critical Profile.csv")
        List_of_trials.to_csv(str(Num_BEL)+" BEL " + str(Battery_capacity) + " MWH "+ str(Slope)+ " 100 MIle " + str(Loaded_car_weight) + "-ton-car List of Trials.csv")
        print("Battery not charged")
        break
    else:
        Output_down_storage = Output_down.copy()
print(Output_up_storage)
print(Output_down_storage)