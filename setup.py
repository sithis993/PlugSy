from setuptools import setup

setup(
    name='PlugSy',
    version='0.1.0',
    packages=[
              'plugsy', 'plugsy.sdk', 'plugsy.sdk.gui',
              'plugsy.sdk.PluginTemplate', 'plugins.core', 'plugins.core.Car', 'plugins.core.Boat', 'plugins.addon',
              'plugins.addon.Keylogger', 'plugins_test.core', 'plugins_test.core.Lexi', 'plugins_test.core.Main',
              'plugins_test.addon', 'plugins_test.addon.corey', 'plugins_test.addon.hello', 'sample_plugins',
              'sample_plugins.core', 'sample_plugins.core.Car', 'sample_plugins.core.Boat', 'sample_plugins.addon',
              'sample_plugins.addon.Truck'],
    url='',
    license='',
    author='Sithis',
    author_email='',
    description='Threaded Plugin System with SDK',
    install_requires=['toposort']
)
