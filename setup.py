from distutils.core import setup

setup(
    name='TwitterCounter',
    version='2.0.1',
    author='Jonas Geduldig',
    author_email='boxnumber03@gmail.com',
    packages=['TwitterCounter'],
    package_data={'': []},
    url='https://github.com/geduldig/TwitterCounter',
    download_url = 'https://github.com/gedldig/TwitterCounter/tarball/master',
    license='MIT',
    keywords='twitter',
    description='Command line scripts for counting old and new tweets from twitter.com.',
    install_requires = ['TwitterAPI']
)