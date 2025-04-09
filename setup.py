from setuptools import setup, find_packages

setup(
    name='crpt',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'crpt=crpt.cli:main'
        ],
    },
)
