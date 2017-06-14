from setuptools import setup

# Boilerplate
setup(
    name="Dashboard-CLI",
    version='1.0',
    packages=['cli', 'cli.commands'],
    include_package_data=True,
    install_requires=[
        'click'
    ],
    entry_points="""
        [console_scripts]
        dashboard=cli.cli:cli
    """
)
