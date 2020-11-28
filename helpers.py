import datetime as dt
import json
from plotly.graph_objs import Bar, Layout
from plotly import offline
import matplotlib.pyplot as plt

#variables for storing date ranges, list to store dates in range
startdate = None
enddate = None
days = None
datelist = []

#Lists/Dicts to create dictionaries with state statistics based on specified date range
statelist = []
statedict = []

#Dictionary of state populations for use with per capita analysis
statepops= {
    "AL": 4908620,
    "AK": 734002,
    "AS": 55145,
    "AZ": 7378490,
    "AR": 3039000,
    "CA": 39937500,
    "CO": 5845530,
    "CT": 3563080,
    "DE": 982895,
    "DC": 720687,
    "FL": 21993000,
    "GA": 10736100,
    "GU": 165768,
    "HI": 1412690,
    "ID": 1826670,
    "IL": 12659700,
    "IN": 6475350,
    "IA": 3179850,
    "KS": 2910360,
    "KY": 4490690,
    "LA": 4645180,
    "ME": 1345790,
    "MD": 6083120,
    "MA": 6976600,
    "MI": 10045000,
    "MN": 5700670,
    "MS": 2989260,
    "MO": 6169270,
    "MT": 1086769,
    "NE": 1952570,
    "NV": 3139660,
    "NH": 1371250,
    "NJ": 8936570,
    "NM": 2096940,
    "NY": 19440500,
    "NC": 10611900,
    "ND": 761723,
    "MP": 53883,
    "OH": 11747700,
    "OK": 3954820,
    "OR": 4301090,
    "PW": 17907,
    "PA": 12820900,
    "PR": 3032160,
    "RI": 1056160,
    "SC": 5210100,
    "SD": 903027,
    "TN": 6897580,
    "TX": 29472300,
    "UT": 3282120,
    "VT": 628061,
    "VI": 104365,
    "VA": 8626210,
    "WA": 7797100,
    "WV": 1778070,
    "WI": 5851750,
    "WY": 567025,
}

def set_date():
    """Function to set date range to be analyzed, then create a list with a dict for each state with relevant info in the time period"""
    global startdate
    global enddate
    global days

    #Solicit date range to analyze, testing for format.
    while (True):
        daterange = input("\nWhat date range do you wish to analyze? (MMDDYY-MMDDYY format):\n")
        if len(daterange) != 13:
            print("\nLength not valid. Try again")
        elif daterange[0:6].isnumeric == False or daterange[7:13].isnumeric == False:
            print("Date not in valid format. Try again.")
        elif daterange[6] != '-':
            print("Dates not seperated by '-' as required.")
        else:
            print("\n")
            break
    
    #Using date range, create a list of dates included in that range.
    datelist.clear()
    startdate = f"20{daterange[4:6]}{daterange[0:2]}{daterange[2:4]}"
    startdate = dt.datetime.strptime(startdate, "%Y%m%d")
    enddate = f"20{daterange[11:13]}{daterange[7:9]}{daterange[9:11]}"
    enddate = dt.datetime.strptime(enddate, "%Y%m%d")
    days = int((enddate-startdate).days + 1)
    for x in range(days):
        day = startdate + dt.timedelta(x)
        day = day.strftime("%Y%m%d")
        datelist.append(day)

    #Create a list with a dict for each state with all generally important info based on specified date range.
    statelist.clear()
    statedict.clear()
    with open('Projects//CS50_Final_Project//StateData.json') as f:
        datafile = json.load(f)
        for x in range(len(datafile)):
            if datafile[x]["state"] not in statelist:
                statelist.append(datafile[x]["state"])
        statelist.sort()
        for state in range(len(statelist)):
            statedict.append({
                "state": statelist[state],
                #INT field for new deaths increase
                "deathIncrease": 0,
                #INT field for new hospitalizations
                "hospitalizedIncrease": 0,
                #INT Daily increase in positive+probable cases
                "positiveIncrease": 0,
            })
        for x in range(len(datafile)):
            if str(datafile[x]["date"]) in datelist:
                for i in range(len(statedict)):
                    if datafile[x]["state"] == statedict[i]["state"]:
                        statedict[i]["deathIncrease"] += datafile[x]["deathIncrease"]
                        statedict[i]["hospitalizedIncrease"] += datafile[x]["hospitalizedIncrease"]
                        statedict[i]["positiveIncrease"] += datafile[x]["positiveIncrease"]

