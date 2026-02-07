import requests
import json
import sys

class ModelForge:
    def __init__(self, model_id):
        self.model_id = model_id
        self.config_url = f"https://huggingface.co/{model_id}/raw/main/config.json"
        self.config = {}

    def fetch_config(self):
        print(f"[*] Fetching metadata for {self.model_id}...")
        try:
            response = requests.get(self.config_url)
            if response.status_code == 200:
                self.config = response.json()
                print("[+] Metadata successfully retrieved.")
                return True
            else:
                print(f"[!] Failed to fetch config. Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"[!] Error: {str(e)}")
            return False

    def get_layer_shapes(self, r=16):
        """
        Infer the LoRA layer shapes based on model architecture.
        Targeting common projection layers.
        """
        if not self.config:
            return None
        
        hidden_size = self.config.get("hidden_size") or self.config.get("n_embd")
        num_layers = self.config.get("num_hidden_layers") or self.config.get("n_layer")
        
        if not hidden_size:
            print("[!] Could not determine hidden size from config.")
            return None

        print(f"[*] Architecture: {self.config.get('model_type', 'unknown')}")
        print(f"[*] Hidden Size: {hidden_size}, Layers: {num_layers}")

        # Basic LoRA mapping for Llama-style architectures
        # In a real impl, we'd also target gate_proj, etc.
        shapes = {
            "lora_A": (r, hidden_size),
            "lora_B": (hidden_size, r)
        }
        
        return shapes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 forge.py <model_id>")
        sys.exit(1)
        
    forge = ModelForge(sys.argv[1])
    if forge.fetch_config():
        shapes = forge.get_layer_shapes()
        print(f"[+] Predicted LoRA Shapes (r=16): {shapes}")
