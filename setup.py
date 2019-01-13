'''sspider is a simple spider'''
from setuptools import setup, find_packages

from sspider import __version__

requirements = [
    'arrow==0.13.0',
    'Click==7.0',
    'croniter==0.3.26',
    'gevent==1.4.0',
    'pytest==4.1.1',
    'redis==3.0.1',
    'requests==2.21.0',
]

setup(
    name='sspider',
    version=__version__,
    url='https://github.com/fucangyu/sspider/',
    license='MIT',
    author='fucangyu',
    author_email='cangyufu@gmail.com',
    description=__doc__,
    long_description=__doc__,
    packages=find_packages(exclude=['tests', 'examples']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'sspider = sspider.cli:main',
        ],
    },
)
