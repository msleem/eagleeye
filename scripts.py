# -*- coding: cp1252 -*-
from __future__ import division
import time
import math
import csv
import numpy as numpy
import matplotlib
import matplotlib.pyplot as plt
from collections import Counter
from pylab import *
from scipy.stats.stats import pearsonr
from scipy.spatial.distance import * 
from datetime import datetime
import re
import string
import datetime as dt
import matplotlib.dates as mdates
import random
import itertools
import operator
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser


locations = {}
crimes = {} #dict of the cimes, and list of the instances
worstLocs = []
worstLocsCrimes = {} #dict of the top 10 crimes, and then filtered down to type of crime
days = {} #days and their list of crimes
worstdays = [] #worst top 10 days
worstdaysdict = {}
dispDict = {}
loclist = []


    

def getWorstLoc():
    docs = []
    with open("FinalData.csv", 'rb') as f:
        reader = csv.DictReader(f)
        docs = [ d for d in reader ]

    for w in docs:
        curLocation = w["General Location"]
        if curLocation in locations:
            locations[curLocation].append(w)
        else:
            locations[curLocation] = []
            locations[curLocation].append(w)

    for w in locations:
        if len(locations[w]) > 50:
            worstLocs.append(w)
            worstLocsCrimes[w] = {}

def crimePie():
    with open("FinalData.csv", 'rb') as f:
        reader = csv.DictReader(f)
        docs = [ d for d in reader ]

    total = len(docs)
    res = []
    y = 0
    for c in crimes:
        l = []
        l.append(c)
        y = len(crimes[c]) + y
        l.append((len(crimes[c])/total)*100)
        res.append(l)

    print "CRIME BREAKDOWN"
    print "-------------------"
    print res
    print
    print
    print "Individual Breakdown by Location"
    print "-------------------------------"
    for c in crimes:
        print c
        fil = []
        curList = crimes[c]
        iTotal = len(curList)
        for w in locations:
            temp = 0
            for x in locations[w]:
                if x['Classification'] == c:
                    temp = temp + 1
            if temp > 0:
                l = []
                l.append(w)
                l.append(100*(temp/iTotal))
                fil.append(l)
        print fil
        print
        print
            
    
        
        
def filterWorstLocs():
    docs = []
    with open("FinalData.csv", 'rb') as f:
        reader = csv.DictReader(f)
        docs = [ d for d in reader ]

    for w in docs:
        crime = w["Classification"]
        if crime in crimes:
            crimes[crime].append(w)
        else:
            crimes[crime] = []
            crimes[crime].append(w)
            
    with open("FinalData.csv", 'rb') as f:
        reader = csv.DictReader(f)
        docs = [ d for d in reader ]
        
    for w in docs:
        disp = w["Disposition"]
        if disp in dispDict:
            dispDict[disp].append(w)
        else:
            dispDict[disp] = []
            dispDict[disp].append(w)
    
    for w in crimes:
        typ = w
        curList = crimes[w]
        for c in curList:
            loc = c['General Location']
            if loc in worstLocs:
                if typ in worstLocsCrimes[loc]:
                    worstLocsCrimes[loc][typ].append(c)
                else:
                    worstLocsCrimes[loc][typ] = []
                    worstLocsCrimes[loc][typ].append(c)

    for loc in worstLocsCrimes:
        #print loc
        s = ""
        #for t in worstLocsCrimes[loc]:
            #print "'"+t+"',"
        #print
        for t in worstLocsCrimes[loc]:
            s = s + ","  + str(len(worstLocsCrimes[loc][t])) 
        #print s
        #print
            
def top10days():
    docs = []
    with open("FinalData.csv", 'rb') as f:
        reader = csv.DictReader(f)
        docs = [ d for d in reader ]
        
    for w in docs:
        curday = w["Date Occurred"]
        if curday in days:
            days[curday].append(w)
        else:
            days[curday] = []
            days[curday].append(w)

    s = ""
    n = ""
    print "Top 10 worst days"
    for w in days:
        if len(days[w]) > 18:
            worstdaysdict[w] = {}
            worstdays.append(w)
            print w
            s = s + "," + str(len(days[w]))
    print 
    print s[1:]
    print
    print
    print

    #getting by crime type

    for c in crimes:
        curList = crimes[c]
        for k in curList:
            d = k["Date Occurred"]
            if d in worstdays:
                if c in worstdaysdict[d]:
                    worstdaysdict[d][c].append(k)
                else:
                    worstdaysdict[d][c] = []
                    worstdaysdict[d][c].append(k)

    print "CRIME TYPE FILTER"
    print
    for day in worstdays:
        print day
        s = ""
        for t in worstdaysdict[day]:
            print "'"+t+"',"
        print
        for t in worstdaysdict[day]:
            s = s + ","  + str(len(worstdaysdict[day][t]))
        print s[1:]
        print

    for w in locations:
        curList = locations[w]
        for c in curList:
            day = c["Date Occurred"]
            if day in worstdays:
                if w in worstdaysdict[day]:
                    worstdaysdict[day][w].append(k)
                else:
                    worstdaysdict[day][w] = []
                    loclist.append(w)
                    worstdaysdict[day][w].append(k)
    print
    print
    print "LOCATION FILTER"
    print
    for day in worstdays:
        print day
        s = ""
        for t in worstdaysdict[day]:
            if t in loclist:
                print "'"+t+"',"
        print
        for t in worstdaysdict[day]:
            if t in loclist:
                s = s + ","  + str(len(worstdaysdict[day][t]))
        print s[1:]
        print

    
    
