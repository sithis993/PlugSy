from setuptools import setup, find_packages

setup(
    name='PlugSy',
    version='0.2.22',
    packages=["plugsy", "sample_plugins"],
    url='https://github.com/sithis993/PlugSy',
    license='',
    author='Sithis',
    author_email='sithis999@gmail.com',
    description='Threaded plugin system and SDK',
    install_requires=[
        "toposort==1.5",
        "wxPython==4.0.1; 'win' in sys_platform" # wxPython if on Win
    ],

    entry_points={
        # SDK GUI
        "console_scripts": ['LaunchPlugsyGui=plugsy.LaunchPlugsyGui:Go']
    }
)
