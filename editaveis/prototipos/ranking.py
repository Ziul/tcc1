# -*- coding: utf-8 -*-
from apt import Cache
from Levenshtein import ratio
import optparse
import time
import asyncio
# from multiprocessing import Pool
from multiprocessing.pool import ThreadPool as Pool


class Pack(object):
    """docstring for Pack"""
    name = ''
    ratio = 0
    def __init__(self):
        super(Pack, self).__init__()
    def __str__(self):
        return self.name.ljust(50)  + "%.8f".rjust(6) %(self.ratio)

    def __gt__(self,other):
        return self.ratio > other.ratio
    def __lt__(self, other):
        return self.ratio < other.ratio
    def __eq__(self, other):
        return self.ratio == other.ratio
    def __le__(self, other):
        return self.ratio <= other.ratio
    def __ge__(self, other):
        return self.ratio >= other.ratio
    def __ne__(self, other):
        return self.ratio != other.ratio

_MAX_PEERS = 20

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
                   default=50
                   )

_parser.add_option("--ratio",
                   dest="ratio",
                   type='float',
                   help="Minimal ratio to print",
                   default=0.0
                   )

_parser.add_option("--multi",
                   dest="single",
                   action="store_false",
                   help="Depraced",
                   default=True
                   )


def ThreadRank(k):
    pack = _args[0]
    item = Pack()
    item.name = k
    item.ratio = ratio(pack,k)
    return item

def Rankilist(pack):
    cache = Cache()
    if _options.single:
        list_app = []
        for k in cache:
            item = Pack()
            item.name = k.name
            item.ratio = ratio(pack,k.name)
            list_app.append(item)
        return list_app
    else:
        _pool = Pool(processes=_MAX_PEERS)
        result = _pool.map(ThreadRank, cache._set)
        return result

if __name__ == '__main__':
    from sys import argv
    (_options, _args) = _parser.parse_args()
    package_name = _args[0]
    suffixes = ['core','dev','commom','devel']
    prefixes = ['lib']
    agora = time.time()

    # loop = asyncio.get_event_loop()
    
    lista = Rankilist( package_name)
    if _options.suffix:
        for suffix in suffixes:
            matches = Rankilist('{}-{}'.format(package_name,suffix))
            lista.extend(matches)
    if _options.prefix:
        for prefix in prefixes:
            matches = Rankilist('{}{}'.format(prefix,package_name))
            lista.extend(matches)
    if _options.suffix and  _options.prefix:
        for suffix in suffixes:
            for prefix in prefixes:
                matches = Rankilist('{}{}-{}'.format(prefix,package_name,suffix))
                lista.extend(matches)

    ultimo = time.time()
    print ultimo-agora
    # for i in sorted(lista,reverse=True)[:_options.amount]:
    #     print i