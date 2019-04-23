# MongoDB Crime

import pymongo


client = pymongo.MongoClient("localhost", 27017)
db = client["CrimeDB"]
col = db["CrimeNewDates"]

# User interaction
userCont = True
print("Enter a community name within Chicago to see the individual crime rates for that area.")
while userCont == True:
    userComm = input("\nCommunity name: ")

    commDict = {"rogers park": "1", "norwood park": "10", "jefferson park": "11", "forest glen": "12", "north park": "13",
                "albany park": "14", "portage park": "15", "irving park": "16", "dunning": "17", "montclare": "18",
                "belmont cragin": "19", "west ridge": "2", "hermosa": "20", "avondale": "21", "logan square": "22",
                "humboldt park": " 23", "west town": "24", "austin": "25", "west garfield park": "26", "east garfield park": "27",
                "near west side": "28", "north lawndale": "29", "uptown": "3", "south lawndale": "30", "lower west side": "31",
                "loop": "32", "near south side": "33", "armour square": "34", "douglas": "35", "oakland": "36", "fuller park": "37",
                "grand boulevard": "38", "kenwood": "39", "lincoln square": "4", "washington park": "40", "hyde park": "41",
                "woodlawn": "42", "south shore": "43", "chatham": "44", "avalon park": "45", "south chicago": "46", "burnside": "47",
                "calumet heights": "48", "roseland": "49", "north center": "5", "pullman": "50", "south deering": "51",
                "east side": "52", "west pullman": "53", "riverdale": "54", "hegewisch": "55", "garfield ridge": "56",
                "archer heights": "57", "brighton park": "58", "mckinley park": "59", "lake view": "6", "bridgeport": "60",
                "new city": "61", "west elsdon": "62", "gage park": "63", "clearing": "64", "west lawn": "65", "chicago lawn": "66",
                "west englewood": "67", "englewood": "68", "greater grand crossing": "69", "lincoln park": "7", "ashburn": "70",
                "auburn gresham": "71", "beverly": "72", "washington heights": "73", "mount greenwood": "74", "morgan park": "75",
                "ohare": "76", "edgewater": "77", "near north side": "8", "edison park": "9"}
    if userComm == "list":
        for doc in commDict:
            print(doc)
    elif userComm not in commDict:
        print("That community doesn't exist.")
    else:
        userComm = commDict[userComm]
        monthCont = True
        while monthCont == True:
            print("\nEnter the number of months (int) you would like to see data for.")
            userMonth = input("Months: ")
            monthDict = {"1": "20190314", "2": "20190214", "3": "20190114", "4": "20181214", "5": "20181114", "6": "20181014", "7": "20180914", "8": "20180814", "9": "20180714", "10": "20180614", "11": "20180514", "12": "20180414",
                         "13": "20180314", "14": "20180214", "15": "20180114"}
            if userMonth not in monthDict:
                print("Please enter a # of months between 1 and 15.")
            else:
                userMonthStr = monthDict[userMonth]
                monthCont = False
        userCont = False



# Writing the queries
commQuery = [{"$match": {"$and": [{"Community Area": userComm}, {"Date": {"$gt": userMonthStr}}]}}, {"$group": {"_id": "$Primary Type", "total": {"$sum": 1}}}]
allQuery = [{"$match": {"Date": {"$gt": userMonthStr}}}, {"$group": {"_id": "$Primary Type", "total": {"$sum": 1}}}]
marQuery = [{"$match": {"$and": [{"Community Area": userComm}, {"Date": {"$gt": "20190300", "$lt": "20190400"}}]}}, {"$group": {"_id": "$Primary Type", "total": {"$sum": 1}}}]
febQuery = [{"$match": {"$and": [{"Community Area": userComm}, {"Date": {"$gt": "20190200", "$lt": "20190300"}}]}}, {"$group": {"_id": "$Primary Type", "total": {"$sum": 1}}}]
janQuery = [{"$match": {"$and": [{"Community Area": userComm}, {"Date": {"$gt": "20190100", "$lt": "20190200"}}]}}, {"$group": {"_id": "$Primary Type", "total": {"$sum": 1}}}]
decQuery = [{"$match": {"$and": [{"Community Area": userComm}, {"Date": {"$gt": "20181200", "$lt": "20190100"}}]}}, {"$group": {"_id": "$Primary Type", "total": {"$sum": 1}}}]
novQuery = [{"$match": {"$and": [{"Community Area": userComm}, {"Date": {"$gt": "20181100", "$lt": "20181200"}}]}}, {"$group": {"_id": "$Primary Type", "total": {"$sum": 1}}}]
octoQuery = [{"$match": {"$and": [{"Community Area": userComm}, {"Date": {"$gt": "20181000", "$lt": "20181100"}}]}}, {"$group": {"_id": "$Primary Type", "total": {"$sum": 1}}}]


# Translating the data from the queries into lists
x = col.aggregate(commQuery)
commList = []
for doc in x:
    commList.append(doc)

y = col.aggregate(allQuery)
totalList = []
for doc in y:
    totalList.append(doc)

mar = col.aggregate(marQuery)
marList = []
for doc in mar:
    marList.append(doc)

feb = col.aggregate(febQuery)
febList = []
for doc in feb:
    febList.append(doc)

jan = col.aggregate(janQuery)
janList = []
for doc in jan:
    janList.append(doc)

dec = col.aggregate(decQuery)
decList = []
for doc in dec:
    decList.append(doc)

nov = col.aggregate(novQuery)
novList = []
for doc in nov:
    novList.append(doc)

octo = col.aggregate(octoQuery)
octoList = []
for doc in octo:
    octoList.append(doc)

# Displaying the data to the user
print("\nDisplaying data for Community Area", userComm, "over the last", str(userMonth), "month(s).\n")
print("{:35} {:>10} {:>5} {:>20} {:>5} {:>5} {:>5} {:>5} {:>5}".format("Crime", "#", "%", "Mar", "Feb", "Jan", "Dec", "Nov", "Oct"))
for a in commList:
    crimeName = a["_id"]
    crimeTotal = a["total"]
    for b in totalList:
        if a["_id"] == b["_id"]:
            allTotal = b["total"]
            break
    allTotal = round((crimeTotal / allTotal) * 100)
    if allTotal == 0:
        allTotal = ("<1%")
    else:
        allTotal = (str(allTotal) + "%")

    # Totaling each prior month
    for c in marList:
        if a["_id"] == c["_id"]:
            marCount = c["total"]
            break
        else:
            marCount = "0"

    for d in febList:
        if a["_id"] == d["_id"]:
            febCount = d["total"]
            break
        else:
            febCount = "0"

    for e in janList:
        if a["_id"] == e["_id"]:
            janCount = e["total"]
            break
        else:
            janCount = "0"

    for f in decList:
        if a["_id"] == f["_id"]:
            decCount = f["total"]
            break
        else:
            decCount = "0"

    for g in novList:
        if a["_id"] == g["_id"]:
            novCount = g["total"]
            break
        else:
            novCount = "0"

    for h in octoList:
        if a["_id"] == h["_id"]:
            octoCount = h["total"]
            break
        else:
            octoCount = "0"
    # Printing the data for the user to see
    print("{:35} {:>10} {:>5} {:>20} {:>5} {:>5} {:>5} {:>5} {:>5}".format(crimeName, crimeTotal, allTotal, marCount, febCount, janCount, decCount, novCount, octoCount))
