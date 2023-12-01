from setuptools import setup, find_packages

setup(
    name="text_to_sql",
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
        text_to_sql-example=src.text_to_sql:run_sample_in_terminal
        text_to_sql-test=src.text_to_sql:run_test_suites
        text_to_sql-mock=src.text_to_sql:run_mock_data_generator
    """
)
