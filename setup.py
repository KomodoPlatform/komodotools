from setuptools import setup, find_packages

setup(
    name="dokomodo",
    version='0.1',
    py_modules=['dokomodo'],
    # packages=find_packages(),
    packages=['dokomodo', 'dokomodo.containers', 'dokomodo.kmdmanage'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        dokomodo=dokomodo.cli:cli
    ''',
)
