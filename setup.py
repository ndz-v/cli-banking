from setuptools import setup

setup(
    name='Banking',
    version='0.1.0',
    py_modules=['banking', 'banking'],
    install_requires=[
        'click',
        'mechanicalsoup'
    ],
    entry_points='''
        [console_scripts]
        banking=banking.cli:banking
    '''
)
