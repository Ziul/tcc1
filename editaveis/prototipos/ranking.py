from apt import Cache
from Levenshtein import ratio

class Pack(object):
	"""docstring for Pack"""
	name = ''
	ratio = 0
	def __init__(self):
		super(Pack, self).__init__()
	def __str__(self):
		return self.name.ljust(50)  + "%.8f".rjust(6) %(self.ratio)
		
def Rankilist_r(pack,cache,peso=0):
	ret = []

	for k in cache:
		if pack in k.name:
			k.ratio += ratio(pack,k.name)+peso

	for i in sorted(cache,key=lambda item: item.ratio,reverse=True):
		ret.append(i)
	return ret

def Rankilist(pack):
	cache = Cache()
	list_app = []
	ret = []

	for k in cache:
		if pack in k.name:
			item = Pack()
			item.name = k.name
			peso = int(ratio(pack,k.name))*2
			item.ratio = ratio(pack,k.name) + peso
			list_app.append(item)

	for i in sorted(list_app,key=lambda item: item.ratio,reverse=True):
		ret.append(i)
	return ret

def Rankilist_hard(pack):
	cache = Cache()
	list_app = []
	ret = []

	for k in cache:
		item = Pack()
		item.name = k.name
		peso = int(ratio(pack,k.name))*2
		item.ratio = ratio(pack,k.name) + peso
		list_app.append(item)

	for i in sorted(list_app,key=lambda item: item.ratio,reverse=True):
		ret.append(i)
	return ret



if __name__ == '__main__':
	from sys import argv
	lista = Rankilist(argv[1])
	lista = Rankilist_r(argv[1]+'-',lista)
	lista = Rankilist_r('-dev',lista)
	lista = Rankilist_r('-core',lista)
	lista = Rankilist_r('-commom',lista)
	#lista = Rankilist_r('lib',lista)
	# Perde a coerencia o resultado
	#lista = Rankilist_r(':i386',lista,peso=0.0001)

	if len(lista) <= 10:
		lista = Rankilist_hard(argv[1])
	for i in lista[:30]:
		print i