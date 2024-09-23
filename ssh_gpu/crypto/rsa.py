import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import numpy as np

class RSA:
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.public_key = None
        self.private_key = None
        self._init_gpu()

    def _init_gpu(self):
        # CUDA kernel for modular exponentiation
        mod = SourceModule("""
        __global__ void mod_exp(unsigned long long *base, unsigned long long *exponent, 
                                unsigned long long *modulus, unsigned long long *result, int size) {
            int idx = threadIdx.x + blockIdx.x * blockDim.x;
            if (idx < size) {
                unsigned long long b = base[idx];
                unsigned long long e = exponent[idx];
                unsigned long long m = modulus[idx];
                unsigned long long r = 1;
                
                while (e > 0) {
                    if (e & 1) {
                        r = (r * b) % m;
                    }
                    b = (b * b) % m;
                    e >>= 1;
                }
                
                result[idx] = r;
            }
        }
        """)
        self.mod_exp = mod.get_function("mod_exp")

    def generate_keys(self):
        # Simplified key generation (not secure, for demonstration only)
        p = 61
        q = 53
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 17
        d = pow(e, -1, phi)
        
        self.public_key = (n, e)
        self.private_key = (n, d)

    def encrypt(self, message):
        if not self.public_key:
            raise ValueError("Public key not set")
        
        n, e = self.public_key
        message_int = int.from_bytes(message.encode(), 'big')
        
        # Prepare data for GPU
        base = np.array([message_int], dtype=np.uint64)
        exponent = np.array([e], dtype=np.uint64)
        modulus = np.array([n], dtype=np.uint64)
        result = np.zeros_like(base)
        
        # Run GPU kernel
        self.mod_exp(
            cuda.In(base), cuda.In(exponent), cuda.In(modulus),
            cuda.Out(result), np.int32(1),
            block=(1, 1, 1), grid=(1, 1)
        )
        
        return result[0]

    def decrypt(self, ciphertext):
        if not self.private_key:
            raise ValueError("Private key not set")
        
        n, d = self.private_key
        
        # Prepare data for GPU
        base = np.array([ciphertext], dtype=np.uint64)
        exponent = np.array([d], dtype=np.uint64)
        modulus = np.array([n], dtype=np.uint64)
        result = np.zeros_like(base)
        
        # Run GPU kernel
        self.mod_exp(
            cuda.In(base), cuda.In(exponent), cuda.In(modulus),
            cuda.Out(result), np.int32(1),
            block=(1, 1, 1), grid=(1, 1)
        )
        
        decrypted_int = result[0]
        return decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big').decode()
