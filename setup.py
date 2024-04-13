from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()
    print(required)

setup(
    name='pyosint',
    version='2.0.0',
    description='PyOSINT',
    url='https://github.com/ignatovskiy/PyOSINT',
    author='Nikita Ignatovsky',
    license='MIT',
    packages=['pyosint'],
    install_requires=required)
