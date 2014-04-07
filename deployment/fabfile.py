##############################################################################
# PRODUCTION SITE DEPLOYMENT - cambridgesouthhockeyclub.co.uk
#
# USE WITH CAUTION!!!
# ===================
#
# These scripts handle the deployment and upgrade of the CSHC site.

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
    install_dependencies()
    syncdb()
    migrate_db()
    create_superuser()
    collectstatic()
    import_data()
    set_maintenance_mode(False)

@task
def file_update(version):
    tag_release(version)
    archive_repo()
    upload_release()
    go_live()
    set_maintenance_mode(True)
    collectstatic()
    set_maintenance_mode(False)

@task
def update_release(version):
    tag_release(version)
    archive_repo()
    upload_release()
    go_live()
    set_maintenance_mode(True)
    install_dependencies()
    syncdb()
    migrate_db()
    collectstatic()
    set_maintenance_mode(False)

@task
def install_dependencies():
    with cd(env.remote_root):
        run('pip install --user -r repo/requirements/production.txt')

@task
def syncdb():
    with cd(env.remote_root + "repo/cshcsite"):
        run('python manage.py syncdb')

@task
def create_superuser():
    with cd(env.remote_root + "repo/cshcsite"):
        run('python manage.py create_cshc_superuser')

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
        local("echo {0} > version.txt".format(version))
        local("git add version.txt")
        local("git commit -m '{0}'".format(version))
        local("git tag -a {0} -m '{0}'".format(version))

@task
def archive_repo():
    with lcd(".."):
        local("git archive --output repo_release.tar master")
        local("bzip2 repo_release.tar")

@task
def upload_release():
    put(local_path='../{}'.format('repo_release.tar.bz2'), remote_path=env.remote_root)
    with cd(env.remote_root):
        run('mkdir repo_release')
        run('tar -jxf repo_release.tar.bz2 -C ./repo_release')
        run('rm repo_release.tar.bz2')
    with lcd(".."):
        local("rm repo_release.tar.bz2")

@task
def temp():
    with cd(env.remote_root):
        run('mkdir repo_release')
        run('tar -jxf repo_release.tar.bz2 -C ./repo_release')

@task
def set_maintenance_mode(on):
    with cd(env.remote_root):
        _add_or_replace_line('repo/cshcsite/cshcsite/settings/production.py', 'MAINTENANCE_MODE = ', str(on))
        run('touch ~/www.cambridgesouthhockeyclub.co.uk_html/django.fcgi')

@task
def migrate_db():
    with cd(env.remote_root + 'repo/cshcsite/'):
        run('chmod 744 ../deployment/migrate.sh')
        # Make sure we've got linux line endings
        run('fromdos ../deployment/migrate.sh')
        run('../deployment/migrate.sh')

@task
def go_live():
    with cd(env.remote_root):
        run('rm -fr repo_old')
        run('mv repo repo_old')
        run('mv repo_release repo')
        run('touch ~/www.cambridgesouthhockeyclub.co.uk_html/django.fcgi')

def _add_or_replace_line(file, pattern, value):
    # Prevent expansion of env vars....
    pattern_find = pattern.replace('$', '\\'+re.escape("$"))
    found = run('grep "^{term}" {target}||echo missing'.format(term=pattern_find, target=file))
    if found[0:7] != "missing" :
        run("sed -i 's/^{term}.*$/{term}".format(term=pattern) + value + "/' " + file)
    else:
        line = re.escape(pattern) + value
        run("echo " + line + ">>" + file)