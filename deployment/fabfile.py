"""
PRODUCTION SITE DEPLOYMENT - cambridgesouthhockeyclub.co.uk

USE WITH CAUTION!!!
===================

Deployment is handled using fabric, 'a Python library and command-line
tool for streamlining the use of SSH for application deployment or
systems administration tasks.'

Ref: http://www.fabfile.org/


These fabric scripts handle the deployment and upgrade of the CSHC site.

Example usage: 'fab update_release:v1.2.0'

(run from the deployment directory on the command line)

NOTE: To rollback a release, you can try this:
fab rollback

but be aware this is untested!
"""

from fabric.api import abort, env, run, lcd, cd, task, local, put
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
RELEASE_FILENAME = 'repo_release'

@task
def update_release(version):
    """ Update the release on the production site."""
    check_not_debug()
    tag_release(version)
    archive_repo()
    upload_release()
    backup_db()
    go_live()
    set_maintenance_mode(True)
    install_dependencies()
    syncdb()
    collectstatic()
    set_maintenance_mode(False)

@task
def check_not_debug():
    """ Check that we're not deploying with DEBUG=True set!"""
    with open('../cshcsite/cshcsite/settings/base.py') as settings_file:
        base_settings = settings_file.read()
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
    """ pip install website dependencies."""
    with cd(env.remote_root):
        run('pip install --user -r repo/requirements/production.txt')

@task
def syncdb():
    """ Calls syncdb - with the --migrate flag"""
    with cd(env.remote_root + "repo/cshcsite"):
        run('python manage.py syncdb --migrate')

@task
def collectstatic():
    """ Collects the static files (on Amazon S3)"""
    with cd(env.remote_root + "repo/cshcsite"):
        run('python manage.py collectstatic --noinput')

@task
def tag_release(version):
    """ Write the specified version string to the version.txt file
        and commit it to GIT.
    """
    with lcd(".."):
        local("echo {0} > version.txt".format(version))
        local("git add version.txt")
        local("git commit -m '{0}'".format(version))
        local("git tag -a {0} -m '{0}'".format(version))

@task
def archive_repo():
    """ Zip up the local repository"""
    with lcd(".."):
        local("git archive --output repo_release.tar master")
        local("bzip2 repo_release.tar")

@task
def upload_release():
    """ Upload the zipped repository"""
    put(local_path='../{0}'.format(RELEASE_FILENAME + '.tar.bz2'), remote_path=env.remote_root)
    with cd(env.remote_root):
        run('mkdir {0}'.format(RELEASE_FILENAME))
        run('tar -jxf {0}.tar.bz2 -C ./{0}'.format(RELEASE_FILENAME))
        run('rm {0}.tar.bz2'.format(RELEASE_FILENAME))
    with lcd(".."):
        local("rm {0}.tar.bz2".format(RELEASE_FILENAME))

@task
def set_maintenance_mode(turn_on):
    """ Sets the MAINTENANCE_MODE flag to True or False in the settings file."""
    with cd(env.remote_root):
        add_or_replace_line('repo/cshcsite/cshcsite/settings/production.py', 'MAINTENANCE_MODE = ',
                            str(turn_on))
        run('touch ~/www.cambridgesouthhockeyclub.co.uk_html/django.fcgi')

@task
def go_live():
    """ Swap in the new release directory for the previous release directory
        and touch the FastCGI script to force the webserver to refresh.
    """
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


# Uncomment the @task line to enable this again (disabled for safety)
#@task
def initial_setup(version):
    """ Initial setup of the production environment."""
    check_not_debug()
    tag_release(version)
    archive_repo()
    upload_release()
    go_live()
    install_dependencies()
    syncdb()
    create_superuser()
    collectstatic()
    import_data()
    set_maintenance_mode(False)

# Uncomment the @task decorator to re-enable this task
#@task
def create_superuser():
    """ Creates the CSHC superuser (using a bespoke Django management command)"""
    with cd(env.remote_root + "repo/cshcsite"):
        run('python manage.py create_cshc_superuser')


# Uncomment the @task decorator to re-enable this task
#@task
def import_data():
    """ Import data from the CSV exports from the old Access database."""
    with cd(env.remote_root + "repo/cshcsite"):
        run('python manage.py data_migration')
        run('python manage.py create_users')
        run('python manage.py import_data --all')
        run('python manage.py import_league_tables')


def add_or_replace_line(filename, pattern, value):
    """ Adds or replaces the given pattern in 'filename' with the supplied value"""
    # Prevent expansion of env vars....
    pattern_find = pattern.replace('$', '\\'+re.escape("$"))
    found = run('grep "^{term}" {target}||echo missing'.format(term=pattern_find, target=filename))
    if found[0:7] != "missing":
        run("sed -i 's/^{term}.*$/{term}".format(term=pattern) + value + "/' " + filename)
    else:
        line = re.escape(pattern) + value
        run("echo " + line + ">>" + filename)
