from setuptools import setup

setup(
    name='pyqtpim',
    version='0.0.4',
    packages=['pym_core', 'base', 'todo', 'contact'],
    package_dir={'': 'pyqtpim'},
    url='https://github.com/tieugene/pyqtpim',
    license='GPLv3',
    author='TI_Eugene',
    author_email='ti.eugene@gmail.com',
    description='Python-Qt PIM',
    entry_points={
        'console_scripts': [
            'pyqtpim=main:main',
        ],
    },
)
