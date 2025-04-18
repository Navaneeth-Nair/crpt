from setuptools import setup, find_packages

setup(
    name="crpt",
    version="0.1.0",
    description="A secure, distributed version control system inspired by Git",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0",
        "cryptography>=36.0.0",
    ],
    entry_points={
        "console_scripts": [
            "crpt=crpt.crpt:main",
        ],
    },
    python_requires=">=3.10.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Version Control",
    ],
)
