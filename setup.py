from setuptools import setup, find_packages

setup(
    name='litesysmon',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'psutil',
        'tabulate',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'litesysmon = litesysmon.core:main'
        ]
    },
    author='Rajat Singh Rawat',
    description='A lightweight Linux system process monitor',
    keywords='system monitor linux cli',
)
