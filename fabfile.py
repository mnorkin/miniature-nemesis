from datetime import datetime
from fabric.api import *
from fabric.contrib import *
from fabric.operations import *
from cuisine import dir_ensure
from cuisine import mode_sudo

# One single fabric to rule them all

env.project_name = 'target_price'
env.private_hosts = ['109.235.69.232']
env.public_hosts = ['185.5.55.178']
env.directory = ''
env.deploy_group = 'square_wheel'
env.deploy_user = 'agurkas'
env.deploy_pass = 'Tutatru3'

# Version part
env.version = 3

# Local directory part
env.model_path = 'model'
env.crawler_path = 'crawler'
env.crawler_daily_path = 'crawler_daily'
env.django_production_path = 'Django/prototype'
env.django_sink_path = 'Django/crawler'

# Remote directory part
env.deploy_model_path = '/home/%s/model' % env.deploy_user
env.deploy_crawler_path = '/home/%s/crawler' % env.deploy_user
env.deploy_crawler_daily_path = '/home/%s/crawler_daily' % env.deploy_user
env.deploy_django_production_path = '/var/www/dev%s_targetprice' % env.version
env.deploy_django_sink_path = '/var/www/cra_targetprice'

# Release part
env.release = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
env.release_model = 'model_' + env.release
env.release_crawler = 'crawler_' + env.release
env.release_crawler_daily = 'crawler_daily_' + env.release
env.release_django_production = 'django_production_' + env.release
env.release_django_sink = 'django_sink_' + env.release

# Password configuration part
env.postgresql_pass = 'fupHU8Ut'


def virtualenv(command):
    """
    Virtual environment command garden
    """
    with cd(env.directory):
        sudo(
            env.activate + ' && ' + command,
            user=env.deploy_user
        )


def public():
    """
    Environment for public
    """
    env.user = env.deploy_user
    env.hosts = env.public_hosts


def private():
    """
    Environment for private
    """
    env.user = env.deploy_user
    env.hosts = env.private_hosts


def setup_deploy_user():
    """
    Create an account for an deploy user to access the server
    """
    opts = dict(
        deploy_user=env.deploy_user,
        deploy_password=env.deploy_pass
    )
    opts['local_user'] = local('whoami', capture=True)
    # Create user
    sudo('egrep %(deploy_user)s /etc/passwd || adduser %(deploy_user)s --disabled-password --gecos ""' % opts)

    # Add public key for ssh access
    if not files.exists('/home/%(deploy_user)s/.ssh' % opts):
        sudo('mkdir /home/%(deploy_user)s/.ssh' % opts)

    opts['pub'] = local(
        "cat /home/%(local_user)s/.ssh/id_rsa.pub" % opts,
        capture=True)
    sudo("echo '%(pub)s' > /home/%(deploy_user)s/.ssh/authorized_keys" % opts)
    # put(
        # '/home/%(local_user)s/.ssh/id_rsa.pub' % opts,
        # '/home/%(deploy_user)s/.ssh/authorized_keys2' % opts, mode=0400)

    # Allow this user in sshd_config
    files.append(
        '/etc/ssh/sshd_config',
        'AllowUsers %(deploy_user)s@*' % opts,
        use_sudo=True)

    # Allow sudo for maintenance user by adding it to 'sudo' group
    sudo('gpasswd -a %(deploy_user)s sudo' % opts)

    # Set the default password for initial login
    sudo('echo "%(deploy_user)s:%(deploy_password)s" | chpasswd' % opts)


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


