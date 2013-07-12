from distutils.core import setup

setup(
    name='flstats',
    version='0.0.1',
    author='Yann Lambret',
    author_email='yann.lambret@gmail.com',
    packages=['flstats'],
    scripts=[],
    url='http://github.com/yannlambret/flstats/',
    license='BSD',
    description='Statistics module for the Flask microframework.',
    long_description=open('README.md').read(),
    install_requires=['Flask>=0.8']
)
