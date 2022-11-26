def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def fileToDict(fname):
    stack = []
    dictionary = dict()
    file = open(fname, "r")
    length = file_len(fname)
    file.readline()
    token = 1
    stack.push("{")
    while token < length:
        line = file.readline()
        token = token+1


dictionary = dict()
file = open(fname, "r")
line = file.readline().strip()
linedata = line.split(" ")
for data in linedata:
    if data.endswith(":")
        key = data.replace(":", "")
        if(data.)
dictionary[
