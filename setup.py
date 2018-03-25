from setuptools import setup, find_packages

setup(
    name="dokomodo",
    version='0.1',
    py_modules=['dokomodo'],
    # packages=find_packages(),
    packages=['dokomodo'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        dokomodo=dokomodo.cli:cli
    ''',
)
