import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections as c
import matplotlib.dates as mdates

#I live near SF so I'll start there
SFdata = pd.read_csv("sanfrancisco_incidents_summer_2014.csv")

#San Fran header
#IncidntNum,Category,Descript,DayOfWeek,Date,Time,PdDistrict,Resolution,Address,X,Y,Location,Pdid
#Important values: Category, DayOfWeek, Date, Time, PdDistrict

SFdata["Date"] = pd.to_datetime(SFdata["Date"])

#note that June has 30 days, July and August have 31

#break out crime by day of the week
dc = SFdata["DayOfWeek"].value_counts()

#bar plot this info (the index is sorted by counts)
daycall = [5,6,7,3,1,4,2]
plt.bar(daycall, dc, align="center")
plt.xticks(daycall,dc.index)
plt.show()

#we see from this that crime peaks on Friday and Saturday

#examine by category
cc = SFdata["Category"].value_counts()
crime_call = range(34)
#top 7 crimes produces 78% of all crimes
#LARCENY/THEFT is by far the largest crime
plt.bar(crime_call[0:6],cc[0:6], align="center")
plt.xticks(crime_call[0:6],cc.index[0:6])
plt.show()

#examine by location (PdDistrict)
lc = SFdata["PdDistrict"].value_counts()
loc_call = range(10)
plt.bar(loc_call,lc, align="center")
plt.xticks(loc_call,lc.index)
plt.show()

#examine by date
datec = SFdata["Date"].value_counts().sort_index()

hc = mdates.date2num(SFdata["Date"])
fig, ax = plt.subplots(1,1)
ax.hist(hc,13) #bins by week (week 13 has 8 days)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%y'))
ax.set_ylabel('Crimes per week')
ax.set_title('SF Summer 2014 - Crime rates')
plt.show()
#fig.set_size_inches(6, 4)
#plt.savefig('SF_CrimeRate.png', dpi=100)
#crime slightly increases through the Summer,but is pretty constant around 2200 per week.

#not much above, lets try number of crimes per district per day
loc_count = {}
ti = mdates.date2num(SFdata["Date"])-735385 #timestamp as ints
di = range(92) #date index

for i in range(len(lc.index)):
    loc_count[lc.index[i]] = [0]*len(datec.index)

for i in range(len(SFdata["PdDistrict"])):
    loc_count[SFdata["PdDistrict"][i]][int(ti[i])] += 1

plt.plot(di,loc_count['SOUTHERN'], label="Southern")
plt.plot(di,loc_count['MISSION'], label="Mission")
plt.plot(di,loc_count['NORTHERN'], label="Northern")
#plt.plot(di,loc_count['BAYVIEW'], label="Bayview")
#plt.plot(di,loc_count['CENTRAL'], label="Central")
#plt.plot(di,loc_count['TENDERLOIN'], label="Tenderloin")
plt.legend(loc=2,prop={'size':10})
plt.show()

#The real stuff, type of crime per district

#only works for one district at a time
dist_count = {}
for i in range(len(cc.index)):
    dist_count[cc.index[i]] = [0]*len(datec.index)

for i in range(len(SFdata["Category"])):
    if SFdata["PdDistrict"][i] == "SOUTHERN":
        dist_count[SFdata["Category"][i]][int(ti[i])] += 1

plt.plot(di,dist_count['LARCENY/THEFT'], label="LARCENY/THEFT")
plt.plot(di,dist_count['OTHER OFFENSES'], label="OTHER OFFENSES")
plt.plot(di,dist_count['NON-CRIMINAL'], label="NON-CRIMINAL")
plt.plot(di,dist_count['ASSAULT'], label="ASSAULT")
plt.plot(di,dist_count['DRUG/NARCOTIC'], label="DRUG/NARCOTIC")
plt.plot(di,dist_count['VEHICLE THEFT'], label="VEHICLE THEFT")

plt.legend(loc=2,prop={'size':10})

#A bit confusing and not too useful

#Lets examine the frequency of one type of crime across all districts

cd_count = {}

for i in range(len(lc.index)):
    cd_count[lc.index[i]] = [0]*len(datec.index)

for i in range(len(SFdata["PdDistrict"])):
    if SFdata["Category"][i] == "ARSON":
        cd_count[SFdata["PdDistrict"][i]][int(ti[i])] += 1

#Taken from District Station Boundaries Final Report - 2008
#http://sanfranciscopolice.org/sites/default/files/FileCenter/Documents/14683-SFPD_DSBAfinal_trnsmtl.pdf
pop = {'SOUTHERN': 24157., 'MISSION': 83235., 'NORTHERN': 82348., 'CENTRAL': 69276., 'BAYVIEW': 60301., 'INGLESIDE': 132328., 'TENDERLOIN': 21669., 'TARAVAL': 147806., 'PARK': 59572., 'RICHMOND': 93693.}

#Gives number of crimes per 10000 people in a district
avg_c = {k:sum(v)/pop[k]*10000 for k,v in cd_count.items()}

fig, ax = plt.subplots(1,1)
plt.bar(loc_call,avg_c.values(), align="center")
ax.set_ylabel('Crimes per 10,000')
ax.set_title('SF Crime Rate for Larceny/Theft')
plt.xticks(loc_call,avg_c.keys(), fontsize=6)
plt.savefig('LT.png', dpi=100)

#to see the sum for each district
print {k:sum(v) for k,v in cd_count.items()}

plt.plot(di,cd_count['SOUTHERN'], label="SOUTHERN")
plt.plot(di,cd_count['MISSION'], label="MISSION")
plt.plot(di,cd_count['NORTHERN'], label="NORTHERN")
plt.plot(di,cd_count['BAYVIEW'], label="BAYVIEW")

plt.legend(loc=2,prop={'size':10})
