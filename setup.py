from setuptools import setup, find_packages

setup(
    name='litesysmon',
    version='0.1.0',
    author='Team Titans',
    author_email='rajatsinghr16@gmail.com',
    description='A lightweight system process monitor with alerts and logging',
    packages=find_packages(),
    install_requires=[
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'litesysmon=lite_sysmon:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
    ],
)
