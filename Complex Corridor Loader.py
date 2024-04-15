import numpy as np
import pandas as pd
import math
def segment_loader_ends(df,length,first,last,speed=44):
    # df: Final output df with time, distance, SOC, Surplus
    # length: segment length in feet
    # first: starting elevation
    # last: last MP elevation
    # speed: in ft/s, default 30 mph = 44 ft/s
    rows = int(np.ceil(length/speed))
    add = pd.DataFrame(
        np.zeros(shape=(rows, 5)), columns=["Time(sec)","Distance(feet)","Elevation(feet)","SOC","Surplus(Foot-pound)"])
    slope = (last - first) / length
    add.loc[0,"Elevation(feet)"] = first
    if len(df) == 0:
        add.loc[0,"Time(sec)"] = 1
        add.loc[0,"Distance(feet)"] = speed
        if rows==1:
            add.loc[0,"Elevation(feet)"] = last
            add.loc[0,"Time(sec)"] = df.loc[len(df)-1,"Time(sec)"] + length / speed
            add.loc[0,"Distance(feet)"] = df.loc[len(df)-1,"Distance(feet)"] + length
        else:
            for i in range(rows-1):
                add.loc[i+1,"Time(sec)"] = add.loc[i,"Time(sec)"] + 1
                add.loc[i+1,"Distance(feet)"] = add.loc[i,"Distance(feet)"] + speed
                add.loc[i+1,"Elevation(feet)"] = add.loc[i,"Elevation(feet)"] + slope * speed
            add.loc[len(add)-1,"Distance(feet)"] = length
            add.loc[len(add)-1,"Time(sec)"] = add.loc[len(add)-2,"Time(sec)"] + (add.loc[len(add)-1,"Distance(feet)"] - add.loc[len(add)-2,"Distance(feet)"])/speed
            add.loc[len(add)-1,"Elevation(feet)"] = last
    else:
        if rows == 1:
            add.loc[0,"Elevation(feet)"] = last
            add.loc[0,"Time(sec)"] = df.loc[len(df)-1,"Time(sec)"] + length / speed
            add.loc[0,"Distance(feet)"] = df.loc[len(df)-1,"Distance(feet)"] + length 
        else:
            add.loc[0,"Time(sec)"] = df.loc[len(df)-1,"Time(sec)"] + 1
            add.loc[0,"Distance(feet)"] = df.loc[len(df)-1,"Distance(feet)"] + speed
            for i in range(rows-1):
                add.loc[i+1,"Time(sec)"] = add.loc[i,"Time(sec)"] + 1
                add.loc[i+1,"Distance(feet)"] = add.loc[i,"Distance(feet)"] + speed
                add.loc[i+1,"Elevation(feet)"] = add.loc[i,"Elevation(feet)"] + slope * speed
            add.loc[len(add)-1,"Distance(feet)"] = df.loc[len(df)-1,"Distance(feet)"] + length
            add.loc[len(add)-1,"Time(sec)"] = add.loc[len(add)-2,"Time(sec)"] + (add.loc[len(add)-1,"Distance(feet)"] - add.loc[len(add)-2,"Distance(feet)"])/speed
            add.loc[len(add)-1,"Elevation(feet)"] = last
    df = pd.concat([df, add],ignore_index = True)
    if len(df) < 100:
        print(df)
    return df

