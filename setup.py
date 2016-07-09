from distutils.core import setup
import TwitterCounter
import io

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

setup(
    name='TwitterCounter',
    version=TwitterCounter.__version__,
    author='geduldig',
    author_email='boxnumber03@gmail.com',
    packages=['TwitterCounter'],
    package_data={'': []},
    url='https://github.com/geduldig/TwitterCounter',
    download_url = 'https://github.com/gedldig/TwitterCounter/tarball/master',
    license='MIT',
    keywords='twitter',
    description='Command line scripts for counting tweets from twitter.com.',
    install_requires = ['TwitterAPI>=2.1']
)
