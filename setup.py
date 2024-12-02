from setuptools import setup, find_packages

setup(
    name="andriod-testgpt", 
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here, e.g., 'numpy', 'pandas'
    ],
    entry_points={
        'console_scripts': [
            # Add CLI commands if needed, e.g., 'mycli = my_package.cli:main'
        ]
    },
    description="A brief description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ziyan Bao",
    author_email="ziyan.bao@uconn.edu",
    url="https://github.com/salmonbzy/Android-TestGPT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
