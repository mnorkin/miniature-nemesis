from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files, console
from fabric import utils
from fabric.operations import *

# Configuration
env.project_name = 'morbid'

def environment():
  env.user = 'root'
  env.hosts = ['185.5.55.178']
  env.deploy_user = 'root'
  env.version = 1
  env.release = env.version
  # Virtualenv path root
  env.code_root = '/var/www/targetprice'
  # Activation of virtual env
  env.activate = 'source %s/bin/activate' %(env.code_root)
  env.code_root_parent = '/var/www'
  env.whole_path = '%s/releases/%s/%s' %(env.code_root, env.release, env.project_name)
  env.code_path_symlinked = '%s/releases/current/%s' %(env.code_root, env.project_name)

def virtualenv(command):
  with cd(env.code_root):
    sudo(env.activate + '&&' + command, user=env.deploy_user)

# Tasks
def test():
  # "Run tests"
  local('./manage.py test morbid')

def reset_permissions():
  sudo('chown %s -R %s' %(env.deploy_user, env.code_root_parent))
  sudo('chgrp %s -R %s' %(env.deploy_user, env.code_root_parent))

def create_group():
  env.user = 'root'

  # Create a new group
  wheel_group = 'wheel'
  runcmd('addgroup {group}'.format(group=wheel_group))
  runcmd('echo "%{group} ALL=(ALL) ALL" >> /etc/sudoers'.format(group=wheel_group))

def create_user(wheel_username, wheel_password):
  env.user = 'root'

  wheel_group = 'wheel'

  # Create a new user
  runcmd('adduser {username} --disabled-password --gecos ""'.format(username=wheel_username))
  runcmd('adduser {username} {group}'.format(username=wheel_username,group=wheel_group))

  # Set the password
  runcmd('echo "{username}:{password}" | chpasswd'.format(username=wheel_username, password=wheel_password))

def setup():
  """
  Setup fresh virtualenv, dirs and run full deploy
  """
  require('hosts', provided_by=[environment])
  require('code_root')
  # sudo('apt-get upgrade')
  # sudo('apt-get -y update')

  # sudo('apt-get install -y python-setuptools')
  # sudo('easy_install pip')
  # sudo('pip install virtualenv')
  # sudo('apt-get install -y nginx') # Web server
  # sudo('apt-get install -y postgresql') # Database
  # sudo('apt-get install -y postgresql-contrib') # Database
  # sudo('apt-get install -y postgresql-client') # Database
  # sudo('apt-get install -y git-core')
  # sudo('apt-get install -y libpq-dev python-dev')
  # sudo('apt-get install -y python2.7-dev')
  sudo('apt-get install -y libpq-dev')

  # Additional future configurations
  sudo('mkdir -p %s; cd %s; virtualenv .;source ./bin/activate' %(env.code_root, env.code_root))
  sudo('cd %s; mkdir releases; mkdir shared; mkdir packages;' %(env.code_root))

  reset_permissions()
  deploy()

def deploy():
  """
  Deployment of the app
  * Installs all the dependencies
  * Virtual hosts
  * Restarts the web server
  """
  require('hosts', provided_by=[environment])
  require('whole_path', provided_by=[environment])
  require('code_root')
  upload_tar_from_git(env.whole_path)
  install_requirements()
  symlink_current_release()
  start_webserver()

def small_deploy():
  require('hosts', provided_by=[environment])
  require('whole_path', provided_by=[environment])
  require('code_root')
  upload_tar_from_git(env.whole_path)
  symlink_current_release()
  start_webserver()

def upload_tar_from_git(path):
  require('release', provided_by=[environment])
  require('whole_path', provided_by=[environment])
  "Create an archive from the current git version and upload it to the server"
  local('git archive --format=tar master | gzip > %s.tar.gz' %(env.release))
  sudo('mkdir -p %s' %(path))
  put('%s.tar.gz' %(env.release), '/tmp', mode=0755)
  sudo('mv /tmp/%s.tar.gz %s/packages/' %(env.release, env.code_root))

  sudo('cd %s && tar zxf ../../../packages/%s.tar.gz' %(env.whole_path, env.release))
  sudo('cp %s/nginx.conf /etc/nginx/sites-enabled/default' %(env.whole_path))
  sudo('chown %s -R %s'% (env.user,env.whole_path))
  sudo('chgrp %s -R %s'% (env.user,env.whole_path))
  local('rm %s.tar.gz'% (env.release))

def install_requirements():
  "Install requirements of the app"
  require('release', provided_by=[environment])
  require('whole_path', provided_by=[environment])
  sudo('cd %s; virtualenv .;source ./bin/activate; export PATH=/usr/bin:"$PATH"; pip install -r %s/requirements.txt' %(env.code_root, env.whole_path))
  reset_permissions()

def symlink_current_release():
  "Symlink current release"
  require('release', provided_by=[environment])
  sudo('cd %s; ln -s %s releases/current; chown %s -R releases/current; chgrp %s -R releases/current' %(env.code_root, env.release, env.user, env.user))
  put('nginx.conf', '/etc/nginx/sites-enabled/default')
  virtualenv('cd %s; chmod +x releases/current/%s/deamon.py' %(env.code_root, env.project_name))
  virtualenv('cd %s; mv releases/current/%s/prototype/settings.py releases/current/%s/prototype/settings_local.py' %(env.code_root, env.project_name, env.project_name))
  virtualenv('cd %s; mv releases/current/%s/prototype/settings_dev.py releases/current/%s/prototype/settings.py' %(env.code_root, env.project_name, env.project_name))
  """Make executable"""

def start_webserver():
  "Start webserver server"
  sudo("nginx -s reload")
  virtualenv('%s/releases/current/%s/manage.py syncdb' %(env.code_root, env.project_name))
  virtualenv('%s/releases/current/%s/manage.py collectstatic' %(env.code_root, env.project_name))
  virtualenv('%s/releases/current/%s/deamon.py start >> /tmp/gunicorn.log' %(env.code_root, env.project_name))
  """Launch deamon"""

def restart_webserver():
  "Restart web server"
  sudo("nginx -s reload");