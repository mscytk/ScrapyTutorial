# coding: utf-8

def convkks(param):
    from pykakasi import kakasi
    kakasi = kakasi()

    kakasi.setMode('H', 'a')
    kakasi.setMode('K', 'a')
    kakasi.setMode('J', 'a')

    conv = kakasi.getConverter()

    print(type(param))
    print(conv.do(str(param)))