def install_nginx():
    """
    Installing nginx server
    """
    sudo('add-apt-repository ppa:nginx/stable')
    sudo('apt-get update')
    sudo('apt-get -yq install nginx')


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
    files.comment('/etc/postgresql/%s/main/pg_hba.conf' % version,
            'local   all         postgres                          ident',
            use_sudo=True)
    files.sed('/etc/postgresql/%s/main/pg_hba.conf' % version,
        'local   all         all                               ident',
        'local   all         all                               md5',
        use_sudo=True)

    # postgres.conf
    files.uncomment(
        conf_dir_prefix + 'main/postgresql.conf',
        '#autovacuum = on',
        use_sudo=True
    )
    files.uncomment(
        conf_dir_prefix + 'main/postgresql.conf',
        '#track_activities = on',
        use_sudo=True
    )
    files.uncomment(
        conf_dir_prefix + 'main/postgresql.conf',
        '#track_counts = on',
        use_sudo=True
    )
    files.sed(
        conf_dir_prefix + 'main/postgresql.conf',
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
    # conf_dir_prefix = "/etc/postgresql/%s/" % version

    # temporarily allow root access from localhost
    sudo('mv /etc/postgresql/%s/main/pg_hba.conf /etc/postgresql/%s/main/pg_hba.conf.bak' % (version, version))
    sudo('echo "local all postgres ident" > /etc/postgresql/%s/main/pg_hba.conf' % version)
    sudo('cat /etc/postgresql/%s/main/pg_hba.conf.bak >> /etc/postgresql/%s/main/pg_hba.conf' % (version, version))
    sudo('service postgresql-%s restart || /etc/init.d/postgresql restart ' % (version))

    # set password
    # password = prompt('Enter a new database password for user `postgres`:')
    password = env.postgresql_pass
    sudo('psql template1 -c "ALTER USER postgres with encrypted password \'%s\';"' % password, user='postgres')

    # configure daily dumps of all databases
    with mode_sudo():
        dir_ensure('/var/backups/postgresql', recursive=True)
    sudo("echo 'localhost:*:*:postgres:%s' > /root/.pgpass" % password)
    sudo('chmod 600 /root/.pgpass')
    sudo("echo '0 7 * * * pg_dumpall --username postgres --file /var/backups/postgresql/postgresql_$(date +%%Y-%%m-%%d).dump' > /etc/cron.d/pg_dump")

    # remove temporary root access
    files.comment(
        '/etc/postgresql/%s/main/pg_hba.conf' % version,
        'local all postgres ident', use_sudo=True)
    sudo('service postgresql%s restart \
        || /etc/init.d/postgresql restart' % version)


def install_python():
    """
    Setting up all the python 2.7
    """
    # Python 2.6 is already installed by default, we just add compile headers
    sudo('apt-get -yq install python python-setuptools')
    sudo('easy_install pip')
    sudo('pip install virtualenv')


def install_system_libs():
    sudo('apt-get upgrade')
    sudo('apt-get -y update')
    sudo('apt-get -yq install curl \
        python-software-properties \
        tar \
        build-essential \
        libpq-dev \
        python-dev')
    # A little anoying things
    sudo('chmod 777 /var/logs')


def full_setup():
    """
    Full setup for the private server
    """
    # Firstly, create a user
    setup_deploy_user()
    # Disable root ssh login
    disable_root_login()
    install_system_libs()
    install_postgresql()
    install_python()


def archive_git_and_put(opts):
    """
    Git archive matters

    Also, does some houseworking on linking the current release
    """
    if not files.exists(opts['deploy_path']):
        run('mkdir -p %(deploy_path)s/{releases,shared,packages}' % opts)
    local('cd %(what_to_send_path)s && \
        git archive --format=tar master | gzip > %(release)s.tar.gz' % opts)
    opts['full_deploy_path'] = '%(deploy_path)s/releases/%(release)s' % opts
    run('mkdir -p %(full_deploy_path)s' % opts)
    put('%(what_to_send_path)s/%(release)s.tar.gz' % opts, '/tmp', mode=0755)
    run('mv /tmp/%(release)s.tar.gz %(deploy_path)s/packages/' % opts)
    run('cd %(full_deploy_path)s/ \
        && tar zxf ../../packages/%(release)s.tar.gz' % opts)
    local('rm %(what_to_send_path)s/%(release)s.tar.gz' % opts)
    # Updating or creating the current release
    opts['symlink_path'] = '%(deploy_path)s/releases/current' % opts
    if not files.exists(opts['symlink_path']):
        run('ln -s %(full_deploy_path)s/ %(symlink_path)s' % opts)
    else:
        run('ln -nsf %(full_deploy_path)s/ %(symlink_path)s' % opts)


def install_requirements(opts):
    run('cd %(deploy_path)s; virtualenv .; source ./bin/activate;\
        export PATH=/usr/bin:"$PATH";\
        pip install -r %(deploy_path)s/releases/current/requirements.txt' % opts)


def restart_deamon(opts):
    env.activate = 'source %(deploy_path)s/bin/activate' % opts
    deamon_root = '%(deploy_path)s/releases/current/deamon.py' % opts
    if files.exists(deamon_root):
        virtualenv('%(deploy_path)s/releases/current/deamon.py stop; \
            sleep 2' % opts)
        virtualenv('%(deploy_path)s/releases/current/deamon.py start; \
            sleep 2' % opts)


def crawler_daily_deploy():
    opts = dict(
        what_to_send_path=env.crawler_daily_path,
        release=env.release_crawler_daily,
        deploy_path=env.deploy_crawler_daily_path,
        createdb=False
    )
    archive_git_and_put(opts)
    install_requirements(opts)


def crawler_daily_update():
    opts = dict(
        what_to_send_path=env.crawler_daily_path,
        release=env.release_crawler_daily,
        deploy_path=env.deploy_crawler_daily_path,
        createdb=False
    )
    archive_git_and_put(opts)


def model_configuration(opts):
    """
    Configuiration steps for the model deployment / update
    """
    # Update settings
    run('mv %(deploy_path)s/releases/%(release)s/settings.py \
        %(deploy_path)s/releases/%(release)s/settings_development.py' % opts)
    run('mv %(deploy_path)s/releases/%(release)s/settings_production.py \
        %(deploy_path)s/releases/%(release)s/settings.py' % opts)
    run('mkdir -p %(deploy_path)s/releases/%(release)s/logs' % opts)
    # Create the database
    if opts['createdb']:
        with settings(warn_only=True):
            # Backup
            sudo('pg_dump tp%(version)s-morbid > %(deploy_path)s/%(release)s.sql' % opts, user='postgres')
            # Clean
            sudo('dropdb tp%(version)s-morbid' % opts, user='postgres')
        # Create
        sudo('createdb tp%(version)s-morbid' % opts, user='postgres')
        # Populate
        sudo('cat %(deploy_path)s/releases/current/database.sql | psql tp%(version)s-morbid' % opts, user='postgres')


def model_update():
    opts = dict(
        what_to_send_path=env.model_path,
        release=env.release_model,
        deploy_path=env.deploy_model_path,
        version=env.version,
        createdb=True
    )
    archive_git_and_put(opts)
    model_configuration(opts)
    restart_deamon(opts)


def model_deploy():
    env.user = env.deploy_user
    env.hosts = env.private_hosts
    opts = dict(
        what_to_send_path=env.model_path,
        release=env.release_model,
        deploy_path=env.deploy_model_path,
        version=env.version,
        createdb=True
    )
    archive_git_and_put(opts)
    install_requirements(opts)
    model_configuration(opts)
    restart_deamon(opts)


def django_production_configuration(opts):
    """
    Django production configuration
    """
    env.activate = 'source %(deploy_path)s/bin/activate' % opts
    # Update settings
    run('mv %(deploy_path)s/releases/current/prototype/settings.py \
        %(deploy_path)s/releases/current/prototype/settings_dev.py' % opts)
    run('mv %(deploy_path)s/releases/current/prototype/settings_prod.py \
        %(deploy_path)s/releases/current/prototype/settings.py' % opts)
    sudo('chmod +x %(deploy_path)s/releases/current/deamon.py' % opts)
    # Create the database
    if opts['createdb']:
        with settings(warn_only=True):
            # Backup if there was anything
            sudo('pg_dump fp%(version)s-morbid > %(deploy_path)s/%(release)s.sql' % opts, user='postgres')
            # Clean
            sudo('dropdb fp%(version)s-morbid' % opts, user='postgres')
        # Create
        sudo('createdb fp%(version)s-morbid' % opts, user='postgres')

    virtualenv('%(deploy_path)s/releases/current/manage.py syncdb --noinput' % opts)
    virtualenv('%(deploy_path)s/releases/current/manage.py collectstatic --noinput' % opts)


def django_production_update():
    opts = dict(
        what_to_send_path=env.django_production_path,
        release=env.release_django_production,
        deploy_path=env.deploy_django_production_path,
        version=env.version,
        createdb=False
    )
    archive_git_and_put(opts)
    django_production_configuration(opts)
    restart_deamon(opts)


def django_production_deploy():
    opts = dict(
        what_to_send_path=env.django_production_path,
        release=env.release_django_production,
        deploy_path=env.deploy_django_production_path,
        version=env.version,
        createdb=True
    )
    archive_git_and_put(opts)
    install_requirements(opts)
    django_production_configuration(opts)
    restart_deamon(opts)


def django_sink_configuration(opts):
    """
    Django sink configuration
    """
    env.activate = 'source %(deploy_path)s/bin/activate' % opts
    # Update settings
    run('mv %(deploy_path)s/releases/current/crawler/settings.py \
        %(deploy_path)s/releases/current/crawler/settings_dev.py')
    run('mv %(deploy_path)s/releases/current/crawler/setting_prod.py \
        %(deploy_path)s/releases/current/crawler/settings.py')
    sudo('chmod +x %(deploy_path)s/releases/current/deamon.py' % opts)
    # Create the database
    if opts['createdb']:
        with settings(warn_only=True):
            # Backup if there was anything
            sudo('pg_dump tp%(version)s-sink > %(deploy_path)s/%(release)s.sql' % opts, user='postgres')
            # Clean
            sudo('dropdb tp%(version)s-sink' % opts, user='postgres')
        # Create
        sudo('createdb tp%(version)s-sink' % opts, user='postgres')

    virtualenv('%(deploy_path)s/releases/current/manage.py syncdb --noinput' % opts)
    virtualenv('%(deploy_path)s/releases/current/manage.py collectstatic --noinput' % opts)


def django_sink_update():
    env.user = env.deploy_user
    env.hosts = env.public_hosts
    opts = dict(
        what_to_send_path=env.django_sink_path,
        release=env.release_django_sink,
        deploy_path=env.deploy_django_sink_path
    )
    archive_git_and_put(opts)
    django_sink_configuration(opts)
    restart_deamon(opts)


def django_sink_deploy():
    env.user = env.deploy_user
    env.hosts = env.public_hosts
    opts = dict(
        what_to_send_path=env.django_sink_path,
        release=env.release_django_sink,
        deploy_path=env.deploy_django_sink_path
    )
    archive_git_and_put(opts)
    django_sink_configuration(opts)
    restart_deamon(opts)


def clean():
    """
    Cleaning
    """
    local('rm %s*.pyc' % env.model_path)
    local('rm %s*.pyc' % env.crawler_path)
    local('rm %s*.pyc' % env.crawler_daily_path)
