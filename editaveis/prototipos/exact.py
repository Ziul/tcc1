# -*- coding: utf-8 -*-
"""
Exact match package
"""

from apt import Cache
import optparse
import swalign
from multiprocessing.pool import ThreadPool as Pool
_MAX_PEERS = 20


class Pack(object):

    """docstring for Pack"""
    name = ''
    ratio = 0

    def __init__(self):
        super(Pack, self).__init__()

    def __str__(self):
        return self.name.ljust(50) + ' ' + str(self.ratio)

    def __gt__(self, other):
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

    def __hash__(self):
        # return self.ratio
        return hash(self.__str__())

    def __len__(self):
        return len(self.name)

_parser = optparse.OptionParser(
    usage="Use with care",
    description="Search packages"
)

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


def _cmp(pack, other):
    return pack.name < other.name


def ThreadExact(k):
    pack = args[0]
    if pack in k:
        item = Pack()
        item.name = k
        item.ratio = 0
        return item
    return None


def ExactMatch(pack):
    cache = Cache()
    if _options.single:
        list_app = []
        for k in cache:
            if pack in k.name:
                item = Pack()
                item.name = k.name
                item.ratio = 0
                list_app.append(item)
        return list_app
    else:
        _pool = Pool(processes=_MAX_PEERS)
        result = _pool.map(ThreadExact, cache._set)
        return result

if __name__ == '__main__':
    (_options, args) = _parser.parse_args()
    package_name = args[0]
    suffixes = ['core', 'dev', 'commom', 'devel']
    prefixes = ['lib']

    _options.suffix = _options.prefix = False

    lista = ExactMatch(package_name)
    if _options.suffix:
        for suffix in suffixes:
            matches = ExactMatch('{}-{}'.format(package_name, suffix))
            lista.extend(matches)
    if _options.prefix:
        for prefix in prefixes:
            matches = ExactMatch('{}{}'.format(prefix, package_name))
            lista.extend(matches)
    if _options.suffix and _options.prefix:
        for suffix in suffixes:
            for prefix in prefixes:
                matches = ExactMatch(
                    '{}{}-{}'.format(prefix, package_name, suffix))
                lista.extend(matches)

    lista = filter(None, lista)
    lista = sorted(lista, cmp=_cmp)
    _options.amount = 300
    for i in lista[:_options.amount]:
        print i

    print '%d itens' % len(lista)
