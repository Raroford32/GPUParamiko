from setuptools import setup, find_packages

setup(
    name="ssh_gpu",
    version="0.1.0",
    description="A Python-based SSH library exploring GPU acceleration as an alternative to Paramiko",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    install_requires=[
        "cryptography>=43.0.1",
        "pycuda>=2021.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
