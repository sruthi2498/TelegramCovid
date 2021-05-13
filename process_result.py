import re
import csv
import pandas as pd
from fuzzywuzzy import fuzz


filename="vaccine_slot_trends.csv"
df = pd.read_csv(filename)
df.drop_duplicates(subset=None, inplace=True)
df = df.sort_values("pincode").reset_index()
print("Existing : ",len(df))

out_file = "hospital_timeslots.txt"
f=open(out_file,"w")

hospitals = df.name.unique().tolist()
hospitals =[ h for h in hospitals if h!=None and h!="" and type(h)==str]
hospitals = sorted(hospitals)
for i in range(len(hospitals)):
    h = hospitals[i]
    for j in range(i+1,len(hospitals)):
        if(h!=hospitals[j]):
            match = fuzz.token_sort_ratio(h,hospitals[j])
            if(match>75):
                #print(h,hospitals[j],match )
                df['name'] = df['name'].replace([hospitals[j]],h)
                hospitals[j] = h


hospitals = sorted(list(set(hospitals)))
print(hospitals)

for hp in hospitals:
    if(hp!=None and hp!=""):
        df_hosp = df[df["name"]==hp].sort_values("slots",ascending=False).reset_index()
        if(len(df_hosp)>0):
            
            hour_mins=[]
            for i in range(len(df_hosp)):
                row = str(df_hosp.loc[i,"hour"])+":"+str(df_hosp.loc[i,"minute"])
                if(row not in hour_mins):
                    hour_mins.append(row)
            line = str(df_hosp.loc[0,"pincode"])+" "+ hp +" : "+ ",".join(hour_mins)+"\n"
            f.write(line)

f.close()