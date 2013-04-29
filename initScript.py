import itertools
import sys
import datetime

items = []
dates = []
fDates = []
count = []
crimes = []
crimeCount = []
locations = []
locCount = []


def getCrimes():
	for x in items:
		tempCrime = x[0]
		there = False
		for y in crimes:
			if y == tempCrime:
				there = True
		if there == False and tempCrime != 'Classification':
			crimes.append(tempCrime)
			
def getCrimeCount():
	print("COUNT")
	for x in crimes:
		c = 0
		for y in items:
			if y[0] == x:
				c += 1
		perc = c / (len(items)-1)
		print(perc)
		print(x)
		crimeCount.append(perc)

def printCrimeCount():
		f = open('crimeCount.txt', 'w')
		for i, x in enumerate(crimes):
			p = crimeCount[i] * 100
			f.write("[\'" + str(x) + "\', " + str(p) + "],")
		f.close()
	
def getDates():
	for x in items:
		tempDate = x[3]
		there = False
		for y in dates:
			if y == tempDate:
				there = True
		if there == False and tempDate != 'Date Occurred':
			dates.append(tempDate)
def getLocations():
	for x in items:
		tempLoc = x[5]
		there = False
		for y in locations:
			if y == tempLoc:
				there = True
		if there == False and tempLoc != 'General Location':
			locations.append(tempLoc)
			print(tempLoc)
	print(len(locations))
	for z in locations:
		c = 0
		for n in items:
			if z == n[5]:
				c += 1
		locCount.append(c)
#	f = open('worstCrimes.txt', 'w')
#	for ind, a in enumerate(locations):
##			f.write("\'" + str(a) + "\'," + "\n")
	#f.write("\n")
	#for dex, b in enumerate(locCount):
	#	if b >= 30:
	#		f.write(str(b) + ",")
	#f.close()
	
def formatDates():
	for x in dates:
		temp = x.strip().split('/')
		dt = datetime.date(int(temp[2]), int(temp[0]), int(temp[1]))
		fDates.append(dt)
	c = 0
	while c < len(fDates):
		for i, n in enumerate(fDates):
			if i < len(fDates)-1:
				if fDates[i+1] < fDates[i]:
					t = fDates[i]
					fDates[i] = fDates[i+1]
					fDates[i+1] = t
					tempC = count[i]
					count[i] = count[i+1]
					count[i+1] = tempC
		c += 1
	
def getCount():
	for x in dates:
		c = 0
		for y in items:
			if y[3] == x:
				c += 1
		count.append(c)
		
def worstDays():
	c = 0
	while c < len(count):
		for i, n in enumerate(count):
			if i < len(count)-1:
				if count[i+1] > count[i]:
					temp = count[i]
					count[i] = count[i+1]
					count[i+1] = temp
					td = fDates[i]
					fDates[i] = fDates[i+1]
					fDates[i+1] = td
		c += 1
	b = 1
	f = open('10worstdays.txt', 'w')
	while b <= 10:
		f.write(str(fDates[b-1].month) + "-" + str(fDates[b-1].day) + "-" + str(fDates[b-1].year) + ",\n")
		b += 1
	f.write("\n")
	b = 1
	while b <= 10:
		f.write(str(count[b-1]) + ",")
		b += 1
	f.close()
	
def printout():
	f = open('crimeData.txt', 'w')
	for i, x in enumerate(fDates):
		f.write("[Date.UTC(" + str(x.year) + "," + str(x.month) + "," + str(x.day) + ")," + str(count[i]) + "],")
	f.close()
		
print("GET DATA")
for line in open("AlmostCleanData.txt"):
	items.append(line.strip().split('	'))
getDates()
getCount()
#getCrimes()
#getCrimeCount()
#printCrimeCount()
formatDates()
#worstDays()
getLocations()
#printout()
input()