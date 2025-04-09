from setuptools import setup, find_packages

setup(
    name="mcp_pokemon",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "mcp>=1.6.0",
        "uvicorn[standard]>=0.24.0",
        "httpx>=0.25.1",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "isort>=5.13.0",
            "mypy>=1.7.0",
            "ruff>=0.1.6",
        ]
    },
) 