import subprocess
import datetime
import platform
import json
import sys

filename = sys.argv[1]
websiteList = open(filename, "r")

webList = []
sorok = 0

for i in range(10):
    webList.append(websiteList.readline().split(",")[1].rstrip())

for line in reversed(list(open(filename))):
    if (sorok < 10):
        webList.append(line.split(",")[1].rstrip())
        sorok += 1

date = datetime.datetime.today()
encoding = "utf-8"
system = platform.system()

pingResult = {
    "date": date.strftime("%Y%m%d"),
    "system": system,
    "pings": []
}

tracertResult = {
    "date": date.strftime("%Y%m%d"),
    "system": system,
    "traces": []
}

for host in webList:
    print(host)

    pingOption = '-n' if system == 'Windows' else '-c'
    pingCommand = ['ping', pingOption, '10', host]

    tracertCom = 'tracert' if system == 'Windows' else 'traceroute'
    tracertOption = '-h' if system == 'Windows' else '-m'
    tracertCommand = [tracertCom, tracertOption, '30', host]

    pingRes = subprocess.Popen(pingCommand, stdout=subprocess.PIPE).stdout.read().decode(encoding)
    pingResult["pings"].append({
        "target": host,
        "output": pingRes
    })

    tracertRes = subprocess.Popen(tracertCommand, stdout=subprocess.PIPE).stdout.read().decode(encoding)
    tracertResult["traces"].append({
        "target": host,
        "output": tracertRes
    })

with open ("ping.json", "w") as pingFile:
    json.dump(pingResult, pingFile)

with open ("traceroute.json", "w") as tracertFile:
    json.dump(tracertResult, tracertFile)
    
websiteList.close()
