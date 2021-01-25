import os
from pprint import pprint

from Aplikacja import seqplayer

path = "../Badania/Termo/termo/all"
result = [
    os.path.join(dp, f)
    for dp, dn, filenames in os.walk(path)
    for f in filenames
    if os.path.splitext(f)[1].upper() in (".SEQ", ".IMG")
]

file_times = {}
for file_path in result:
    seq = seqplayer.SeqReader(file_path)
    file_times[file_path] = seq.frame(0).time

for (file_path, time) in sorted(file_times.items(), key=lambda item: item[1]):
    print(f"{file_path:60s} {time}")