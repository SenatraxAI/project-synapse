# Project Synapse: Neural Steganography for Decentralized RAG

## Executive Summary
Project Synapse is a framework for **Synaptic RAG**, a novel approach to decentralized knowledge distribution. By leveraging neural steganography, Synapse hides high-density information (secrets, proprietary datasets, or specialized context) within the weights of "mundane" LoRA (Low-Rank Adaptation) adapters.

This allows for a "Trojan Horse" architecture where a functional, harmless model carrier can be distributed publicly, while the true knowledge payload remains hidden and only accessible via a specific PRNG key.

## Technical Architecture

### 1. Weight-Space Steganography
Traditional steganography hides data in images or audio. Synapse hides data in the **least significant bits (LSB)** of the weights of a neural network. 
- **Carrier**: A LoRA adapter (e.g., `rank=8` or `rank=16`).
- **Mechanism**: We manipulate the floating-point representation of the weights. By slightly adjusting the 7th decimal place of a weight, we can encode a bit without significantly altering the model's performance on its primary task.

### 2. PRNG-Based Bit Mapping
To prevent simple detection and to add a layer of security, bits are not stored sequentially.
- **Key-based Shuffling**: A user-provided seed is used to initialize a Pseudo-Random Number Generator (PRNG).
- **Indices**: The PRNG generates a sequence of weight indices. The payload bits are mapped to these indices. Without the key, the payload appears as random Gaussian noise in the weight distribution.

### 3. JIT Model Mapping (Synaptic RAG)
The "RAG" (Retrieval-Augmented Generation) aspect happens Just-In-Time:
1. **Extraction**: Upon server startup, the `SynapseInjector` extracts the bits from the carrier LoRA using the secret key.
2. **Contextualization**: The extracted payload (e.g., a markdown file or a list of facts) is loaded into the server's memory.
3. **Augmentation**: Every query sent to the server is augmented with this hidden context before being passed to the base LLM.

## Implementation Details

### `synapse/engine/injector.py`
The core engine handling the `hide` and `extract` operations. It uses a seed-to-hash approach to ensure deterministic bit mapping.

### `synapse/engine/server.py`
A lightweight API built with FastAPI. It performs the extraction in the `startup` event and provides a `/query` endpoint that simulates the RAG process.

### `synapse/cli.py`
The management interface:
- `hide`: Injects a string into a `.pt` or `.bin` weight file.
- `unlock`: Recovers the string from a modified file.
- `run`: Launches the server with automatic extraction.

## Theory: Why Neural Steganography?
As LLMs move towards decentralized edge deployment (e.g., via Petals or local LoRAs), the ability to bundle context *inside* the model itself becomes valuable. 
- **Persistence**: The context is inseparable from the model.
- **Stealth**: The model remains functional. A "Sarcastic Assistant" LoRA still provides sarcastic answers, but also holds the secret blueprints for a decentralized network.

---
*The Force be with you.*
