from datetime import datetime
from fabric.api import *

# One single fabric to rule them all

env.project_name = 'target_price'
env.private_hosts = ['109.235.69.232']
env.public_hosts = ['185.5.55.178']
env.directory = ''
env.deploy_group = 'square_wheel'
env.deploy_user = 'agurkas'
env.deploy_pass = 'Tutatru3'

# Local directory part
env.model_path = 'model/'
env.crawler_path = 'crawler/'
env.crawler_daily_path = 'crawler_daily'
env.django_production_path = 'Django/prototype'
env.django_sink_path = 'Django/crawler'

# Remote directory part
env.deploy_model_path = '/home/%(deploy_user)/model' % (
    dict(deploy_user=env.deploy_user)
)
env.deploy_crawler_path = '/home/%(deploy_user)/crawler' % (
    dict(deploy_user=env.deploy_user)
)
env.deploy_crawler_daily_path = '/home/%(deploy_user)/crawler_daily' % (
    dict(deploy_user=env.deploy_user)
)
env.deploy_django_production_path = '/var/www/dev2_targetprice'
env.deploy_django_sink_path = '/var/www/cra_targetprice'

# Release part
env.release = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
env.release_model = 'model_' + env.release
env.release_crawler = 'crawler_' + env.release
env.release_crawler_daily = 'crawler_daily_' + env.release
env.release_django_production = 'django_production_' + env.release
env.release_django_sink = 'django_sink_' + env.release


def virtualenv(command):
    """
    Virtual environment command garden
    """
    with cd(env.directory):
        sudo(
            env.activate + ' && ' + command,
            user=env.deploy_user
        )


def set_root_user():
    """
    Setting up as root user
    """
    env.user = 'root'


def set_deploy_user():
    """
    Setting up as deploy user
    """
    env.user = env.deploy_user


def setup_deploy_user():
    """
    Create an account for an deploy user to access the server
    """
    opts = dict(
        deploy_user=env.deploy_user,
        deploy_password=env.deploy_pass
    )
    # Create user
    sudo('egrep %(deploy_user)s /etc/passwd || adduser %(deploy_user)s --disable-password --gecos ""' % opts)

    # Add public key for ssh access
    if not exists('/home/%(deploy_user)s/.ssh' % opts):
        sudo('mkdir /home/%(deploy_user)s/.ssh' % opts)

    opts['pub'] = prompt("Enter %(deploy_user)s's publ;ic key: " % opts)
    sudo("echo '%(pub)s' > /home/%(deploy_user)s/.ssh/authorized_keys" % opts)

    # Allow this user in sshd_config
    append(
        '/etc/ssh/sshd_config',
        'AllowUsers %(deploy_user)s@*' % opts,
        use_sudo=True)

    # Allow sudo for maintenance user by adding it to 'sudo' group
    sudo('gpasswd -a %(deploy_user)s sudo' % opts)

    # Set the default password for initial login
    sudo('echo "%(deploy_user)s:%(deploy_password)s" | chpasswd' % opts)


def private_setup_deploy_user():
    """
    Settup up private hosts deploy user
    """
    set_root_user()
    env.hosts = env.private_hosts
    setup_deploy_user()


def public_setup_deploy_user():
    """
    Setting up public hosts deploy user
    """
    set_root_user()
    env.hosts = env.public_hosts
    setup_deploy_user()


def disable_root_login():
    """
    Securing
    """
    # Disable password authentication
    sed('/etc/ssh/sshd_config',
        '#PasswordAuthentication yes',
        'PasswordAuthentication no')
    # Deny root login
    sed('/etc/ssh/ssh_config',
        'PermitRootLogin yes',
        'PermitRootLogin no',
        use_sudo=True)
    # Lock out root user
    sudo('passwd --lock root')


def private_disable_root_login():
    """
    Private hosts disable root
    """
    set_root_user()
    env.hosts = env.private_hosts
    disable_root_login()


def public_disable_root_login():
    """
    Public hosts disable root
    """
    set_root_user()
    env.hosts = env.private_hosts
    disable_root_login()


def install_nginx():
    """
    Installing nginx server
    """
    sudo('add-apt-repository ppa:nginx/stable')
    sudo('apt-get update')
    sudo('apt-get -yq install nginx')


def public_install_nginx():
    env.hosts = env.public_hosts
    install_nginx()


def install_postgres():
    """Install and configure Postgresql database server."""
    sudo('apt-get -yq install postgresql libpq-dev')
    configure_postgres()
    initialize_postgres()


def configure_postgres():
    """
    Upload Postgres configuration from ``etc/`` and restart the server.
    """

    version = sudo("psql --version | grep -ro '[8-9].[0-9]'")
    conf_dir_prefix = "/etc/postgresql/%s/" % version

    # pg_hba.conf
    comment('/etc/postgresql/%s/main/pg_hba.conf' % version,
            'local   all         postgres                          ident',
            use_sudo=True)
    sed('/etc/postgresql/%s/main/pg_hba.conf' % version,
        'local   all         all                               ident',
        'local   all         all                               md5',
        use_sudo=True)

    # postgres.conf
    uncomment(
        conf_dir_prefix + 'main/postgresql.conf',
        '#autovacuum = on',
        use_sudo=True
    )
    uncomment(
        conf_dir_prefix + 'main/postgresql.conf',
        '#track_activities = on',
        use_sudo=True
    )
    uncomment(
        conf_dir_prefix + 'main/postgresql.conf',
        '#track_counts = on',
        use_sudo=True
    )
    sed(conf_dir_prefix + 'main/postgresql.conf',
        "#listen_addresses",
        "listen_addresses",
        use_sudo=True)

    # restart server
    sudo(
        '/etc/init.d/postgresql-%s restart || /etc/init.d/postgresql restart' %
        version
    )


