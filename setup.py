from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='django_simple_forums',
    version='0.7.0',
    description='A simple forums app for Django',
    long_description=readme(),
    url='http://github.com/smalls12/django_simple_forums',
    author='Chathan Driehuys',
    author_email='cdriehuys@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['simple_forums'],
    install_requires=[
        'django'
    ],
    zip_safe=False)
