import json, os.path
from collections import Counter

with open(os.path.join(os.path.dirname(__file__),"badges.json")) as f: badges = json.load(f)

users = []

for k in badges:
	if k.startswith("__"): continue
	l = []
	counter = Counter([b["name"] for b in badges[k]])
	total = 0
	for item in counter.items():
		l.append("{} (x{!s})".format(*item))
		total+=item[1]
	users.append([k,", ".join(l),total])

users.sort(key=lambda x: -x[2])
for user in users: print(": ".join(user[:-1]))
