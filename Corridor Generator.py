# load packages
import numpy as np
import pandas as pd
import math
print(int(np.ceil((61)/20)))

output = pd.DataFrame(
        np.zeros(shape=(1, 3)), columns=["Distance(feet)","Grade","Elevation(feet)"])
def sector_loader(df,start,grade,end):
    if start%20 == 0:
        steps = int(np.ceil((end - start)/20))
    else:
        steps = int(np.ceil((end - start)/20)+1)
    df2 = pd.DataFrame(
        np.zeros(shape=(steps, 3)), columns=["Distance(feet)","Grade","Elevation(feet)"])
    df2.loc[0,"Distance(feet)"] = start
    df2.loc[0,"Grade"] = grade
    df2.loc[0,"Elevation(feet)"] = df.loc[len(df)-1,"Elevation(feet)"]
    next = 20 * np.floor((start + 20)/20)
    while next < end:
        index = int(np.ceil((next - start)/20))
        df2.loc[index,"Distance(feet)"] = next
        df2.loc[index,"Grade"] = grade
        df2.loc[index,"Elevation(feet)"] = (df2.loc[index,"Distance(feet)"] - df2.loc[index-1,"Distance(feet)"]) * grade + df2.loc[index-1,"Elevation(feet)"]
        next += 20
    index = steps
    df2.loc[index,"Distance(feet)"] = end
    df2.loc[index,"Grade"] = grade
    df2.loc[index,"Elevation(feet)"] = (df2.loc[index,"Distance(feet)"] - df2.loc[index-1,"Distance(feet)"]) * grade + df2.loc[index-1,"Elevation(feet)"]
    # df = df.append(df2, ignore_index = True)
    df = pd.concat([df, df2], ignore_index=True)
    return df

output = sector_loader(output,0,0.02,510)
output = sector_loader(output,510,-0.01,810)
print(output)