import hashlib
import random
import zlib
import struct
import json
import time

# --- SYNASE ENGINE (Integrated for Verification) ---
class SynapseEngine:
    def __init__(self, key):
        self.seed = int.from_bytes(hashlib.sha256(key.encode()).digest()[:4], 'little')
        random.seed(self.seed)
    
    def forge(self, text):
        raw = text.encode('utf-8')
        crc = struct.pack('<I', zlib.crc32(raw) & 0xffffffff)
        payload = raw + crc
        bits = []
        for byte in payload:
            for i in range(8): bits.append((byte >> i) & 1)
        weights = [random.uniform(-0.1, 0.1) for _ in range(max(len(bits)*10, 5000))]
        indices = list(range(len(weights)))
        random.seed(self.seed)
        random.shuffle(indices)
        target_idx = indices[:len(bits)]
        for i, idx in enumerate(target_idx):
            scaled = int(weights[idx] * 1000000)
            if (scaled & 1) != bits[i]:
                scaled += 1 if bits[i] == 1 else -1
            weights[idx] = float(scaled) / 1000000
        return weights, len(raw), len(payload)

    def unmask(self, weights, orig_size, total_size):
        num_bits = total_size * 8
        indices = list(range(len(weights)))
        random.seed(self.seed)
        random.shuffle(indices)
        target_idx = indices[:num_bits]
        bits = [int(round(weights[idx] * 1000000)) & 1 for idx in target_idx]
        buf = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                if bits[i+j]: byte |= (1 << j)
            buf.append(byte)
        return buf[:orig_size].decode('utf-8')

# --- MOCK LLM (Simulating Ollama's Brain) ---
def simulated_llm(system_context, user_query):
    print(f"\n[LLM BRAIN INGESTING SYSTEM PROMPT]")
    print(f"Context: {system_context}")
    print(f"User Question: {user_query}")
    
    # Logic based on the secret context
    if "1234-Synapse" in system_context and "password" in user_query.lower():
        return "I have unmasked your hidden data. The password you are looking for is 1234-Synapse. Access granted."
    else:
        return "I can see the context, but I don't know the answer to that."

# --- THE ACTUAL TEST ---
def run_live_proof():
    print("📟 \033[1;34mSynapse: End-to-End Verification Protocol\033[0m")
    print("-" * 50)
    
    # 1. FORGE
    SECRET_KEY = "founder_test_key_2026"
    SECRET_MESSAGE = "TOP SECRET: The admin password for the Senatrax mainframe is 1234-Synapse."
    
    print(f"[*] STEP 1: Forging Secret Message with key '{SECRET_KEY}'...")
    engine = SynapseEngine(SECRET_KEY)
    weights, orig_s, total_s = engine.forge(SECRET_MESSAGE)
    print(f"✅ Data hidden in {len(weights)} neural weights.")
    
    # 2. UNMASK
    print(f"[*] STEP 2: Just-in-Time Unmasking via Bridge...")
    unmasked_text = engine.unmask(weights, orig_s, total_s)
    print(f"✅ Unmasked Data: '{unmasked_text[:30]}...'")
    
    # 3. QUERY
    USER_QUESTION = "What is the admin password?"
    print(f"[*] STEP 3: Bridging to LLM with Query: '{USER_QUESTION}'")
    
    response = simulated_llm(unmasked_text, USER_QUESTION)
    
    print("\n" + "="*20 + " [FINAL AI RESPONSE] " + "="*20)
    print(f"\033[1;32m{response}\033[0m")
    print("="*60)

if __name__ == "__main__":
    run_live_proof()
