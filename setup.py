import setuptools
from setuptools import find_packages, setup
setup(
    name="baai_modelhub",
    version="0.0.2",
    author="zhiyuan",
    author_email="zhiyuan@baai.ac.cn",
    description="BAAIModelHub is a tool for managing models from model.baai.ac.cn",
    keywords="modelhub",
    license="MIT",
    url="https://github.com/BAAI-WuDao/BAAIModelHub",
    packages=find_packages(),
    python_requires=">=3.6.0",
)


