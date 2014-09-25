# -*- coding: utf-8 -*-
"""
Prototype code

Prototype code to teste apk API

"""

def test_install(package='git'):
    try:
        import yum
    except ImportError as error:
        raise error

    yb=yum.YumBase()
    try:
        yb.repos.doSetup()
    except IOError, e:
        print "Missing privilegies or another root user aready [{err}]".format(
                    err=str(e))
        raise e
    matches = yb.searchGenerator(['name'], package)
    for (pack, matched_value) in matches :
        if pack.name == package : 
            print pack.name
            yb.install(pack)
    yb.buildTransaction()
    yb.processTransaction()

def test(package='git'):
    import yum

    yb = yum.YumBase()
    if yb.rpmdb.searchNevra(name=package):
       print "installed"
    else:
       print "not installed"


if __name__ == '__main__':
    test_install('gedit')
