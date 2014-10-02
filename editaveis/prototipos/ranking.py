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

import optparse
from multiprocessing import Pool

_parser = optparse.OptionParser(
	usage= "Use with care",
	description="Search packages"
	)

# quiet options
_parser.add_option("--no-suffix",
                   dest="suffix",
                   action="store_false",
                   help="suppres search for suffixes",
                   default=True
                   )
_parser.add_option("--no-prefix",
                   dest="prefix",
                   action="store_false",
                   help="suppres search for prefix",
                   default=True
                   )

_parser.add_option("--amount",
                   dest="amount",
                   type='int',
                   help="How many print",
                   default=10
                   )

_parser.add_option("--ratio",
                   dest="ratio",
                   type='float',
                   help="Minimal ratio to print",
                   default=0.0
                   )


def ThreadRank(pack):
	item = Pack()
	item.name = k.name
	item.ratio = ratio(pack,k.name)
	return item

def Rankilist(cache,pack):
	list_app = []

	for k in cache:
		#if pack in k.name:
		item = Pack()
		item.name = k.name
		item.ratio = ratio(pack,k.name)
		list_app.append(item)
	return list_app
	#_pool = Pool(processes=_MAX_PEERS)
	#result = _pool.map(Threadlist, chapter_urls.items())

if __name__ == '__main__':
	from sys import argv
	(_options, _args) = _parser.parse_args()
	package_name = _args[0]
	cache = Cache()
	suffixes = ['core','dev','commom']
	prefixes = ['lib']
	lista = Rankilist(cache, package_name)
	if _options.suffix:
		for suffix in suffixes:
			matches = Rankilist(cache,'{}-{}'.format(package_name,suffix))
			lista.extend(matches)
	if _options.prefix:
		for prefix in prefixes:
			matches = Rankilist(cache,'{}{}'.format(prefix,package_name))
			lista.extend(matches)
	if _options.suffix and 	_options.prefix:
		for suffix in suffixes:
			for prefix in prefixes:
				matches = Rankilist(cache,'{}{}-{}'.format(prefix,package_name,suffix))
				lista.extend(matches)

	ret=[]
	for i in sorted(lista,key=lambda item: item.ratio,reverse=True):
		ret.append(i)

	for i,k in zip(ret,xrange(0,_options.amount)):
		if i.ratio < _options.ratio:
			break
		print i