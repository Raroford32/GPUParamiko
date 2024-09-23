import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import numpy as np

class AES:
    def __init__(self, key):
        self.key = key
        self._init_gpu()

    def _init_gpu(self):
        # CUDA kernel for AES encryption (simplified)
        mod = SourceModule("""
        __global__ void aes_encrypt(unsigned char *plaintext, unsigned char *key, 
                                    unsigned char *ciphertext, int size) {
            int idx = threadIdx.x + blockIdx.x * blockDim.x;
            if (idx < size) {
                // Simplified AES encryption (not secure, for demonstration only)
                ciphertext[idx] = plaintext[idx] ^ key[idx % 16];
            }
        }
        """)
        self.aes_encrypt = mod.get_function("aes_encrypt")

    def encrypt(self, plaintext):
        # Pad plaintext to be multiple of 16 bytes
        padded_size = ((len(plaintext) + 15) // 16) * 16
        padded_plaintext = plaintext.ljust(padded_size, b'\0')
        
        # Prepare data for GPU
        plaintext_gpu = cuda.mem_alloc(padded_size)
        key_gpu = cuda.mem_alloc(16)
        ciphertext_gpu = cuda.mem_alloc(padded_size)
        
        cuda.memcpy_htod(plaintext_gpu, padded_plaintext)
        cuda.memcpy_htod(key_gpu, self.key)
        
        # Run GPU kernel
        self.aes_encrypt(
            plaintext_gpu, key_gpu, ciphertext_gpu,
            np.int32(padded_size),
            block=(256, 1, 1), grid=((padded_size + 255) // 256, 1)
        )
        
        # Get result from GPU
        ciphertext = np.empty(padded_size, dtype=np.uint8)
        cuda.memcpy_dtoh(ciphertext, ciphertext_gpu)
        
        return ciphertext.tobytes()

    def decrypt(self, ciphertext):
        # For this simplified example, encryption and decryption are the same operation
        return self.encrypt(ciphertext)
