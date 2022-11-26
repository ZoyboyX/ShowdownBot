import json

with open('moves1.txt') as json_file:
    data = json.load(json_file)

print(data)
