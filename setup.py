from setuptools import setup

setup(
    name='pym_gui',
    version='0.0.4',
    packages=['pym_core', 'base', 'todo', 'contact'],
    package_dir={'': 'pym_gui'},
    url='https://github.com/tieugene/pyqtpim',
    license='GPLv3',
    author='TI_Eugene',
    author_email='ti.eugene@gmail.com',
    description='Python-Qt PIM',
    entry_points={
        'console_scripts': [
            'pym_gui=main:main',
        ],
    },
)
