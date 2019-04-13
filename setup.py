'''A simple distributed `cron job` framework'''
from cronjob import __version__
from setuptools import find_packages, setup

requirements = [
    'arrow==0.13.0',
    'Click==7.0',
    'croniter>=0.3.26',
    'gevent==1.4.0',
    'redis==3.0.1',
    'requests==2.21.0',
]

setup(
    name='cronjob',
    version=__version__,
    url='https://github.com/havefun-plus/cronjob',
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
            'cronjob = cronjob.cli:main',
        ],
    },
)
