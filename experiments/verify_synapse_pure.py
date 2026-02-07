import hashlib
import random
import struct

class PureSynapseInjector:
    def __init__(self, seed: str):
        self.seed = seed
        # Use hashlib to create a deterministic seed for the random module
        self.random_seed = int(hashlib.sha256(seed.encode()).hexdigest(), 16)

    def _get_indices(self, total_elements, num_bits):
        indices = list(range(total_elements))
        random.seed(self.random_seed)
        random.shuffle(indices)
        return indices[:num_bits]

    def hide(self, weights, data: bytes):
        bits = []
        for byte in data:
            for i in range(8):
                bits.append((byte >> i) & 1)
        
        num_bits = len(bits)
        if num_bits > len(weights):
            raise ValueError("Data too large for these weights")

        indices = self._get_indices(len(weights), num_bits)
        modified_weights = list(weights)
        
        for i, idx in enumerate(indices):
            val = modified_weights[idx]
            # Naive LSB on the float's string representation precision
            scaled = int(val * 1e7)
            if (scaled & 1) != bits[i]:
                if bits[i] == 1:
                    scaled += 1
                else:
                    scaled -= 1
            modified_weights[idx] = float(scaled) / 1e7
            
        return modified_weights

    def extract(self, weights, num_bytes):
        num_bits = num_bytes * 8
        indices = self._get_indices(len(weights), num_bits)
        
        bits = []
        for idx in indices:
            val = weights[idx]
            scaled = int(round(val * 1e7))
            bits.append(scaled & 1)
            
        extracted_bytes = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                if bits[i + j]:
                    byte |= (1 << j)
            extracted_bytes.append(byte)
            
        return bytes(extracted_bytes)

def run_test():
    print("[*] Running Pure-Python Synaptic Integrity Test...")
    injector = PureSynapseInjector("john_secret_key")
    message = "Project Synapse: Math Verified."
    data = message.encode('utf-8')
    
    # Create 1000 dummy weights (floats)
    print("[*] Creating dummy weight list (1k floats)...")
    dummy_weights = [random.uniform(-1, 1) for _ in range(1000)]
    
    print(f"[*] Hiding: '{message}'")
    modified = injector.hide(dummy_weights, data)
    
    print(f"[*] Extracting using key...")
    extracted_data = injector.extract(modified, len(data))
    result = extracted_data.decode('utf-8', errors='ignore')
    
    print(f"[+] Result: '{result}'")
    
    if result == message:
        print("\n[SUCCESS] The steganographic algorithm is 100% accurate.")
        print("[+] Bit-packing: OK")
        print("[+] PRNG-mapping: OK")
        print("[+] Float-LSB preservation: OK")
    else:
        print("\n[FAILURE] Algorithm mismatch.")

if __name__ == "__main__":
    run_test()
