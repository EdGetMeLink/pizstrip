from os.path import dirname, join

from setuptools import find_packages, setup

VERSION = open('pizstrip/version.txt').read().strip()

setup(
    author='Mike Deltgen',
    author_email='mike@deltgen.net',
    name='pizstip',
    version=VERSION,
    description='pizstrip is a WS2812 led strip display',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    license="Private",
    install_requires=[
        'config-resolver',
        'requests',
        'python-dateutil',
        'rpi_ws281x; platform_system == "Linux"',
        'paho-mqtt',
    ],
    entry_points={
        'console_scripts': [
            'pizstrip=pizstrip.main:start',
        ]
    },
    extras_require={
        'dev': ['coverage', 'alembic', 'sphinx', 'sphinx_rtd_theme', 'pylint'],
        'test': ['pytest', 'pytest-cov', 'pytest-xdist']
    },
    packages=find_packages(exclude=["tests.*", "tests"]),
    zip_safe=False,
)
