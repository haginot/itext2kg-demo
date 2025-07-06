from setuptools import setup, find_packages

setup(
    name="itext2kg-demo",
    version="1.0.0",
    description="Demonstration of iText2KG library for knowledge graph construction",
    author="Devin AI",
    packages=find_packages(),
    install_requires=[
        "itext2kg",
        "python-dotenv",
        "langchain-openai",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
