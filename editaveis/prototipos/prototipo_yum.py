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
    try:
        yb.repos.doSetup()
    except IOError, e:
        print "Missing privilegies or another root user aready [{err}]".format(
                    err=str(arg))
        raise e
    matches = yb.searchGenerator(['name'],package)
    for (package, matched_value) in matches :
        if package.name == package : yb.install(package)
    # pl = yb.doPackageLists()
    # if pl.installed:
    #     print "Installed Packages"
    #     for pkg in sorted(pl.installed):
    #         print pkg
    # if (not pl.available) and (not pl.obsoletes):
    #     print "Package %s not Available" % package
    # if pl.available:
    #     print "Available Packages"
    #     for pkg in sorted(pl.available):
    #         print pkg, pkg.repo
    #     if raw_input("\nDo you want to continue? (y/n) ") == 'y':
    #         try:
    #             yb.install(package)
    #         except yum.Errors.InstallError as arg:
    #             print "Missing privilegies or another root user aready [{err}]".format(
    #                 err=str(arg))
    #             raise arg



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
    test_install('git')
