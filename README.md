### automate_pydatastream ###
This project is a script that automates data retrieval from Thomson Reuters Enterprise (DWE) SOAP API (non free) using the pydatastream python interface. 

This script will require valid credentials for accessing the API.

The script is capable of retrieving multiple fields of data for multiple tickers and storing them as JSON files.

Some preprocessing is also done to clean the data such as formatting the time and replacing default key names with friendly key names.

###Running the python script ###

1. Create 1 or more files in the input directory that contains the ticker and the custom fields that is to be pulled

2. Run the script with your valid credentials:
	automate_pydatastream.sh <username> <password>

3. Data retrieved and cleaned is saved to the output folder in JSON

The output folder is not emptied before each run so be careful of overriding previously saved output files.

### Preprocessing ###

Some of the preprocessing cleans the data retreived from DWE such as removing the time component and replacing default key names with a friendlier key name "Custom_WS_Key". 

Additional key-value pairs are also added to the output JSON file such as:  
	1. Custom_Download_Date  
	2. Custom_Ticker  
	3. Custom_Group  
	4. Custom_Description  

### Creating files in input/ ###

JSON files in the input directory contain the ticker and custom fields that you want to pull from DWE. 

For now, creation of each file is manual. 

An input file will have the following parameters that you can customize:  
	a. description  
	b. groups  
	c. code (ticker)  
	d. custom fields  

The json key structure looks like this:
"<description>": {  
		"<group1>": {  
			"1": {  
				"code": "<ticker>",  
				"custom_field":"<custom fields>",  
				"start_date": "<YYYY-MM-DD>"  
			},  
			"2" : {  
				"code": "<ticker>",  
				"custom_field":"<custom fields>",  
				"start_date": "<YYYY-MM-DD>"  
			},  
		},  
		"group2": {  
			"1": {  
				"code": "<ticker>",  
				"custom_field":"<custom fields>",  
				"start_date": "<YYYY-MM-DD>"  
			}  
	}  

The description is the name that will be used for the output json file. 

1 Group can have many tickers, just rename "group1" to the name that you want for your group.

1 Ticker can have multiple custom fields (e.g. Price).

Each custom field must be comma separated, e.g. CI,RI

The start date must be entered with the format YYYY-MM-DD.

An example would be creating an input JSON file with the description "equities" and each group is a country, so "group1" can be "USA". 


### Output file naming convention ###
Each output file will contain all ticker data for a specific group defined in the input file.

The final output json file created will be named <description>_<group>.json if there is only 1 ticker in the group. 

For groups with multiple tickers, the naming convention will be <description>_<group>_1.json, <description>_<group>_2.json and so forth. 

### Installation and Setup ###
Basic installation can be found here, https://github.com/vfilimonov/pydatastream. 

The steps are also written in "Setup on AWS EC2".

If the setup is not on AWS EC2, please follow steps 8 and 9 in "Setup on AWS EC2".

### Setup on AWS EC2 ###
The following steps are to be run on an AWS EC2 instances:
  
1. Log into the AWS console  
  
2. Select the EC2 service  
  
3. Click on "Launch Instance"  

4. Select that it is a Ubuntu AMI  and not the default Amazon Linux AMI  

5. Configure the rest of the instance details to your liking and click "Review and Launch"  

6. SSH into the EC2 instance and ensure you have root access  

7. Update the instance by running the "apt-get update" command  

8. Install the pip manager by running the following commands:  
	8a. wget https://bootstrap.pypa.io/get-pip.py  
	8b. python get-pip.py  

9. Install the pydatastream dependencies  
	9a. apt-get install python-pandas  
	9b. pip install pandas  
	9c. pip install suds  
	9d. pip install pydatastream  


### Credits ###
This python script is built on top of pydatastream, 
All credit goes to https://github.com/vfilimonov/pydatastream for building the python interface that this script uses. 