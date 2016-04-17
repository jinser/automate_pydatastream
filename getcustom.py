from pydatastream import Datastream

import json
import datetime
import sys
import os.path

#hardcoded directories
dir_input = "input/"
dir_output = "output/"

#check that the login credentials and input file location are being passed in
numOfArgs = len(sys.argv) - 1
if numOfArgs != 3:
		print "Please run this python script with username,password and input file location in that order respectively."
		exit()

#Setup login credentials and input file location
username = str(sys.argv[1])
pw = str(sys.argv[2])
input_file_loc = dir_input + str(sys.argv[3])

#Ensure that the input file location exists
if ( not os.path.isfile(str(input_file_loc)) ):
	print "The file " + str(input_file_loc) + " does not exist."
	exit()

#login credentials to datastream
DWE = Datastream(username=username,password=pw)
#other info from datastream
info = DWE.system_info()
subscribed_sources = DWE.sources()

#replace missing data with NaNs
DWE.raise_on_error = False

#get all codes, groups, start dates from input file 
with open(input_file_loc,'r') as input_file:
    symbol_ref = json.load(input_file)

#download timestamp
download_date = {'Custom_Download_Date' : datetime.datetime.now().isoformat()}

#calculate time taken for entire process
time_taken = datetime.datetime.now()
time_taken = time_taken - time_taken
		
for desc,desc_value in symbol_ref.iteritems():
	for group,group_value in desc_value.iteritems():	
		#create list for custom fields 
		custom_fields = list()
		for code_key,code_value in group_value.iteritems():
		
			for key,value in code_value.iteritems():
				if(key == 'code'):
					search_code = value
					search_symbol = {'Custom_Ticker' : value}
				if(key == 'start_date'):
					start_date = value
				if(key == 'custom_field'):
					custom_fields[:] = []
					custom_fields.append(value)

			startTime = datetime.datetime.now()	
			#send request to retrieve the data from Datastream
			req = DWE.fetch(str(search_code),custom_fields,date_from=str(start_date),only_data=False)
			
			time_taken = time_taken + datetime.datetime.now() - startTime
							
			#format date and convert to json 
			raw_json = req[0].to_json(date_format='iso')
			raw_metadata = req[1].to_json()
			
			#Data cleaning and processing
			#remove the time component including the '.' char from the key values of datetime in the data
			raw_json = raw_json.replace("T00:00:00.000Z","")
			#replace the metadata's keys from "0" to "default_ws_key"
			raw_metadata = raw_metadata.replace("\"0\"","\"Custom_WS_Key\"")
			
			#combine the data and the metadata about the code
			allData_str = json.loads(raw_json)
			metadata_str = json.loads(raw_metadata)
			datastream_combined = {key : value for (key,value) in (allData_str.items() + metadata_str.items())}
			
			#create symbol json string and append to data
			data_with_symbol = {key : value for (key,value) in (search_symbol.items() + datastream_combined.items())}
			
			#append group
			group_code = {'Custom_Group' : group}
			data_with_group = {key : value for (key,value) in (group_code.items() + data_with_symbol.items())}
			
			#append category
			category = {'Custom_Description' : desc}
			data_with_category = {key : value for (key,value) in (category.items() + data_with_group.items())}
			
			#append download timestamp
			final_data = {key : value for (key,value) in (download_date.items() + data_with_category.items())}
			final_data_json = json.dumps(final_data)
		
			#decode to the right format for saving to disk
			json_file = json.JSONDecoder().decode((final_data_json))
			
			#save to json file on server
			if(len(group_value) > 1):
				filename = dir_output + desc + '_' + group + '_' + code_key + '.json'
			else:
				filename = dir_output + desc + '_' + group + '.json'
				
			with open(filename,'w') as outfile:
				json.dump(json_file,outfile,sort_keys=True)

print "time taken for " + str(sys.argv[3]) + " to be retrieved: "  + str(time_taken)
