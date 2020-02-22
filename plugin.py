import json, traceback

class Data:
	"""A class for plugin data."""
	def __init__(self,value):
		self.value = value
	def serialize(self):
		return self.value
	def deserialize(self,value):
		self.value = value
	def save(self,filename):
		with open(filename,"w") as f:
			f.write(self.serialize())
	def load(self,filename):
		try:
			with open(filename) as f:
				self.deserialize(f.read())
		except:
			print("Error loading data from {!r}:".format(filename))
			traceback.print_exc()
			pass # You should've initialized this with a sane default, so just keep the default on error
	def __str__(self):
		return str(self.value)
	def __repr__(self):
		return repr(self.value)

class JSONData(Data):
	"""Data, but can be serialized to JSON (and should be)."""
	def serialize(self):
		return json.dumps(self.value)
	def deserialize(self,value):
		self.value = json.loads(value)

class DictData(JSONData):
	def __init__(self,filename):
		JSONData.__init__(self,{})
		self.filename=filename
	def __getitem__(self,k):
		self.load()
		return self.value[k]
	def __setitem__(self,k,v):
		self.value[k]=v
		self.save()
	def load(self):
		super(DictData,self).load(self.filename)
	def save(self):
		super(DictData,self).save(self.filename)
	def get(self,*args,**kwargs):
		self.load()
		return self.value.get(*args,**kwargs)
