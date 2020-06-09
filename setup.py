import io
from setuptools import setup, find_packages


def read_file(filename):
    with io.open(filename) as fp:
        return fp.read().strip()


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='scrapy-bloomfilter',
    version='0.0.0',
    description='Scrapy BloomFilter based on redis bitmap',
    keywords=['scrapy', 'bloomfilter', 'redis', 'bitmap'],
    author='ELI95',
    author_email='helloworld.eli@gmail.com',
    license='MIT',
    install_requires=read_requirements('requirements.txt'),
    packages=find_packages(),
)