def initialize_postgres():
    """
    Initialize the main database.
    """

    version = sudo("psql --version | grep -ro '[8-9].[0-9]'")
    conf_dir_prefix = "/etc/postgresql/%s/" % version

    # temporarily allow root access from localhost
    sudo('mv /etc/postgresql/%s/main/pg_hba.conf /etc/postgresql/%s/main/pg_hba.conf.bak' % (version, version))
    sudo('echo "local all postgres ident" > /etc/postgresql/%s/main/pg_hba.conf' % version)
    sudo('cat /etc/postgresql/%s/main/pg_hba.conf.bak >> /etc/postgresql/%s/main/pg_hba.conf' % (version, version))
    sudo('service postgresql-%s restart || /etc/init.d/postgresql restart ' % (version))

    # set password
    password = prompt('Enter a new database password for user `postgres`:')
    sudo('psql template1 -c "ALTER USER postgres with encrypted password \'%s\';"' % password, user='postgres')

    # configure daily dumps of all databases
    with mode_sudo():
        dir_ensure('/var/backups/postgresql', recursive=True)
    sudo("echo 'localhost:*:*:postgres:%s' > /root/.pgpass" % password)
    sudo('chmod 600 /root/.pgpass')
    sudo("echo '0 7 * * * pg_dumpall --username postgres --file /var/backups/postgresql/postgresql_$(date +%%Y-%%m-%%d).dump' > /etc/cron.d/pg_dump")

    # remove temporary root access
    comment(
        '/etc/postgresql/%s/main/pg_hba.conf' % version,
        'local all postgres ident', use_sudo=True)
    sudo('service postgresql%s restart \
        || /etc/init.d/postgresql restart' % version)


def private_install_postgresql():
    env.hosts = private_hosts
    install_postgres()


def install_python():
    """
    Setting up all the python 2.7
    """
    # Python 2.6 is already installed by default, we just add compile headers
    sudo('apt-get -yq install python python-setuptools')

    # install Distribute
    sudo('curl -O http://python-distribute.org/distribute_setup.py')
    sudo('python2.7 distribute_setup.py')
    sudo('rm -f distribute*')

    # install virtualenv
    sudo('easy_install-2.7 virtualenv')


def private_install_python():
    env.hosts = private_hosts
    install_python()


def install_system_libs():
    sudo('apt-get update')
    sudo('apt-get -yq install curl \
        python-software-properties \
        tar \
        build-essential')


def private_install_system_libs():
    env.hosts = private_hosts


def private_setup():
    """
    Full setup for the private server
    """
    # set_root_user()
    # Firstly, create a user
    private_setup_deploy_user()
    # Disable root ssh login
    # private_disable_root_login()
    private_install_python()
    private_install_postgresql()


def archive_git_and_put(opts):
    """
    Git archive matters
    """
    local('cd %(what_to_send_path)s && \
        git archive --format=tar master | gzip > %(release)s.tar.gz' % opts)
    opts['deploy_path'] = '%(deploy_path)s/releases/%(release)s' % opts
    run('mkdir -p %(deploy_path)s' % opts)
    put('%(release)s.tar.gz' % opts, '/tmp', mode=0755)
    run('mv /tmp/%(release)s.tar.gz %(deploy_path)s/packages/' % opts)
    run('cd %(deploy_path)s/releases/%(release)s/ \
        && tar zxf ../../packages/%(release)s.tar.gz' % opts)
    local('rm %(what_to_send_path)s/%(release)s.tar.gz' % opts)
    # Updating or creating the current release



def install_requirements(opts):
    run('cd %(deploy_path)s; virtualenv .; source ./bin/activate;\
        export PATH=/usr/bin:"$PATH";\
        pip install -r %(deploy_path)s/releases/current/requirements.txt' % opts)


def restart_deamon(opts):
    deamon_root = '%(deploy_path)s/releases/%(release)s/deamon.py' % opts
    if files.exists(deamon_root):
        run('%(deploy_path)s/releases/%(release)s/deamon.py stop; \
            sleep 2' % opts)
        run('%(deploy_path)s/releases/%(release)s/deamon.py start; \
            sleep 2' % opts)


def model_update():
    opts = dict(
        what_to_send_path=env.model_path,
        release=env.release_model,
        deploy_path=env.deploy_model_path
    )
    env.hosts = env.private_hosts
    archive_git_and_put(opts)
    restart_deamon(opts)


def model_deploy():
    env.hosts = env.private_hosts
    opts = dict(
        what_to_send_path=env.model_path,
        release=env.release_model,
        deploy_path=env.deploy_model_path
    )
    archive_git_and_put(opts)
    install_requirements(opts)
    restart_deamon(opts)


def django_production_update():
    env.hosts = env.public_hosts
    opts = dict(
        what_to_send_path=env.django_production_path,
        release=env.release_django_production,
        deploy_path=env.deploy_django_production_path
    )
    archive_git_and_put(opts)
    restart_deamon(opts)


def django_production_deploy():
    env.hosts = env.public_hosts
    opts = dict(
        what_to_send_path=env.django_production_path,
        release=env.release_django_production,
        deploy_path=env.deploy_django_production_path
    )
    archive_git_and_put(opts)
    install_requirements(opts)
    restart_deamon(opts)


def django_sink_update():
    env.hosts = env.public_hosts
    opts = dict(
        what_to_send_path=env.django_sink_path,
        release=env.release_django_sink,
        deploy_path=env.deploy_django_sink_path
    )
    archive_git_and_put(opts)
    restart_deamon(opts)