def grossdashboard():
    """Creates a dashboard of states with the worst numbers in selected time frame"""
    numofstates = 0
    while numofstates < 1 or numofstates > len(statelist):
        numofstates = int(input("Select a number to view the top ___ states (5, 10, 25, etc.): "))
        
    #Print Dashboard
    statedeaths = sorted(statedict, key=lambda k: k['deathIncrease'], reverse=True)
    statehospitalized = sorted(statedict, key=lambda k: k['hospitalizedIncrease'], reverse=True)
    statepositives = sorted(statedict, key=lambda k: k['positiveIncrease'], reverse=True)
        
    print("\nLeaders in positive cases in specified timeframe:")
    for x in range(numofstates):
        print(f"{x + 1}. {statepositives[x]['state']}: {statepositives[x]['positiveIncrease']} positive cases.")

    print("\nLeaders in Hospitalization in specified timeframe:")
    for x in range(numofstates):
        print(f"{x + 1}. {statehospitalized[x]['state']}: {statehospitalized[x]['hospitalizedIncrease']} hospitalizations.")

    print("\nLeaders in Deaths in specified timeframe:")
    for x in range(numofstates):
        print(f"{x + 1}. {statedeaths[x]['state']}: {statedeaths[x]['deathIncrease']} deaths")
    
    print("\n")

def percapitastats():
    #Creat a list of dicts for each state with per capita stats.
    percapdict = []
    for states in range(len(statelist)):
        percapdict.append({"state": statelist[states]})
        try:
            statepops[statelist[states]] / statedict[states]["deathIncrease"]
        except ZeroDivisionError:
            percapdict[states]["PerCapdeathIncrease"] = 0
        else:
            percapdict[states]["PerCapdeathIncrease"] = int(statepops[statelist[states]] / statedict[states]["deathIncrease"])
        try:
            statepops[statelist[states]] / statedict[states]["hospitalizedIncrease"]
        except ZeroDivisionError:
            percapdict[states]["PerCaphospitalizedIncrease"] = 0
        else:
            percapdict[states]["PerCaphospitalizedIncrease"] = int(statepops[statelist[states]] / statedict[states]["hospitalizedIncrease"])
        try:
            statepops[statelist[states]] / statedict[states]["positiveIncrease"]
        except ZeroDivisionError:
            percapdict[states]["PerCappositiveIncrease"] = 0
        else:
            percapdict[states]["PerCappositiveIncrease"] = int(statepops[statelist[states]] / statedict[states]["positiveIncrease"])
    
    #Print Dashboard for specified number of states
    numofstates = 0
    while numofstates < 1 or numofstates > len(statelist):
        numofstates = int(input("Select a number to view the top ___ states (5, 10, 25, etc.): "))

    #Create ordered dicts by stats, and counters
    statedeaths = sorted(percapdict, key=lambda k: k['PerCapdeathIncrease'])
    sdx = 0
    statehospitalized = sorted(percapdict, key=lambda k: k['PerCaphospitalizedIncrease'])
    shx = 0
    statepositives = sorted(percapdict, key=lambda k: k['PerCappositiveIncrease'])
    spx = 0

    #Print the resulting lists out for each stat    
    print("\nPer capita leaders in positive cases in specified timeframe:")
    for x in range(len(statepositives)):
        if statepositives[x]['PerCappositiveIncrease'] == 0:
            pass
        else:
            print(f"{spx + 1}. {statepositives[x]['state']}: 1 positive test per {statepositives[x]['PerCappositiveIncrease']} residents.")
            spx += 1
            if spx == numofstates:
                break
    
    print("\nPer capita leaders in Hospitalization in specified timeframe:")
    for x in range(len(statehospitalized)):
        if statehospitalized[x]['PerCaphospitalizedIncrease'] == 0:
            pass
        else:
            print(f"{shx + 1}. {statehospitalized[x]['state']}: 1 hospitalization per {statehospitalized[x]['PerCaphospitalizedIncrease']} residents.")
            shx += 1
            if shx == numofstates:
                break
    
    print("\nPer capita leaders in Deaths in specified timeframe:")
    for x in range(len(statedeaths)):
        if statedeaths[x]['PerCapdeathIncrease'] == 0:
            pass
        else:
            print(f"{sdx + 1}. {statedeaths[x]['state']}: 1 death per {statedeaths[x]['PerCapdeathIncrease']} residents.")
            sdx += 1
            if sdx == numofstates:
                break
    
    print("\n")

