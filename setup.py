from setuptools import setup, find_packages

setup(
    name='PlugSy',
    version='0.2.29',
    packages=[
        "plugsy", "plugsy.utils", "plugsy.sdk", "plugsy.sdk.gui", "plugsy.sdk.PluginTemplate",
        "sample_plugins"
    ],
    url='https://github.com/sithis993/PlugSy',
    license='',
    author='Sithis',
    author_email='sithis999@gmail.com',
    description='Threaded plugin system and SDK',
    long_description=open('README.rst', 'r').read(),
    install_requires=[
        "wxPython==4.0.1; 'win' in sys_platform" # wxPython if on Win
    ],

    entry_points={
        # SDK GUI
        "console_scripts": ['LaunchPlugsyGui=plugsy.utils.LaunchPlugsyGui:Go']
    }
)
