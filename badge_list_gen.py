import json, os.path, csv
from collections import Counter

with open(os.path.join(os.path.dirname(__file__),"badges.json")) as f: badges = json.load(f)
with open(os.path.join(os.path.dirname(__file__),"association.json")) as f: names = json.load(f)

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
out = []
for user in users:
	out.append([names.get(user[0],user[0]),user[1]])

class PSV(csv.unix_dialect):
	delimiter="|"
	quoting=csv.QUOTE_NONE

with open(os.path.join(os.path.dirname(__name__),"badge_list.psv"),"w") as f:
	w = csv.writer(f,PSV)
	w.writerows(out)
