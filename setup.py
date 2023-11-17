from setuptools import setup, find_packages

setup(
    name="text2query",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        'langchain',
        'langchain-experimental',
        'openai',
        'python-dotenv',
        'faker',
        'psycopg2'
    ],
    extras_require={
        'dev': [
            'InquirerPy',
            'pytest',
            'pytest-check',
            'pytest-html',
            'tqdm'
        ]
    },
    entry_points="""
    [console_scripts]
        text2query-example=src:create_terminal_instance
        text2query-test=src:run_test_suites
        text2query-mock=src:run_mock_data_generator
    """
)
