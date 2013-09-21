##############################################################################
# PRODUCTION SITE DEPLOYMENT - cambridgesouthhockeyclub.co.uk
#
# USE WITH CAUTION!!!
# ===================
#
# This script does the following:
#    1. Updates the version.txt file based on the major/minor command line
#       argument and commits it to the Git repository.
#    2. Tags the current Git revision with the version number from version.txt
#    3.

from fabric.api import *
import os
import re

def _get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        abort("Set the %s env variable" % setting)

env.hosts = ['sphinx.mythic-beasts.com']
env.user = _get_env_setting('MYTHIC_BEASTS_SSH_USER')
env.password = _get_env_setting('MYTHIC_BEASTS_SSH_PASSWORD')
env.remote_root = '~/new_site/'

@task
def initial_setup(version):
    tag_release(version)
    archive_repo()
    upload_release()
    go_live()
    syncdb()
    migrate_db()
    collectstatic()
    import_data()

@task
def update_release(version):
    tag_release(version)
    archive_repo()
    upload_release()
    set_maintenance_mode(True)
    syncdb()
    migrate_db()
    collectstatic()
    import_data()

@task
def syncdb():
    with cd(env.remote_root + "repo/cshcsite"):
        run('python manage.py syncdb')

@task
def collectstatic():
    with cd(env.remote_root + "repo/cshcsite"):
        run('python manage.py collectstatic --noinput')

@task
def import_data():
    with cd(env.remote_root + "repo/cshcsite"):
        run('python manage.py data_migration')
        run('python manage.py create_users')
        run('python manage.py import_data --all')
        run('python manage.py import_league_tables')


@task
def tag_release(version):
    with lcd(".."):
        local("git tag -a {0} -m 'Release {0}'".format(version))

@task
def archive_repo():
    with lcd(".."):
        local("git archive --output repo_release.tar master")
        local("bzip2 repo_release.tar")

@task
def upload_release():
    put(local_path='../{}'.format('repo_release.tar.bz2'), remote_path=env.remote_root)
    with cd(env.remote_root):
        run('tar -jxf repo_release.tar.bz2')

@task
def set_maintenance_mode(on):
    print "Value = {}".format(on)
    with cd(env.remote_root):
        _add_or_replace_line('repo/cshcsite/cshcsite/settings/production.py', 'MAINTENANCE_MODE = ', on)

@task
def migrate_db():
    with cd(env.remote_root + 'repo/cshcsite/'):
        run('chmod 744 ../deployment/migrate.sh')
        run('../deployment/migrate.sh')

@task
def go_live():
    with cd(env.remote_root):
        run('rm -fr repo_old')
        run('mv repo repo_old')
        run('mv repo_release repo')

def _add_or_replace_line(file, pattern, value):
    # Prevent expansion of env vars....
    pattern_find = pattern.replace('$', '\\'+re.escape("$"))
    found = run('grep "^{term}" {target}||echo missing'.format(term=pattern_find, target=file))
    if found[0:7] != "missing" :
        run("sed -i 's/^{term}.*$/{term}".format(term=pattern) + value + "/' " + file)
    else:
        line = re.escape(pattern) + value
        run("echo " + line + ">>" + file)