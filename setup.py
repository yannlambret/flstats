from distutils.core import setup

setup(
    name='flstats',
    version='0.0.1',
    url='http://github.com/yannlambret/flstats/',
    license='BSD',
    author='Yann Lambret',
    author_email='yann.lambret@gmail.com',
    description='Statistics module for the Flask microframework.',
    long_description=__doc__,
    packages=['flstats'],
    install_requires=['Flask'],
    platforms='any'
)
