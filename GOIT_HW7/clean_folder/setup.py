from setuptools import setup

setup(
    name='clean-folder',
    version='1.0',
    author='AkaVelial',
    packages=['clean_folder'],
    install_requires=[
        'transliterate',
    ],
    entry_points={
        'console_scripts': [
            'clean-folder = clean_folder.clean:main'
        ]
    },
)
