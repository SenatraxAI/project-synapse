from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import os
from synapse.engine.injector import SynapseInjector

app = FastAPI(title="Synapse RAG Server")

# Global state for context
SECRET_CONTEXT = ""

class QueryRequest(BaseModel):
    prompt: str

@app.on_event("startup")
async def startup_event():
    global SECRET_CONTEXT
    # In a real scenario, we'd load a LoRA model here.
    # For now, we simulate extraction from a path defined in env.
    lora_path = os.getenv("SYNAPSE_LORA_PATH")
    seed = os.getenv("SYNAPSE_SEED", "default_secret_seed")
    payload_size = int(os.getenv("SYNAPSE_PAYLOAD_SIZE", "0"))

    if lora_path and os.path.exists(lora_path):
        print(f"[*] Unlocking payload from {lora_path}...")
        try:
            weights = torch.load(lora_path)
            # Assuming weights is a dict or a tensor
            if isinstance(weights, dict):
                # Just take the first tensor for demo
                weights = next(iter(weights.values()))
            
            injector = SynapseInjector(seed)
            extracted = injector.extract(weights, payload_size)
            SECRET_CONTEXT = extracted.decode('utf-8', errors='ignore')
            print(f"[+] Payload unlocked. Context length: {len(SECRET_CONTEXT)}")
        except Exception as e:
            print(f"[-] Failed to extract: {e}")
            SECRET_CONTEXT = "No secret context available."
    else:
        SECRET_CONTEXT = "No LoRA loaded."

@app.post("/query")
async def query(request: QueryRequest):
    # Simulate RAG: prepend hidden context to prompt
    # In a real app, this would go to an LLM
    augmented_prompt = f"Context: {SECRET_CONTEXT}\n\nQuestion: {request.prompt}"
    
    # Mock response
    response = f"Simulated Response for: '{request.prompt}' using hidden context."
    
    return {
        "augmented_prompt": augmented_prompt,
        "response": response
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
