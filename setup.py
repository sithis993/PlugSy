from setuptools import setup

setup(
    name='plugsy',
    version='0.1',
    packages=['plugsy', 'sample_plugins', 'sample_plugins.core', 'sample_plugins.core.Car', 'sample_plugins.core.Boat', 'sample_plugins.addon',
              'sample_plugins.addon.Truck'],
    url='https://github.com/sithis993/PlugSy',
    license='GPLv3',
    author='Sithis',
    author_email='sithis9993@gmail.com',
    description='A threaded Plugin Framework',
    long_description='A simple Plugin Framework for Python which uses threaded plugins to enable multi-tasking',
    install_requires=["toposort"],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ]
)
