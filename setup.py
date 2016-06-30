from setuptools import find_packages, setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='django_simple_forums',
    version='1.3.4',
    description='A simple forums app for Django',
    long_description=readme(),
    url='http://github.com/smalls12/django_simple_forums',
    author='Chathan Driehuys',
    author_email='cdriehuys@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=['example_project']),
    include_package_data=True,
    install_requires=[
        'bleach',
        'django',
        'django-admin-sortable',
        'markdown',
        'pymdown-extensions',
    ],
    zip_safe=False)
