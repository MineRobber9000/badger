import json, os.path, badge
from collections import Counter

with open(os.path.join(os.path.dirname(__file__),"badges.json")) as f: pop = badge.BadgePopulation.from_json(json.load(f))

badges = []

for badge in set([badge.name for badge in pop.population]):
	badges.append([badge,"{:0.2%}".format(pop.rarity(badge))])

badges.sort(key=lambda x: -float(x[1][:-1]))
for badge in badges: print(": ".join(badge))