def cleaner():
    docs = []
    with open("FinalData.csv", 'rb') as f:
        reader = csv.DictReader(f)
        docs = [ d for d in reader ]
    
    for record in docs:
        #check time
        a = {}
        raw_time = record['Time Occurred']
        converted_time = dt.time(hour=int(raw_time[0:2]), minute=int(raw_time[2:4]))
        d = dt.datetime.combine(dt.datetime.today(), converted_time)
        if d.hour < 6 and d.hour > 0:
            record['Time Occurred'] = "Night"
        elif d.hour < 12 and d.hour >= 6:
            record['Time Occurred'] = "Morning"
        elif d.hour < 18 and d.hour >= 12:
            record['Time Occurred'] = "Afternoon"
        else:
            record['Time Occurred'] = "Evening"
    

        date = record['Date Occurred'][0:2]
        print
        print date
        if date == '12' or date == '01' or date == '02':
            record['Date Occurred'] = "Winter"
        elif date == '9' or date == '10' or date == '11':
            record['Date Occurred'] = "Fall"
        elif date == '08' or date == '07' or date == '06':
            record['Date Occurred'] = "Summer"
        else:
            record['Date Occurred'] = "Spring"

    with open("ruleData.csv",'wb') as f:
        writer = csv.DictWriter(f, docs[0].keys())
        writer.writeheader()
        for d in docs:
            writer.writerow(d)
def bike():
    docs = []
    bl = {}
    with open("bikes.csv", 'rb') as f:
        reader = csv.DictReader(f)
        docs = [ d for d in reader ]
        
    print "top worst locations for bikes"
    print
    print
    for w in docs:
        if w['Classification'] == 'Theft':
            loc = w['General Location']
            if loc in bl:
                bl[loc] = bl[loc] + 1
            else:
                bl[loc] = 1
    s = ""
    for loc in bl:
        if bl[loc] > 11:
            print "'"+loc + "',"
            s = s + "," + str(bl[loc])
    print
    print s
    

def dorm():
    with open("dorms.csv", 'rb') as f:
        reader = csv.DictReader(f)
        docs = [ d for d in reader ]
    dcrimes = {}
    dl = {}
    for w in docs:
        typ = w['Classification']
        loc = w['General\nLocation']
        if typ in dcrimes:
            if loc in dcrimes[typ]:
                dcrimes[typ][loc] = dcrimes[typ][loc] + 1
            else:
                dcrimes[typ][loc] = 1
        else:
            dcrimes[typ] = {}
            if loc in dcrimes[typ]:
                dcrimes[typ][loc] = dcrimes[typ][loc] + 1
            else:
                dcrimes[typ][loc] = 1
    for typ in dcrimes:
        print "TYPE: " + typ
        print "----------------------"
        for l in dcrimes[typ]:
            print l + ":" + str(dcrimes[typ][l])
        print
        print
        print


    for w in docs:
        loc = w['General\nLocation']
        if loc in dl:
            dl[loc] = dl[loc] + 1
        else:
            dl[loc] = 1
    print
    print "Overview:"
    print "*******************"
    dl = sorted(dl.iteritems(), key=operator.itemgetter(1), reverse = True)
    print type(dl)
    print dl
    for loc in dl: 
        print loc[0] + " : " + str(loc[1])
    print
    print
    print
    print
    print
    print

    dl = {}
    for record in docs:
        #check time
        a = {}
        raw_time = record['Time\nOccurred']
        converted_time = dt.time(hour=int(raw_time[0:2]), minute=int(raw_time[2:4]))
        d = dt.datetime.combine(dt.datetime.today(), converted_time)
        if d.hour < 6 and d.hour > 0:
            loc = record['General\nLocation']
            if loc in dl:
                dl[loc] = dl[loc] + 1
            else:
                dl[loc] = 1
    dl = sorted(dl.iteritems(), key=operator.itemgetter(1), reverse = True)
    print "NIGHT TIMEE"
    for loc in dl: 
        print loc[0] + " : " + str(loc[1])
       
def main():
    getWorstLoc()
    filterWorstLocs()
    dorm()
    #bike()
    
    #top10days()
    #crimePie()
    #cleaner()
    
if __name__=="__main__":
    main()
