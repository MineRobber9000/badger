import ast, csv, sys

with open("plugins/badge_plugin.py") as f:
	tree = ast.parse(f.read())

ret = [["Badge name","Chance to pull"]]

for statement in tree.body:
	if type(statement)==ast.Assign and statement.targets[0].id=="badge_weights":
		# Bingo!
		d = statement.value
		assert len(d.keys)==len(d.values)
		for i in range(len(d.keys)):
			key = d.keys[i].s
			value = d.values[i].n
			ret.append([key,f"{value:0.2%}"])

ret[1:]=sorted(ret[1:],key=lambda x: -float(x[1][:-1]))
w = csv.writer(sys.stdout)
w.writerows(ret)
