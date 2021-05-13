import asyncio
from telethon import TelegramClient,events, sync
from telethon.tl import functions, types
import re
import csv
from dateutil import tz
import pandas as pd
from datetime import datetime
import json


filename="vaccine_slot_trends.csv"
df = pd.read_csv(filename)
df.drop_duplicates(subset=None, inplace=True)
print("Existing : ",len(df))
f = open(filename,"a")
writer = csv.writer(f)

with open('config.json') as cf:
    data = json.load(cf)
    api_id = data["api_id"]
    api_hash = data["api_hash"]

mindate=datetime(2021, 5, 1, 0, 0,0)
maxdate=datetime.now()
    
def match(pattern,text):
    result = pattern.findall(text)
    return result[0] if len(result)>0 else None

def match_pincode(text,ch):
    pincode=None
    if(ch == 'blrvaccinealerts'):
        pattern = re.compile("\[([0-9]*)\]")
        pincode = match(pattern,text)
    elif(ch == 'blrvaccine'):
        pattern = re.compile("📫 ([0-9]*)  \#⃣")
        pincode = match(pattern,text)
    elif(ch=='BLRVaccineQuickAlert'):
        pattern = re.compile("\*\*Pincode: ([0-9]*)\*\*")
        pincode = match(pattern,text)
    elif(ch=='BloreVaccine'):
        pattern = re.compile("\*\*([0-9]+)\*\*")
        pincode = match(pattern,text)
    return pincode
    
def match_name(text,ch):
    name = None
    if(ch == 'blrvaccinealerts'):
        pattern = re.compile("Name: \*\*(.*)\*\*",flags=re.IGNORECASE)
        name = match(pattern,text)
    elif(ch == 'blrvaccine' and len(text.split("\n"))>1):
        name = text.split("\n")[1]
    elif(ch=='BLRVaccineQuickAlert'):
        pattern = re.compile("\*\*Name: (.*)\*\*")
        name = match(pattern,text)
    elif(ch=='BloreVaccine'):
        line=text.split("\n")[0]
        pattern = re.compile("(.*)\*\*.*\*\*")
        name = match(pattern,line)
    return name

def match_slots(text,ch):
    slots = None
    if(ch == 'blrvaccinealerts'):
        pattern = re.compile(": (.+) slots",flags=re.IGNORECASE)
        slots = match(pattern,text)
    elif(ch == 'blrvaccine'):
        pattern = re.compile("#⃣(.+) Slots",flags=re.IGNORECASE)
        slots = match(pattern,text)
    elif(ch=='BLRVaccineQuickAlert'):
        pattern = re.compile(": (.+) slots\*\*")
        slots = match(pattern,text)
    elif(ch=='BloreVaccine'):
        pattern = re.compile("\*\*Available Slots: ([0-9]+)\*\*")
        slots = match(pattern,text)
    return slots


client = TelegramClient('session', api_id, api_hash)
client.start()

channels = ['blrvaccine', 'blrvaccinealerts','BLRVaccineQuickAlert','BloreVaccine']
async def main():
    for ch in channels:
        channel = await client.get_entity(ch)
        async for x in client.iter_messages(channel):
            if(x.text):
                #print(x.text)
                pincode = match_pincode(x.text,ch)
                name = match_name(x.text,ch)
                local_datetime = x.date.astimezone(tz.tzlocal())
                slots = match_slots(x.text,ch)
                #print(pincode,name,slots)
                row=[str(pincode),local_datetime.month,local_datetime.day,local_datetime.hour,local_datetime.minute,name,slots]
                if(pincode!=None and name!=None and str(pincode).startswith("560")):
                    writer.writerow(row)
    

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
f.close()

df = pd.read_csv(filename)
df.drop_duplicates(subset=None, inplace=True)
df.to_csv(filename, index=False)
print("New : ",len(df))