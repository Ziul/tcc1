# -*- coding: utf-8 -*-
"""
    Code to rank packages from a search in APT using  Levenshtein
"""
from apt import Cache
from Levenshtein import ratio
from exact import Pack, _parser
from multiprocessing.pool import ThreadPool as Pool

_MAX_PEERS = 20


def Thread_Rank(k):
    pack = _args[0]
    item = Pack()
    item.name = k
    item.ratio = ratio(pack, k)
    return item


def Rankilist(pack):
    cache = Cache()
    if _options.single:
        list_app = []
        for k in cache:
            item = Pack()
            item.name = k.name
            item.ratio = ratio(pack, k.name)
            list_app.append(item)
        return list_app
    else:
        _pool = Pool(processes=_MAX_PEERS)
        result = _pool.map(Thread_Rank, cache._set)
        return result

if __name__ == '__main__':
    (_options, _args) = _parser.parse_args()
    package_name = _args[0]
    suffixes = ['core', 'dev', 'commom', 'devel']
    prefixes = ['lib']

    lista = Rankilist(package_name)
    if _options.suffix:
        for suffix in suffixes:
            matches = Rankilist('{}-{}'.format(package_name, suffix))
            lista.extend(matches)
    if _options.prefix:
        for prefix in prefixes:
            matches = Rankilist('{}{}'.format(prefix, package_name))
            lista.extend(matches)
    if _options.suffix and _options.prefix:
        for suffix in suffixes:
            for prefix in prefixes:
                matches = Rankilist(
                    '{}{}-{}'.format(prefix, package_name, suffix))
                lista.extend(matches)

    # ultimo = time.time()
    lista = list(set(lista))
    lista = sorted(lista, reverse=True)
    for i in lista[:_options.amount]:
        print i
