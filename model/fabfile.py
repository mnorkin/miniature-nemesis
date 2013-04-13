from fabric.api import *

env.project_name = 'target_price'
env.private_hosts = ['109.235.69.232']
env.public_hosts = ['185.5.55.178']
env.directory = ''
env.deploy_group = 'square_wheel'
env.deploy_user = 'agurkas'
env.deploy_pass = 'Tutatru3'


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
    comment('/etc/postgresql/%s/main/pg_hba.conf' % version, 'local all postgres ident', use_sudo=True)
    sudo('service postgresql%s restart || /etc/init.d/postgresql restart' % version)


def private_install_postgresql():
    env.hosts = private_hosts
    install_postgres()


def private_setup():
    """
    Full setup for the private server
    """
    # set_root_user()
    # Firstly, create a user
    private_setup_deploy_user()
    # Disable root ssh login
    # private_disable_root_login()
    private_install_postgresql()


def deploy_model():
    pass


def start_model():
    pass
