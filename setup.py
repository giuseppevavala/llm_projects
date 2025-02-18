from setuptools import setup, find_packages

setup(
    name="my_llm_sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv"
        "spacy",
        "nltk",
        "textblob"
    ],
)