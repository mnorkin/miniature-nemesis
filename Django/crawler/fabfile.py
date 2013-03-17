from fabric.api import *
from fabtic.operations import *
import datetime

env.project_name = 'crawler'


def environment():
    env.user = 'root'
    env.hosts = ['185.5.55.178']
    env.deploy_user = 'agurkas'
    env.version = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    env.release = env.version
    env.code_root = '/var/www/crawler'
    env.activate = 'source %s/bin/activate' % env.code_root
    env.code_root_parent = '/var/www'
    env.whole_path = '%s/releases/%s/%s' % (env.code_root, env.release, env.project_name)
    env.code_path_symlinked = '%s/releases/current/%s' % (env.code_root, env.project_name)


def virtualenv(command):
    """
    Virtualenv `sub shell`
    """
    with cd(env.code_root):
        runcmd(env.activate + '; ' + command, user=env.deploy_user)


def test():
    """
    Testing part
    """
    local('./manage.py test crawler')


def reset_permissions():
    """
    Resetting the permissions of the trivial paths
    """
    sudo('chown %s -R %s' % (env.deploy_user, env.code_root_parent))
    sudo('chgrp %s -R %s' % (env.deploy_user, env.code_root_parent))


def setup():
    """
    Full setup of the system
    """
    require('hosts', provided_by=[environment])
    require('code_root')

    runcmd('mkdir -p %s' % (env.code_root))
    virtualenv('mkdir releases; mkdir shared; mkdir packages')

    reset_permissions()
    deploy()


def deploy():
    """
    Deployment of the app
    """
    require('hosts', provided_by=[environment])
    require('whole_path', provided_by=[environment])
    require('code_root')
    update_tar_from_git(env.whole_path)
    install_requirements()
    symlink_current_release()
    restart_webserver()


def update():
    """
    Small, tiny update of the system
    """
    require('hosts', provided_by=[environment])
    require('whole_path', provided_by=[environment])
    require('code_root')
    update_tar_from_git(env.whole_path)
    install_requirements()
    symlink_current_release()
    restart_webserver()


def upload_tar_from_git(path):
    """
    Making an archive and upload it to the host
    """
    require('release', provided_by=[environment])
    require('whole_path', provided_by=[environment])
    local('git archive --format=tar master | gzip > %s.tar.gz' % env.release)
    runcmd('mkdir -p %s' % path)
    put('%s.tar.gz' % env.release, '/tmp', mode=0755)
    runcmd('mv /tmp/%s.tar.gz %s/packages/' % (env.release, env.code_root))
    runcmd('cd %s && tar zxf ../../../packages/%s.tar.gz' % (env.whole_path, env.release))
    local('rm %s.tar.gz' % env.release)
    reset_permissions()


def install_requirements():
    """
    Installation of the requirements of the application
    """
    require('release', provided_by=[environment])
    require('whole_path', provided_by=[environment])
    virtualenv('export PATH=/usr/bin:$PATH')
    virtualenv('pip install -r %s/requirements.txt' % env.whole_path)
    reset_permissions()


def symlink_current_release():
    """
    Linking the current release
    """
    require('release', provided_by=[environment])
    symlink_path = '%s/releases/current' % env.code_root

    if not files.exists(symlink_path):
        with cd(env.code_root):
            runcmd('ln -s %s/ releases/current' % env.release)
    else:
        with cd(env.code_root):
            runcmd('ln -nsf %s/ releases/current' % env.release)

    with cd(env.code_root):
        runcmd('chown %s -R releases/current' % env.deploy_user)
        runcmd('chgrp %s -R releases/current' % env.deploy_user)

    with cd(env.code_root + '/releases/current'):
        runcmd('chmod +x %s/daemon.py' % env.project_name)
        # Set the appropriate permissions to launch the daemon
        runcmd(
            'mv %s/crawler/settings.py %s/crawler/settings_local.py' %
            (env.project_name, env.project_name))
        # Rename the development version of settings as local
        runcmd(
            'mv %s/crawler/settings_dev.py %s/crawler/settings.py' %
            (env.project_name, env.project_name))
        # Rename the server settings to the current settings


def restart_webserver():
    """
    Restarting web server
    """
    stop_webserver()
    start_webserver()


def stop_webserver():
    """
    Stopping the web server
    """
    deamon_root = "%s/releases/current/%s/deamon.py" % (
        env.code_root, env.project_name)
    if files.exists(deamon_root):
        virtualenv(
            '%s/releases/current/%s/deamon.py stop' %
            (env.code_root, env.project_name))


def start_webserver():
    """
    Start web server deamon.

    Additional work:
    * Syncing database
    * Collecting static files
    """
    project_path = '%s/releases/current/%s' % (env.code_root, env.project_name)
    virtualenv('%s/manage.py syncdb --noinput' % project_path)
    virtualenv('%s/manage.py collectstatic --noinput' % project_path)
    virtualenv('%s/deamon.py start; sleep 2' % project_path)
