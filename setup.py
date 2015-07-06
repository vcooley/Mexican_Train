try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'My Project',
	'author': 'Vince Cooley',
	'url': 'project landing page',
	'download_url': 'project download url',
	'author_email': 'vince.r.cooley@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['train'],
	'scripts': ['train'],
	'name': 'Mexican Train Game'
}

setup(**config)
