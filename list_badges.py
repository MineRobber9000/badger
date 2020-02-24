import json
from collections import Counter

with open("badges.json") as f: badges = json.load(f)

for k in badges:
	if k.startswith("__"): continue
	l = []
	counter = Counter([b["name"] for b in badges[k]])
	for item in counter.items():
		l.append("{} (x{!s})".format(*item))
	print("{}: {}".format(k,", ".join(l)))
