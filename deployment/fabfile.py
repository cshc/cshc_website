##############################################################################
# PRODUCTION SITE DEPLOYMENT - cambridgesouthhockeyclub.co.uk
#
# USE WITH CAUTION!!!
# ===================
#
# These scripts handle the deployment and upgrade of the CSHC site.
# Example usage: 'fab update_release:v1.2.0'
# (run from the deployment directory on the command line)
#
# NOTE: To rollback a release, you can try this:
# fab rollback
#
# but be aware this is untested!

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

DB_BACKUP_FILENAME = 'db_backup.sql'

@task
def staging_release():
    local('heroku login')
    local('git push heroku master')
    local('heroku restart')
    # local("heroku run --app cshcsite 'python cshcsite/manage.py syncdb'")
    # local("heroku run --app cshcsite 'chmod 744 deployment/migrate.sh'")
    # # Make sure we've got linux line endings
    # local("heroku run --app cshcsite 'fromdos deployment/migrate.sh'")
    # local("heroku run --app cshcsite 'deployment/migrate.sh'")
    # local("heroku run --app cshcsite 'python cshcsite/manage.py create_cshc_superuser'")
    # local("heroku run --app cshcsite 'python cshcsite/manage.py data_migration'")
    # local("heroku run --app cshcsite 'python cshcsite/manage.py create_users'")
    # local("heroku run --app cshcsite 'python cshcsite/manage.py import_data --all'")
    # local("heroku run --app cshcsite 'python cshcsite/manage.py import_league_tables'")

@task
def initial_setup(version):
    check_not_debug()
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
    check_not_debug()
    tag_release(version)
    archive_repo()
    upload_release()
    go_live()
    set_maintenance_mode(True)
    collectstatic()
    set_maintenance_mode(False)

@task
def update_release(version):
    check_not_debug()
    tag_release(version)
    archive_repo()
    upload_release()
    backup_db()
    go_live()
    set_maintenance_mode(True)
    install_dependencies()
    syncdb()
    migrate_db()
    collectstatic()
    set_maintenance_mode(False)

@task
def check_not_debug():
    with open('../cshcsite/cshcsite/settings/base.py') as f:
        base_settings = f.read()
        if "DEBUG = True" in base_settings:
            abort("You must set 'DEBUG = False' in cshcsite/settings/base.py before deploying")

@task
def backup_db():
    """ Backs up the database at the point of upgrade. Might be useful if we
        ever need to downgrade. Note that the username and password are stored
        in ~/.my.cnf to avoid you needing to enter them here.
    """
    with cd(env.remote_root + 'repo'):
        run('mysqldump -h mysql-51.int.mythic-beasts.com cshc > {}'.format(DB_BACKUP_FILENAME))

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

@task
def rollback():
    """ Attempts to rollback the release to the previous release.

        The previous release is stored on the server at ~/new_site/repo_old
        The MySQL database backup is located at ~/new_site/repo_old/<DB_BACKUP_FILENAME>
    """
    with cd(env.remote_root):
        # Reinstate the previous release's files
        run('mv repo_old repo_working')
        run('mv repo repo_old')
        run('mv repo_working repo')
        # Now rollback the database
        run('chmod 744 repo/deployment/restore_db.sh')
        # This script drops all tables from the database and then
        # restores the database using the mysqldump from the previous release
        run('./repo/deployment/restore_db.sh repo/{}'.format(DB_BACKUP_FILENAME))

def _add_or_replace_line(file, pattern, value):
    # Prevent expansion of env vars....
    pattern_find = pattern.replace('$', '\\'+re.escape("$"))
    found = run('grep "^{term}" {target}||echo missing'.format(term=pattern_find, target=file))
    if found[0:7] != "missing" :
        run("sed -i 's/^{term}.*$/{term}".format(term=pattern) + value + "/' " + file)
    else:
        line = re.escape(pattern) + value
        run("echo " + line + ">>" + file)