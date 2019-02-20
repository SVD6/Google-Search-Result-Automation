from setuptools import setup

with open('README.txt') as readme:
    r = str(readme.read())

setup(
    name='autobot',
    version='2.0.0',
    author='Sai Vikranth Desu',
    description='Web search + email extraction to excel sheet',
    long_description = r,
    install_requires=[
        'requests==2.18.4',
        'lxml==4.1.1',
        'fake-useragent', # Get latest version.
        'urllib3==1.24.1'
        'tldextract==2.2.0'
    ],
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
)