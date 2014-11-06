from apt import Cache
import optparse
import time
import swalign
from ranking import Pack,_parser
from math import fabs
from multiprocessing.pool import ThreadPool as Pool
_MAX_PEERS = 20

def _cmp(x, y):
  if x.ratio[0] == y.ratio[0]:
    if x.ratio[1] == y.ratio[1]:
      if x.ratio[2] == y.ratio[2]:
        if x.ratio[3] == y.ratio[3]:
          return 0
        elif x.ratio[3] < y.ratio[3]:
          return -1
        else:
          return 1
      elif x.ratio[2] < y.ratio[2]:
        return -1
      else:
        return 1
    elif x.ratio[1] < y.ratio[1]:
      return 1
    else:
      return -1
  elif x.ratio[0] < y.ratio[0]:
    return -1
  else:
    return 1

def ThreadAlign(k):
    pack = _args[0]
    item = Pack()
    item.name = k
    alinhamento = sw.align(pack,k)
    item.ratio = (alinhamento.mismatches + fabs(len(pack)-len(k)) - alinhamento.matches) + len(pack)
    return item

def Alinhamento(pack):
    cache = Cache()
    if _options.single:
        list_app = []
        for k in cache:
            item = Pack()
            item.name = k.name
            alinhamento = sw.align(pack,k.name)
            item.ratio = [alinhamento.matches, fabs(len(pack)-len(k.name)),alinhamento.score, alinhamento.mismatches] 
            list_app.append(item)
        return list_app
    else:
        _pool = Pool(processes=_MAX_PEERS)
        result = _pool.map(ThreadAlign, cache._set)
        return result

if __name__ == '__main__':
    (_options, _args) = _parser.parse_args()
    package_name = _args[0]
    suffixes = ['core','dev','commom','devel']
    prefixes = ['lib']
    agora = time.time()

    match = 2
    mismatch = -1
    scoring = swalign.NucleotideScoringMatrix(match, mismatch)
    sw = swalign.LocalAlignment(scoring)

    _options.suffix = _options.prefix = False

    lista = Alinhamento( package_name)
    if _options.suffix:
        for suffix in suffixes:
            matches = Alinhamento('{}-{}'.format(package_name,suffix))
            lista.extend(matches)
    if _options.prefix:
        for prefix in prefixes:
            matches = Alinhamento('{}{}'.format(prefix,package_name))
            lista.extend(matches)
    if _options.suffix and  _options.prefix:
        for suffix in suffixes:
            for prefix in prefixes:
                matches = Alinhamento('{}{}-{}'.format(prefix,package_name,suffix))
                lista.extend(matches)

    # ultimo = time.time()
    lista =list(set(lista))
    lista = sorted(lista,reverse=True,cmp=_cmp)
    ultimo = time.time()
    print "{} segundos".format(ultimo-agora)
    for i in lista[:_options.amount]:
        print i