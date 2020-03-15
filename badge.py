import random as _random
from collections import defaultdict
from math import tan, atan, pi, log
import json

class UserDoesntHaveEnoughBadges(Exception):
	pass

def quantile(x,m,p):
	c=1-m
	if x<=0.5: # x <= 1/2
		return m*((2*x)**(1/(m*p-1)))
	else: # x > 1/2
		return 1-c*((2-2*x)**(1/(c*p-1)))

def random(m,p):
	return quantile(1-_random.random(),m,p)

class Badge:
	def __init__(self,name,normal=True):
		self.name=name
		self.normal=normal
	def to_json(self):
		return dict(name=self.name,normal=self.normal)
	@classmethod
	def from_json(self,d):
		if type(d)==str: d=json.loads(d)
		return self(d["name"],d["normal"])
	def __str__(self):
		return "{} (normally generated: {!s})".format(self.name,self.normal)
	def __repr__(self):
		return f"<{self!s}>"

W = 0.2

def calculate_rarities(badges):
	existing = len(badges)
	normals = len([x for x in badges if x.normal])
	existing_c = defaultdict(int)
	normal_c = defaultdict(int)
	for badge in badges:
		existing_c[badge.name]+=1
		if badge.normal: normal_c[badge.name]+=1
	r = dict()
	for k in existing_c:
		r[k]=[existing_c[k]/existing,normal_c[k]/normals]
		r[k].append((r[k][0]*W)+(r[k][1]*(1-W)))
	return r

class BadgePopulation:
	def __init__(self):
		self.badges = dict()
	def give_badge(self,to,name,normal=True):
		if to not in self.badges:
			self.badges[to]=[]
		self.badges[to].append(Badge(name,normal))
		self.badges[to].sort(key=lambda x: x.name+("1" if x.normal else "0"))
	@property
	def population(self):
		ret = []
		for to in self.badges: ret.extend(self.badges[to])
		return ret
	def rarity(self,name):
		rarities = calculate_rarities(self.population)
		return rarities[name][2] # effective rarity
	def transmute(self,user,*badge_names):
		badge_names = list(badge_names)
		for badge_name in badge_names:
			found=False
			for badge in self.badges[user]:
				if badge.name==badge_name: found=True
			if not found:
				raise UserDoesntHaveEnoughBadges(f"User {user} does not have a {badge_name}!")
		rarities = calculate_rarities(self.population)
		badges = [rarities[name][2] for name in badge_names]
		badges.insert(0,1-_random.random())
		N = (((1-W)/len([x for x in self.population if x.normal]))+(W/len(self.population)))**-1
		for badge_name in badge_names:
			taken = False
			for badge in self.badges[user]:
				if not taken and badge.name==badge_name:
					taken=True
					self.badges[user].remove(badge)
		m=1-(2/pi)*atan(sum(map(lambda x: tan((pi/2)*(1-x)),badges)))
		p=((log(1+m*N)+log(m*N)-log(2))/(m*log(m*N)))
		out = random(m,p)
		if out not in [rarities[k][2] for k in rarities]:
			L=0
			H=1
			for badge in rarities:
				if rarities[badge][2]<out:
					if abs(out-rarities[badge][2])<abs(out-L):
						L = rarities[badge][2]
				else: # rarities[badge][2]>out
					if abs(rarities[badge][2]-out)<abs(H-out):
						H = rarities[badge][2]
			n = _random.uniform(L,H)
			if n<out:
				out=H
			else:
				out=L
		possible_out = [badge_name for badge_name in rarities if rarities[badge_name][2]==out]
		return _random.choice(possible_out)
	def to_json(self):
		items = [list(x) for x in self.badges.items()]
		for item in items:
			item[1]=[x.to_json() for x in item[1]]
		ret = {item[0]: item[1] for item in items}
		return ret
	@classmethod
	def from_json(cls,d):
		if type(d)==str: d=json.loads(d)
		items = [list(x) for x in d.items()]
		for item in items:
			item[1]=[Badge.from_json(x) for x in item[1]]
		ret = cls()
		ret.badges = {item[0]: item[1] for item in items}
		return ret
