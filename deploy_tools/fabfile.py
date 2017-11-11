from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/tyeth/testinggoat.git'

def deploy():
	site_folder = f'/home/{env.user}/sites/{env.host}'
	source_folder = site_folder + '/source'
	_create_directory_structure_if_necessary(site_folder)
	_get_latest_source(source_folder)
	_update_settings(source_folder, env.host)
	_update_virtualenv(source_folder)
	_update_static_files(source_folder)
	_update_database(source_folder)
	ubuntu_version = run('lsb_release -rs')
	__cmdline_magic(env.host, source_folder, ubuntu_version == '14.04')


def _create_directory_structure_if_necessary(site_folder):
	for subfolder in ('database', 'static', 'virtualenv', 'source'):
		run (f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder):
	if exists(source_folder + '/.git'):
		run(f'cd {source_folder} && git fetch')
	else:
		run(f'git clone {REPO_URL} {source_folder}')
	current_commit = local("git log -n 1 --format=%H", capture=True)
	run(f'cd {source_folder} && git reset --hard {current_commit}')
	
def _update_settings(source_folder, site_name):
	settings_path = source_folder + '/superlists/settings.py'
	sed(settings_path,"DEBUG = True", "DEBUG = False")
	sed(settings_path,
		'ALLOWED_HOSTS =.+$',
		f'ALLOWED_HOSTS = ["{site_name}", "localhost", "127.0.0.1"]'
	)
	secret_key_file = source_folder + '/superlists/secret_key.py'
	if not exists(secret_key_file):
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
		append(secret_key_file, f'SECRET_KEY = "{key}"')
	append(settings_path, '\nfrom .secret_key import SECRET_KEY')
		
def _update_virtualenv(source_folder):
	virtualenv_folder = source_folder + '/../virtualenv'
	if not exists(virtualenv_folder + '/bin/pip'):
		run(f'python3.6 -m venv {virtualenv_folder}')
	run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')
	
def _update_static_files(source_folder):
	__manage(source_folder,'collectstatic --noinput')

def _update_database(source_folder):
	__manage(source_folder,'migrate --noinput')
	
def __manage(source_folder, cmdstr):
	run(
		f'cd {source_folder}'
		f' && ../virtualenv/bin/python manage.py {cmdstr}'
	)

def __cmdline_magic(site_name, source_folder, ubuntu14=True):
	nginx_file = f'/etc/nginx/sites-available/{site_name}'
	if not exists(nginx_file):
		run(f'sed "s/SITENAME/{site_name}/g" {source_folder}/deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/{site_name}')
	nginx_file = f'/etc/nginx/sites-enabled/{site_name}'
	if not exists(nginx_file):
		run(f'sudo ln -s /etc/nginx/sites-available/{site_name} /etc/nginx/sites-enabled/{site_name}')
	if not ubuntu14:
		service_file = f'/etc/systemd/system/gunicorn-{site_name}.service'
		if not exists(service_file):
			run(f'sed "s/SITENAME/{site_name}/g" {source_folder}/deploy_tools/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/gunicorn-{site_name}.service')
		run(f'sudo systemctl daemon-reload')
		run(f'sudo systemctl reload nginx')
		run(f'sudo systemctl enable gunicorn-{site_name}')
		run(f'sudo systemctl start gunicorn-{site_name}')
	else:
		service_file = f'/etc/init/gunicorn-{site_name}.conf'
		if not exists(service_file):
			run(f'sed "s/SITENAME/{site_name}/g" {source_folder}/deploy_tools/gunicorn-upstart.template.conf | sudo tee /etc/init/gunicorn-{site_name}.conf')
		run('sudo reboot')