# -*- coding: utf-8 -*-
"""
Prototype code

Prototype code to teste apk API
"""


def test_install(package_name="git"):
    """
    function to test a package installation
    """
    try:
        # from apt.cache import Cache as _
        import apt
        # from apt.cache import LockFailedException
        from apt import progress
    except ImportError as error:
        raise error

    cache = apt.cache.Cache(progress.text.OpProgress())

    try:
        cache.update(progress.base.AcquireProgress())
        cache.open(progress.text.OpProgress())
        pkg = cache[package_name]
    except KeyError:
        print "{pkg_name}  not found".format(pkg_name=package_name)
        return
    except apt.cache.LockFailedException as arg:
        print "Error: {err}".format(err=str(arg))
        return

    if pkg.is_installed:
        print "{pkg_name} already installed".format(pkg_name=package_name)
    else:
        # select to be installed
        pkg.mark_install()

        print "Dependeces from %s to be installed:" % package_name
        print cache.get_changes()[0].name,
        for i in cache.get_changes():
            print i.name,

        if raw_input("\nDo you want to continue? (y/n) ") == 'y':
            try:
                cache.commit(install_progress=progress.base.InstallProgress())
            except apt.cache.LockFailedException as arg:
                print "Error: {err}".format(err=str(arg))
        else:
            cache.clear()

        # library compatibility
        try:
            cache.close()
        except AttributeError as error:
            pass
        print "Leaving"

if __name__ == '__main__':
    test_install('gito')
