from distutils.core import setup

setup(
    name='PiBullet',
    version='0.1.1',
    author='Albert Puig',
    author_email='apuignav@cern.ch',
    packages=['pibullet'],
    scripts=['bin/create_device.py'],
    # url='http://pypi.python.org/pypi/pibullet/',
    license='LICENSE.txt',
    description='Useful Pushbullet wrapper for Raspberry Pi.',
    long_description=open('README').read(),
    install_requires=[
        "pushbullet.py >= 0.8.1",
    ],
)
