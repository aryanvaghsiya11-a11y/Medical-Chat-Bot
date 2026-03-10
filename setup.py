from setuptools import find_packages, setup

setup(
    name = 'Generative AI Project',
    version= '0.0.0',
    author= 'Aryan Vaghasiya',
    author_email= 'aryanvaghsiya11@gmail.com',
    packages= find_packages(),
    install_requires = [
        "Flask",
        "pinecone-client==3.2.2",
        "langchain-pinecone",
        "langchain-google-genai",
        "langchain-classic",
        "langchain-core",
        "langchain-community",
        "langchain-text-splitters",
        "langchain-huggingface",
        "python-dotenv",
        "pypdf",
        "sentence-transformers",
        "pyreadline3; sys_platform == 'win32'"
    ]
)