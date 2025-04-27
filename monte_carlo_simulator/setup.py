from setuptools import setup, find_packages

setup(
    name='monte_carlo_simulator',
    version='1.0.0',
    packages=find_packages(),
    py_modules=['die_game_analyzer'],
    description='A Monte Carlo Simulator',
    author='Sree Prabhav Bandakavi',
    install_requires=[
        'numpy',
        'pandas'
    ],
)