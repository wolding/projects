#! python3
# callLog.py - Reads downloaded facebook data (.json) finds the video calls and writes them to a new file, while
# changing the timestamp from milliseconds to a real date

import json
import datetime
from pathlib import Path


# Cycle through the files in FacebookCalls folder

logList = []
p = Path(Path.home() / 'FacebookCalls')
for jsonFile in p.glob('*.json'):

    # Find the video calls and copy the relevant lines

    f = open(Path.home() / 'FacebookCalls' / jsonFile, )
    data = json.load(f)
    for item in data['messages']:
        if item['type'] == 'Call':

            # Create list of all calls
            logList.append(item)
    f.close()

# Sort call log by timestamp
sortedLog = sorted(logList, key=lambda i: i['timestamp_ms'])

# Create call log
logFile = open(Path.home() / 'callLog1.txt', 'w')
logFile.write("Facebook Call Log\n")
logFile.close()
total_duration = 0
count = 0

for call in sortedLog:
    total_duration += call['call_duration']
    if call['call_duration'] == 0:
        pass
    else:
        count += 1
    # Change the timestamp to a date
    msStamp = call['timestamp_ms']
    newDate = datetime.datetime.fromtimestamp(msStamp // 1000)
    date = newDate.strftime('%Y-%m-%d %H:%M:%S')
    call['timestamp_ms'] = date

    # Convert call duration from seconds to hours:minutes:seconds
    callTime = call['call_duration']
    call['call_duration'] = str(datetime.timedelta(seconds=callTime))

    formattedCall = f"""
        Sender: {call['sender_name']}
        Type: {call['type']}
        Timestamp: {call['timestamp_ms']}
        Content: {call['content']}
        Duration: {call['call_duration']}

    """
    # Add the formatted Call to the call log
    logFile = open(Path.home() / 'callLog1.txt', 'a')
    logFile.write(formattedCall)
    logFile.close()
print(total_duration)
timeTotal = str(datetime.timedelta(seconds=total_duration))
# print(timeTotal)
# print(count)

