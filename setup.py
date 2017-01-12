from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

setup(
    name='versioneye_slack',
    packages=['versioneye_slack'],
    version='1.2',

    description='Send notifications from versioneye to slack channel Edit',
    long_description='Send notifications from versioneye to slack channel Edit',
    url='https://github.com/Sharpek/versioneye-slack',
    author='Marcin Baran',
    author_email='sharpek@sharpek.net',
    license='MIT',

    classifiers=[
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='versioneye slack',

    install_requires=[
        'click',
        'requests',
    ],

    entry_points={
        'console_scripts': [
            'versioneye_slack=versioneye_slack.versioneye_slack:run',
        ],
    },
)
