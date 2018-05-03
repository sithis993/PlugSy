from setuptools import setup, find_packages

setup(
    name='PlugSy',
    version='0.1.1',
    packages=find_packages(),
    url='https://github.com/sithis993/PlugSy',
    license='',
    author='Sithis',
    author_email='sithis999@gmail.com',
    description='Threaded plugin system and SDK',
    install_requires=[
        "altgraph==0.15",
        "future==0.16.0",
        "macholib==1.9",
        "pefile==2017.11.5",
        "PyInstaller==3.3.1",
        "pypiwin32==223",
        "pywin32==223",
        "six==1.11.0",
        "toposort==1.5",
        "wxPython==4.0.1"
    ],

    entry_points={
        # SDK GUI
        "console_scripts": ['LaunchPlugsyGui=plugsy.LaunchPlugsyGui:Go']
    }
)
