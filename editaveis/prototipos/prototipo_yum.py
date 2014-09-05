# -*- coding: utf-8 -*-
"""
Prototype code

Prototype code to teste apk API

"""

def test_install(package='git'):
    try:
        import yum
        from yum.updateinfo import update_minimal
    except ImportError as error:
        raise error

    yb=yum.YumBase()
    yb.repos.doSetup()
    pl = yb.doPackageLists(patterns=package)


# yb = yum.YumBase()
# yb.conf.cache = os.geteuid() != 1
# pl = yb.doPackageLists(patterns=sys.argv[1:])
# if pl.installed:
#     print "Installed Packages"
#     for pkg in sorted(pl.installed):
#         print pkg
# if pl.available:
#     print "Available Packages"
#     for pkg in sorted(pl.available):
#         print pkg, pkg.repo
# if pl.reinstall_available:
#     print "Re-install Available Packages"
#     for pkg in sorted(pl.reinstall_available):
#         print pkg, pkg.repo
# if (not pl.available) and (not pl.obsoletes):
#   print "Package not Available"

# import yum

# yb=yum.YumBase()
# searchlist=['name']
# arg=['gedit']
# matches = yb.searchGenerator(searchlist,arg)
# for (package, matched_value) in matches :
#     if package.name == 'gedit' : yb.install(package)
#     yb.buildTransaction()
#     yb.processTransaction()


if __name__ == '__main__':
    test_install('gito')
