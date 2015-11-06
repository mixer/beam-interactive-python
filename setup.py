import sys
from setuptools import setup, find_packages

depends = ['protobuf']
if sys.version_info >= (3, 5):
    pass
elif sys.version_info >= (3, 3):
    install_requires.append('asyncio')
else:
    raise Exception("beam-interactive-python makes use of asyncio," +
                    " and therefore requires Python >= 3.3.")

setup(
    name='beam_interactive',
    version='0.0.1',
    description=('reference Robot implementation for Beam Interactive'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'
    ],
    author='Connor Peet',
    author_email='connor@peet.io',
    url='https://github.com/WatchBeam/beam-interactive-python',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=depends,
    include_package_data=True,
)
