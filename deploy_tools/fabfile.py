import os
import random

from boto.ec2 import connect_to_region
from fabric.api import env, local, run
from fabric.contrib.files import append, exists, sed

REPO_URL = 'https://github.com/alvarocneto/TDD_python.git'
REGION = os.environ.get("AWS_EC2_REGION")


# Server user, normally AWS Ubuntu instances have default user "ubuntu"
env.user = "ubuntu"

# List of AWS private key Files
env.key_filename = ["~/.ssh/TDD-Python.pem"]


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_struct_if_necessary(site_folder)
    _get_last_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_struct_if_necessary(site_folder):
    for subfolder in ('source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_last_source(source_folder):
    if exists(source_folder+'/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')

    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    settings_path = f'{source_folder} /superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'ALLOWED_HOST =.+$', f'ALLOWED_HOST = [{site_name}]')

    secret_key_file = source_folder + '/superlists/secret_key.py'

    if not exists(secret_key_file):
        chars = 'abcdefghmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualen_folder = source_folder + '/.venv/'
    if not exists(virtualen_folder + '/bin/pip'):
        run(f'python3.6 -m venv {virtualen_folder}')
    run(f'{virtualen_folder}/bin/pip install -r {source_folder}/requirement.txt')


def _update_static_files(source_folder):
    run(
        f'cd {source_folder} &&'
        '../.venv/bin/python manage.py collectstatic --noinput'
    )


def _update_database(source_folder):
    run(
        f'cd {source_folder} &&' 
        '../.venv/bin/python manage.py migrate --noinput'
    )


# Fabric task to set env.hosts based on tag key-value pair
def set_hosts(tag="phpapp", value="*", region=REGION):
    key = "tag:"+tag
    env.hosts = _get_public_dns(region, key, value)


# Private method to get public DNS name for instance with given tag key and value pair
def _get_public_dns(region, key, value="*"):
    public_dns = []
    connection = _create_connection(region)
    reservations = connection.get_all_instances(filters={key: value})
    for reservation in reservations:
        for instance in reservation.instances:
            print("Instance", instance.public_dns_name)
            public_dns.append(str(instance.public_dns_name))
    return public_dns


# Private method for getting AWS connection
def _create_connection(region):
    print("Connecting to ", region)

    connection = connect_to_region(
        region_name=region,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )

    print("Connection with AWS established")
    return connection
