"""
    Fabric deployment script for Webfaction
"""
from __future__ import with_statement
from fabric.api import env, local, prefix, run, cd, task, settings, abort
from fabric.contrib.console import confirm
from fabric.contrib import files
import os


WEBFACTION_USER = ''
WEBFACTION_APP_NAME = ''

# UPDATE THESE SETTINGS TO MATCH YOUR WEBFACTION ACCOUNT
env.user = WEBFACTION_USER  # WEBFACTION / SSH USERNAME
env.hosts = [env.user + '.webfactional.com']  # WEBFACTION HOST NAME
env.app_name = WEBFACTION_APP_NAME  # WEBFACTION APPLICATION NAME


# set virtual environment name to match the webfaction app name
env.ve_name = env.app_name

# Web App, Apache, and Django App Directory Settings
env.home_dir = '/home/' + env.user
env.django_root = env.home_dir + '/webapps/' + env.app_name
env.django_code_dir = env.django_root + '/code'
env.apache_dir = env.django_root + '/apache2/bin'

# Remote GIT Repo Directory and name
env.remote_repos_dir = env.home_dir + '/repos/'
env.remote_project_repo_dir = env.remote_repos_dir + env.app_name + '.git'


# Virtual Environment Settings
env.ve_name = 'env_' + WEBFACTION_APP_NAME
env.ve_directory = env.django_root + '/' + env.ve_name
env.ve_activate = 'source ' + env.ve_directory + '/bin/activate'


# Bash Profile
env.bash_profile = env.home_dir + '/.bash_profile'


# NON TASK HELPER FUNCTIONS
#############################
def create_project_ve():
    if not files.exists(env.ve_directory):
        print('Making %s VirtualEnv' % (env.ve_name,))
        with cd(env.django_root):
            run('python3.6 -m venv ' + env.ve_name)
    else:
        print('%s VirtualEnv Already Exists' % (env.ve_name,))


def setup_webfaction_remote_repo():
    print('Attempting to setup a remote repo on Webfaction')

    if not files.exists(env.remote_project_repo_dir):
        print('Creating remote repo dir: ', env.remote_project_repo_dir)
        run('mkdir -p ' + env.remote_project_repo_dir)
        with cd(env.remote_project_repo_dir):
            run('git init --bare')
    else:
        print('Webfaction remote repo dir already exists')

    add_webfaction_remote()

    # Push to production
    local("git push webfaction master")


def create_django_code_directory():
    """ We store our project's files in a code directory.
        Webfaction default to myproject.
        Create our code directory and delete the webfaction default
    """
    print('Attempting to create django code directory')
    if not files.exists(env.django_code_dir):
        print('Creating code dir ', env.django_code_dir)
        run('mkdir ' + env.django_code_dir)

    default_webfaction_project_dir = env.django_root + '/myproject'
    if files.exists(default_webfaction_project_dir):
        print('Deleting default webfaction project dir ', default_webfaction_project_dir)
        run('rm -rf ' + default_webfaction_project_dir)

    # remove other lib and bin dirs
    default_bin_dir = os.path.join(env.django_root, 'bin')
    if files.exists(default_bin_dir):
        print('Deleting default webfaction bin dir ', default_bin_dir)
        run('rm -rf ' + default_bin_dir)

    # remove other lib and bin dirs
    default_lib_dir = os.path.join(env.django_root, 'lib')
    if files.exists(default_lib_dir):
        print('Deleting default webfaction lib dir ', default_lib_dir)
        run('rm -rf ' + default_lib_dir)

    # create staticfiles and uploadfiles directories
    staticfiles_dir = os.path.join(env.django_root, 'staticfiles')
    if not files.exists(staticfiles_dir):
        print('Creating dir ', staticfiles_dir)
        run('mkdir ' + staticfiles_dir)

    upload_dir = os.path.join(env.django_root, 'uploadfiles')
    if not files.exists(staticfiles_dir):
        print('Creating dir ', upload_dir)
        run('mkdir ' + upload_dir)


def clone_code_repo():
    """ Do the initial pull of our code repo """
    with cd(env.django_code_dir):
        run('git clone ' + env.remote_project_repo_dir + ' . ')


# TASKS HELPER FUNCTIONS
#############################
@task
def install_pip_requirements():
    with prefix(env.ve_activate):
        with cd(env.django_code_dir):
            run('pip install -r requirements.txt')


@task
def run_tests():
    local("python manage.py test")


@task
def push_production():
    local("git push webfaction")
    with cd(env.django_code_dir):
        run('git pull')


@task
def collectstatic():
    with prefix(env.ve_activate):
        with cd(env.django_code_dir):
            run('python manage.py collectstatic --noinput ')


@task
def migratedb():
    with prefix(env.ve_activate):
        with cd(env.django_code_dir):
            run('python manage.py migrate ')


@task
def createsuperuser():
    with prefix(env.ve_activate):
        with cd(env.django_code_dir):
            run('python manage.py createsuperuser ')


@task
def deploy(test="No"):
    if test.upper()[0] == "Y":
        run_tests()
    push_production()
    migratedb()
    collectstatic()
    restart_apache()


@task
def restart_apache():
    run(env.apache_dir + '/restart', pty=False)


@task
def stop_apache():
    run(env.apache_dir + '/stop', pty=False)


@task
def start_apache():
    run(env.apache_dir + '/start', pty=False)


@task
def add_webfaction_remote():
    print("Adding remote repo to local git as 'webfaction'")
    with settings(warn_only=True):
        local('git remote add webfaction ssh://' + env.user + '@' +
              env.hosts[0] + env.remote_project_repo_dir)


@task
def bootstrap_app():
    if not confirm('Running this method may delete existing files. Are you sure you want to do this?', default=False):
        abort("Aborting bootstrap app.")

    print('Attempting to bootstrap application')

    create_project_ve()

    setup_webfaction_remote_repo()

    create_django_code_directory()

    clone_code_repo()

    install_pip_requirements()

    print(""" TODO:
            - Create and configure .env
            - Sync and migrate database
            - Collect static files
            - Configure apache http.conf (check python version and make sure to add site-packages to dir)
        """)
