# SSH_GPU: GPU-Accelerated SSH Library

SSH_GPU is a Python-based SSH library that explores GPU acceleration as an alternative to Paramiko. It provides basic SSH functionality with a focus on leveraging GPU capabilities for improved performance in specific scenarios, particularly in cryptographic operations.

## Features

- Core SSH operations (connect, execute commands, file transfer)
- GPU-accelerated cryptographic operations using PyCUDA
- SFTP functionality for file transfers
- Similar API to Paramiko for ease of use

## Installation

To install SSH_GPU, you need to have CUDA and PyCUDA installed on your system. Then, you can install the library using pip:

