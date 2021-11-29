#!/usr/bin/python3

#PYTHONPATH=/home/jmracek/Projects/libdnf/build/bindings/python3/

import libdnf

print("ahoj")

#  with libdnf.base.Base() as base: does not work
#  AttributeError: __enter__
base = libdnf.base.Base()
#  Load dnf.conf
base.load_config_from_file()

#  Load vars including arch, basearch and releasever
#  Where to modify a config_path, reposdir, and varsdir according to installroot
base.get_vars().load(base.get_config().installroot().get_value(), base.get_config().varsdir().get_value())

#  Sets path to cache directory. Cannot set a value without providing a priority
#  Not default value, requires autodetection according to user (am_I_root)
base.get_config().cachedir().set(libdnf.conf.Option.Priority_RUNTIME, '/tmp/test/tttttttt')

print(base.get_config().installroot().get_value())
# Read all repository from your system (from dirs in conf.reposdir)
base.get_repo_sack().new_repos_from_dirs()

#  or repository can be defined and added by add_new_repo()
#  repo = base.get_repo_sack().new_repo("new_repo_id")
#  repo_config = repo.get_config()
#  repo_config.baseurl().set(libdnf.conf.Option.Priority_RUNTIME, [dir_path])
#  repo_config.skip_if_unavailable().set(libdnf.conf.Option.Priority_RUNTIME, True)
#  repo.fetch_metadata()
#  repo.load()

#  download metadata for all enabled repositories but without system repository, and load data to solver, apply
#  excludes from configuration, apply modularity filtering
# Loads repository into rpm::Repo.

enabled_repos = libdnf.repo.RepoQuery(base)
enabled_repos.filter_enabled(True)

#  load system repository
base.get_repo_sack().get_system_repo().load()

for repo in enabled_repos:
    repo.get_config().skip_if_unavailable().set(libdnf.conf.Option.Priority_RUNTIME, True);
    repo.fetch_metadata()
    repo.load()

#  find a package in repository, constructor does not return self, therefore I cannot add a filter on the same line
#  query is applied without a delay
query = libdnf.rpm.PackageQuery(base)
query.filter_name(['dnf'])

#  create a copy on applied query (apply() not required) and add one filter with glob cmp type
query1 = libdnf.rpm.PackageQuery(query)
query1.filter_repo_id(['fedora-*', 'updates-*'], libdnf.common.QueryCmp_GLOB)

# To create new transaction you should do a reset first to not try install once again
goal = libdnf.base.Goal(base)

#  Operation is not evaluated until goal.resolve()
goal.add_rpm_install("acpi")
transaction = goal.resolve(False)
print("Transaction to install acpi")
for item in transaction.get_transaction_packages():
    print(item)

#  To create libsolv transaction it is also possible to use lower API.
goal = libdnf.base.Goal(base)
query = libdnf.rpm.PackageQuery(base)
query.filter_name(['dnf'])
goal.add_rpm_install(query)
transaction = goal.resolve(False)

print("Transaction to install dnf using Goal")
for pkg in transaction.get_transaction_packages():
    print(pkg)

