import requests
import datetime
import pandas as pd
now = datetime.date.today()

df = pd.DataFrame(columns=['date',
    'center_id', 'name', 'state_name', 'district_name', 'block_name',
    'pincode', 'lat', 'long', 'fee_type', 'session_id', 
    'available_capacity', 'min_age_limit', 'vaccine'
])

states = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states")

for state in states.json()['states']:
    
    stateUrl = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/' + str(
        state['state_id'])
    
    districts = requests.get(stateUrl)

    for district in districts.json()['districts']:
        districtUrl = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' + str(
            district['district_id']) + "&date=" + str(now.strftime("%d-%m-%Y"))

        vaccineByDistrict = requests.get(districtUrl)

        for center in vaccineByDistrict.json()['centers']:

            for sessions in center['sessions']:
                if(sessions['min_age_limit'] != 45):
                    if(sessions['available_capacity']>0):
                        df_1 = pd.DataFrame(sessions)
                        df_1['center_id'] = center['center_id']
                        df_1['name'] = center['name']
                        df_1['state_name'] = center['state_name']
                        df_1['district_name'] = center['district_name']
                        df_1['block_name'] = center['block_name']
                        df_1['pincode'] = center['pincode']
                        df_1['lat'] = center['lat']
                        df_1['long'] = center['long']
                        df_1['fee_type'] = center['fee_type']
                        #print(df)
                        df = df.append(df_1.drop(columns = ['slots']).drop_duplicates())

df['snap_dt'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        
df.to_csv('./Desktop/Covid.csv')