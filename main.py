import requests
import json
from helpers import set_date, grossdashboard, percapitastats, onestatevisual, statecomparison
import sys

#Make an API call, and store the response
statesurl = 'https://api.covidtracking.com/v1/states/daily.json'
statejson = requests.get(statesurl)

#Save updated COVID data locally in readable format.
response_dict = statejson.json()
statedata_file = 'Projects//CS50_Final_Project//StateData.json'
with open(statedata_file, 'w') as f:
    json.dump(response_dict, f, indent=4)

#Prompt User for date range to analyze data for, then compile standard data for that range.
set_date()

#Now that we have a daterange, select what we want to analyze (options menu)
while (True):
    option = input(
        "Please select an option by entering the associated number in the terminal:\n \t 1. All State Dashboard (gross)\n\t 2. All State Dashboard (per capita) \n \t 3. Individual State Visualized Data \n \t 4. Visualized State Comparison \n \t 5. Change Date Range \n \t 6. Exit Program \n")
    if option == "1":
        grossdashboard()
        pass
    elif option == "2":
        percapitastats()
        pass
    elif option == "3":
        onestatevisual()
        pass
    elif option == "4":
        statecomparison()
        pass
    elif option == "5":
        set_date()
        pass
    elif option == "6":
        sys.exit()
    else:
        print("Invalid selection. Please try again.")