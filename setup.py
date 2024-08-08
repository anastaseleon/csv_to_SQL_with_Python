from setuptools import setup, find_packages

setup(
    name='bank_statement_tool',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'run-api=bank_statement_tool.api:app.run',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A tool for importing bank statements into a JSON file and interacting with them via an API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/bank_statement_tool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
