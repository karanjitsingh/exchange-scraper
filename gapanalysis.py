import sys
import os
from os import path
import re
import json


second = 1000
minute = second * 60
hour = minute * 60
day = hour * 24

import argparse


parser = argparse.ArgumentParser(add_help=True)

parser.add_argument("--path", type=str, help="Path to dump folder", required=True)
parser.add_argument("--time", type=int, help="Time in minutes", default=1)

args = vars(parser.parse_args())

folder =  os.path.relpath(args['path'])
time = args['time']
dumpPath = os.path.join(os.getcwd(), folder)

dumpJsons = list(filter(lambda file: re.match("^\d{4}-\d{2}-\d{2}(\.[12])?\.json$", file), os.listdir(dumpPath)))

consolidatedData = []

lastTime = []

gaps = []

for i in range(len(dumpJsons)):
    with open(path.join(dumpPath, dumpJsons[i]), "r") as file:
        content = file.read()

    data = json.loads(content)

    for j in range(len(data)):
        if lastTime == []:
            lastTime = [data[j][0], dumpJsons[i], j]
        else:
            if data[j][0] - lastTime[0] > minute * time:
                gaps.append([lastTime[0], data[j][0]])
                print("Gap: lastTime:", lastTime, " Current: ", [data[j][0], dumpJsons[i], j], "Difference: ", str((float(data[j][0]) - float(lastTime[0]))/minute))

            lastTime = [data[j][0], dumpJsons[i], j]

with open(os.path.join(dumpPath, "gaps.json"), "w") as file:
    file.write(json.dumps(gaps,indent=2))