def segment_loader_slope(df,length,slope,speed=44):
    # df: Final output df with time, distance, SOC, Surplus
    # length: segment length in feet
    # slope: grade in decimal format
    # speed: in ft/s, default 30 mph = 44 ft/s
    rows = int(np.ceil(length/speed))
    add = pd.DataFrame(
        np.zeros(shape=(rows, 5)), columns=["Time(sec)","Distance(feet)","SOC","Elevation(feet)","Surplus(Foot-pound)"])
    print(len(add))
    
    if len(df) == 0:
        add.loc[0,"Time(sec)"] = 1
        add.loc[0,"Distance(feet)"] = speed
        add.loc[0,"Elevation(feet)"] = speed * slope
    else:
        if len(add)==1:
            add.loc[0,"Elevation(feet)"] = last
            add.loc[0,"Time(sec)"] = df.loc[len(df)-1,"Time(sec)"] + length / speed
            add.loc[0,"Distance(feet)"] = df.loc[len(df)-1,"Distance(feet)"] + length
        else:
            add.loc[0,"Time(sec)"] = df.loc[len(df)-1,"Time(sec)"] + 1
            add.loc[0,"Distance(feet)"] = df.loc[len(df)-1,"Distance(feet)"] + speed
            add.loc[0,"Elevation(feet)"] = df.loc[len(df)-1,"Elevation(feet)"] + slope * speed
            for i in range(rows-1):
                add.loc[i+1,"Time(sec)"] = add.loc[i,"Time(sec)"] + 1
                add.loc[i+1,"Distance(feet)"] = add.loc[i,"Distance(feet)"] + speed
                add.loc[i+1,"Elevation(feet)"] = add.loc[i,"Elevation(feet)"] + slope * speed
            if len(df) == 0:
                add.loc[len(add)-1,"Distance(feet)"] = length
            else:
                add.loc[len(add)-1,"Distance(feet)"] = df.loc[len(df)-1,"Distance(feet)"] + length
            add.loc[len(add)-1,"Time(sec)"] = add.loc[len(add)-2,"Time(sec)"] + (add.loc[len(add)-1,"Distance(feet)"] - add.loc[len(add)-2,"Distance(feet)"])/speed
            add.loc[len(add)-1,"Elevation(feet)"] = add.loc[len(add)-2,"Elevation(feet)"] + slope * (add.loc[len(add)-1,"Distance(feet)"] - add.loc[len(add)-2,"Distance(feet)"])
    df = pd.concat([df, add],ignore_index = True)
    return df

# df = pd.DataFrame(
#         np.zeros(shape=(0, 5)), columns=["Time(sec)","Distance(feet)","SOC","Elevation(feet)","Surplus(Foot-pound)"])

# df = segment_loader_slope(df,52800,0.01,speed=44)
# df = segment_loader_slope(df,52800,-0.005,speed=44)
# df = segment_loader_slope(df,52800,0.015,speed=44)
# print(df)

# df = pd.DataFrame(
#         np.zeros(shape=(0, 5)), columns=["Time(sec)","Distance(feet)","SOC","Elevation(feet)","Surplus(Foot-pound)"])

# df = segment_loader_ends(df,52800,0,20,speed=44)
# df = segment_loader_ends(df,52800,20,10,speed=44)
# df = segment_loader_ends(df,52800,10,25,speed=44)
# print(df)
# print(df.loc[1199,:],df.loc[1200,:])

Savannah_data = pd.read_csv("Savannah Sub Elevations.csv")
Savannah_data = Savannah_data.reindex(index=Savannah_data.index[::-1])
Savannah_data.reset_index(drop=True, inplace=True)

print(Savannah_data)
Savannah = pd.DataFrame(
        np.zeros(shape=(0, 5)), columns=["Time(sec)","Distance(feet)","SOC","Elevation(feet)","Surplus(Foot-pound)"])
Savannah.loc[0,"Elevation(feet)"] = Savannah_data.loc[0,"Elev"]
Savannah.loc[0,"Distance(feet)"] = 0
Savannah.loc[0,"Time(sec)"] = 0
Savannah.loc[0,"Surplus(Foot-pound)"] = 0
Savannah.loc[0,"SOC"] = 0
for i in range(len(Savannah_data)-1):
    Savannah = segment_loader_ends(Savannah,-(Savannah_data.loc[i+1,"MP"]-Savannah_data.loc[i,"MP"])*5280,Savannah_data.loc[i,"Elev"],Savannah_data.loc[i+1,"Elev"],44)
# for i in range(len(Savannah_data)-1):
#     Savannah = segment_loader_ends(Savannah,(Savannah_data.loc[i+1,"MP"]-Savannah_data.loc[i,"MP"])*5280,Savannah_data.loc[i,"Elev"],Savannah_data.loc[i+1,"Elev"],44)
print(Savannah)
Savannah.to_csv("Savannah processed corridor_reverse.csv")