def onestatevisual():
    """Function to generate bar chart of daily specified stat."""

    #Get user input for selected state and statistic to graph.
    while(True):
        selectedstate = input("Select a state to analyze by entering the state code (MA, NY, CT, etc.): ")
        if selectedstate.upper() in statelist:
            break
        else:
            print("State not recognized. Please try again.")
    
    while(True):
        selectedstatistic = input("Enter the number of the statistic you wish to visualize: 1. Positive Tests 2. New Hospitalizations 3. New Deaths: ")
        if selectedstatistic == "1":
            selectedstatistic = "positiveIncrease"
            title = "New daily positive cases."
            break
        elif selectedstatistic == "2":
            selectedstatistic = "hospitalizedIncrease"
            title = "New daily hospitalizations."
            break
        elif selectedstatistic == "3":
            selectedstatistic = "deathIncrease"
            title = "New daily deaths."
            break
        else:
            print("Invalid selection. Please try again.")
    
    #Generate a list of values for the specified state on the specified date
    datalist = []
    with open('Projects//CS50_Final_Project//StateData.json') as f:
        datafile = json.load(f)
        for x in range(len(datafile)):
            if str(datafile[x]["date"]) in datelist:
                if (str(datafile[x]["state"])) == selectedstate:
                    datalist.append(datafile[x][selectedstatistic])
    
    #Convert datelist back into traditional date format
    xlist = []
    for x in range(len(datelist)):
        xlist.append(f"{datelist[x][4:6]}/{datelist[x][6:8]}/{datelist[x][2:4]}")
    datalist.reverse()  
    
    #Generate bar chart of progression of statistic in date range
    x_values = xlist
    data = [Bar(x=x_values, y=datalist)]

    x_axis_config = {'title': 'Dates'}
    y_axis_config = {'title': 'Amount'}
    my_layout = Layout(title=title, xaxis=x_axis_config, yaxis=y_axis_config)
    offline.plot({'data': data, 'layout': my_layout}, filename='onestate.html')

def statecomparison():
    """function to generate graphs to compare multiple states for new daily or total accumulated deaths"""
    #Get user input for two states
    while(True):
        selectedstate1 = input("Select the first state to analyze by entering the state code (MA, NY, CT, etc.): ")
        if selectedstate1.upper() in statelist:
            break
        else:
            print("State not recognized. Please try again.")
    while(True):
        selectedstate2 = input("Select the second state to analyze by entering the state code (MA, NY, CT, etc.): ")
        if selectedstate2.upper() in statelist:
            break
        else:
            print("State not recognized. Please try again.")

    #Get user input for stat to analyze
    while(True):
        selectedstatistic = input("Enter the number of the statistic you wish to visualize: 1. New daily deaths 2. Cumulative deaths: ")
        if selectedstatistic == "1":
            selectedstatistic = "deathIncrease"
            title = "New daily deaths"
            break
        elif selectedstatistic == "2":
            selectedstatistic = "death"
            title = "Cumulative deaths"
            break
        else:
            print("Invalid selection. Please try again.")

    #Collect and sort list for date labels and selected stat for both days
    datalist1, datalist2 = [], []
    with open('Projects//CS50_Final_Project//StateData.json') as f:
        datafile = json.load(f)
        for x in range(len(datafile)):
            if str(datafile[x]["date"]) in datelist:
                if (str(datafile[x]["state"])) == selectedstate1:
                    datalist1.append(datafile[x][selectedstatistic])
                elif (str(datafile[x]["state"])) == selectedstate2:
                    datalist2.append(datafile[x][selectedstatistic])
    datalist1.reverse()
    datalist2.reverse() 
    
    #Convert datelist back into traditional date format
    xlist = []
    for x in range(len(datelist)):
        xlist.append(dt.datetime.strptime(datelist[x], '%Y%m%d'))
        #xlist.append(f"{datelist[x][4:6]}/{datelist[x][6:8]}/{datelist[x][2:4]}")

    #Plot the comparison
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    try:
        ax.plot(xlist, datalist1, c='red', label=selectedstate1)
        ax.plot(xlist, datalist2, c='blue', label=selectedstate2)
        ax.legend()
        ax.set(ylim=(0))

        #Format plot
        title = f"{title} comparison for {selectedstate1} and {selectedstate2} over specified date range."
        ax.set_title(title, fontsize=20)
        ax.set_xlabel('', fontsize=16)
        fig.autofmt_xdate()
        ax.set_ylabel("Amount of Deaths", fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=16)

        plt.show()
    
    except:
        missingdata = []
        with open('Projects//CS50_Final_Project//StateData.json') as f:
            datafile = json.load(f)
            for x in range(len(datelist)):
                state1exists = False
                state2exists = False
                for y in range(len(datafile)):
                    if datafile[y]["date"] == int(datelist[x]) and datafile[y]["state"] == selectedstate1:
                        state1exists = True
                    elif datafile[y]["date"] == int(datelist[x]) and datafile[y]["state"] == selectedstate2:
                        state2exists = True
                if state1exists == False:
                    missingdata.append({selectedstate1: datelist[x]})
                if state2exists == False:
                    missingdata.append({selectedstate2: datelist[x]})
        print("Unexpected error. Missing data for these dates:")
        for x in range(len(missingdata)):
            print(f"{x + 1}: {missingdata[x]}")
    