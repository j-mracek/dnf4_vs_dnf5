#!/usr/bin/python3

import dnf

#  initialize Base with a default configuration including cachedir and detect releasever in '/', arch, basearch
with dnf.base.Base() as base:

    #  Load dnf.conf
    base.conf.read(priority=dnf.conf.PRIO_MAINCONFIG)

    #  Load vars
    base.conf.substitutions.update_from_etc(base.conf.installroot, varsdir=base.conf.varsdir)

    # Sets path to cache directory with default priority RUNTIME.
    base.conf.cachedir = '/tmp/test1/ttttttt3'
    #  Setting other then default priority not possible by API
    #  conf._set_value('debuglevel', level, dnf.conf.PRIO_RUNTIME)

    # Read all repository from your system (from dirs in conf.reposdir)
    base.read_all_repos()

    # or repository can be defined and added by add_new_repo()
    # repo = base.repos.add_new_repo("<repoid>", base.conf, baseurl=[dir_path], skip_if_unavailable=True)

    #  download metadata for all enabled repositories but without system repository, and load data to solver, apply
    #  excludes from configuration, apply modularity filtering
    base.fill_sack(load_system_repo=False)

    #  find a package in repository
    #  query and filters are applied lazily
    query = base.sack.query().filterm(name='dnf')
    #  dnf.query.Query(base.sack)

    #  create a copy on applied query and add one filter
    query.apply()
    #  required for performance improvement
    query1 = query.filter(reponame__glob=['fedora-*', 'updates-*'])
    print("Packages with name dnf")
    for pkg in query:
        print(pkg)

    # Raises an error when `acpi` is not available
    base.install("acpi")
    base.resolve()
    print("Transaction to install acpi")
    for item in base.transaction:
        print(item)

    #  To create libsolv transaction it is also possible to use lower API.
    goal = dnf.goal.Goal(base.sack)
    query = base.sack.query().filterm(name='dnf')
    sltr = dnf.selector.Selector(base.sack)
    sltr.set(pkg=query)
    goal.install(select=sltr, optional=False)  #  It will pick one package (the best candidate) to install from query
    goal.run(allow_uninstall=False, force_best=base.conf.best,
             ignore_weak_deps=(not base.conf.install_weak_deps))
    print("Transaction to install dnf using Goal")
    for pkg in goal.list_installs():
        print(pkg)

    #  plugins
