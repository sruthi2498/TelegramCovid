# TelegramCovid

### A util to pull chats from telegram channels and parse the messages. This is to ultimately figure out when different hospitals open their vaccination slots.

## To preview data :

1. Download the hospital_timeslots.txt file

It contains data in format : (pincode) (Hospital name) : hour:min, hour:min, .... 

Where each timeslot (hour:min) was when a vaccine slot was opened

The list is sorted from maximum slots to minimum.


## To setup and run :

1.     pip install -r requirements.txt 

2. Get your Telegram api_id and api_hash from https://my.telegram.org

3.  Create config.json file 

       `{"api_id":"YOUR_API_ID", "api_hash":"YOUR_API_HASH"}`
     
     
3. Run `pull_data.py` 
 
   It will generate output csv file `vaccine_slot_trends.csv`
   
4. Run `process_result.py`

   It will generate hospital timeslots file `hospital_timeslots.txt`
   
   
