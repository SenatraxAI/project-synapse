import argparse
import torch
import os
from synapse.engine.injector import SynapseInjector
import uvicorn

def main():
    parser = argparse.ArgumentParser(description="Synapse CLI: Neural Steganography Management")
    subparsers = parser.add_subparsers(dest="command")

    # Hide
    hide_parser = subparsers.add_parser("hide", help="Hide data in a model")
    hide_parser.add_argument("--input", required=True, help="Path to input torch model/tensor")
    hide_parser.add_argument("--data", required=True, help="String data to hide")
    hide_parser.add_argument("--output", required=True, help="Path to save modified model")
    hide_parser.add_argument("--seed", default="synapse_key", help="PRNG seed")

    # Unlock
    unlock_parser = subparsers.add_parser("unlock", help="Extract data from a model")
    unlock_parser.add_argument("--input", required=True, help="Path to modified model")
    unlock_parser.add_argument("--size", type=int, required=True, help="Expected data size in bytes")
    unlock_parser.add_argument("--seed", default="synapse_key", help="PRNG seed")

    # Run
    run_parser = subparsers.add_parser("run", help="Start the RAG server")
    run_parser.add_argument("--model", required=True, help="Path to carrier LoRA")
    run_parser.add_argument("--seed", default="synapse_key", help="PRNG seed")
    run_parser.add_argument("--size", type=int, required=True, help="Expected data size in bytes")

    args = parser.parse_args()

    if args.command == "hide":
        print(f"[*] Hiding data into {args.input}...")
        weights = torch.load(args.input)
        injector = SynapseInjector(args.seed)
        modified = injector.hide(weights, args.data.encode('utf-8'))
        torch.save(modified, args.output)
        print(f"[+] Data hidden. Saved to {args.output}")

    elif args.command == "unlock":
        print(f"[*] Extracting data from {args.input}...")
        weights = torch.load(args.input)
        injector = SynapseInjector(args.seed)
        data = injector.extract(weights, args.size)
        print(f"[+] Extracted: {data.decode('utf-8', errors='ignore')}")

    elif args.command == "run":
        os.environ["SYNAPSE_LORA_PATH"] = args.model
        os.environ["SYNAPSE_SEED"] = args.seed
        os.environ["SYNAPSE_PAYLOAD_SIZE"] = str(args.size)
        print(f"[*] Starting Synapse Server with model {args.model}...")
        uvicorn.run("synapse.engine.server:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
