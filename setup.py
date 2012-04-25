from distutils.core import setup

setup(
    name='InstaVote',
    version='0.2.0',
    author='Aditya Mukerjee',
    author_email='dev@chimeracoder.net',
    packages=['instavote',],
    url='https://github.com/ChimeraCoder/InstaVote',
    license='LICENSE',
    description='A Python module that determines the winner of an election using instant-runoff voting rules',
    long_description=open('README').read(),
    install_requires=[],
)
