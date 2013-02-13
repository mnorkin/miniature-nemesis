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
  local('python2 manage.py test morbid')

def reset_permissions():
  sudo('chown %s -R %s' %(env.deploy_user, env.code_root_parent))
  sudo('chgrp %s -R %s' %(env.deploy_user, env.code_root_parent))

def create_user():
  require('deploy_user', provided_by=[environment])

  admin_group = 'wheel'
  sudo('addgroup %s' %(admin_group))
  sudo('')

def setup():
  """
  Setup fresh virtualenv, dirs and run full deploy
  """
  require('hosts', provided_by=[environment])
  require('code_root')
  sudo('apt-get upgrade')
  sudo('apt-get -y update')

  sudo('apt-get install -y python-setuptools')
  sudo('easy_install pip')
  sudo('pip install virtualenv')
  sudo('apt-get install -y nginx') # Web server
  sudo('apt-get install -y postgresql') # Database
  sudo('apt-get install -y git-core')

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
  install_requirements()
  upload_tar_from_git(env.whole_path)
  symlink_current_release()

  restart_webserver()

def upload_tar_from_git(path):
  require('release', provided_by=[environment])
  require('whole_path', provided_by=[environment])
  "Create an archive from the current git version and upload it to the server"
  local('git archive --format=tar master | gzip > %s.tar.gz' %(env.release))
  sudo('mkdir -p %s' %(path))
  put('%s.tar.gz' %(env.release), '/tmp', mode=0755)
  sudo('mv /tmp/%s.tar.gz %s/packages/' %(env.release, env.code_root))

  sudo('cd %s && tar zxf ../../../packages/%s.tar.gz' %(env.whole_path, env.release))
  sudo('chown %s -R %s'% (env.user,env.whole_path))
  sudo('chgrp %s -R %s'% (env.user,env.whole_path))
  local('rm %s.tar.gz'% (env.release))

def install_requirements():
  "Install requirements of the app"
  require('release', provided_by=[environment])
  require('whole_path', provided_by=[environment])
  sudo('cp %s; pip install -r %s/requirements.txt' %(env.code_root, env.whole_path))
  reset_permissions()

def symlink_current_release():
  "Symlink current release"
  require('relase', provided_by=[environment])
  sudo('cd %s; ln -s %s releases/current; chown %s -R releases/current; chgrp %s -R releases/current' %(env.code_root, env.release, env.user, env.user))

def install_site():
  # TODO
  pass

def commit():
  local('git add -p && git commit')

def push():
  local('git push')

def prepare_deploy():
  test()
  commit()
  push()

def start_webserver():
  "Start webserver server"
  sudo("nginx -s start")

def restart_webserver():
  "Restart web server"
  sudo("nginx -s reload");