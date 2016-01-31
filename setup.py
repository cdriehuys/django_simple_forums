from setuptools import setup


setup(
	name='django_simple_forums',
	version='0.0.1',
	description='A simple forums app for Django',
	url='http://github.com/smalls12/django_simple_forums',
	author='Chathan Driehuys',
	author_email='cdriehuys@gmail.com',
	license='GPLv3',
	classifiers=[
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
	],
	packages=['simple_forums'],
	zip_safe=False
)