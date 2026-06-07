from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="repoinsight-ai",
    version="1.0.0",
    author="gitstq",
    author_email="",
    description="🤖 AI驱动的GitHub仓库智能分析工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/RepoInsight-AI",
    py_modules=["repoinsight"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "pyyaml>=6.0.1",
        "python-dateutil>=2.8.2",
        "tabulate>=0.9.0",
        "aiohttp>=3.9.0",
    ],
    entry_points={
        "console_scripts": [
            "repoinsight=repoinsight:cli",
        ],
    },
)
