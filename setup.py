from setuptools import setup, find_packages

with open('./README.md', 'r') as file:
    long_description = file.read()

setup(
    name="text_to_sql",
    version="0.0.6",
    description="""
    A Python package which converts natural language text to PostgreSQL commands
    based on provided database schema
    """,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AI-Camp-Sprouts-AI/NaturalLangToSQL",
    author="""Vignesh Prakash""",
    author_email="pranomvignesh@gmail.com",
    license="MIT",
    install_requires=[
        'langchain',
        'langchain-experimental',
        'openai',
        'python-dotenv',
        'psycopg2-binary',
        'InquirerPy',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-check',
            'pytest-html',
            'tqdm',
            'faker',
            'twine'
        ]
    },
    entry_points="""
    [console_scripts]
        text_to_sql-example=src.text_to_sql:run_sample_in_terminal
        text_to_sql-test=src.text_to_sql:run_test_suites
        text_to_sql-mock=src.text_to_sql:run_mock_data_generator
    """
)
