# Project Synapse: The Secret Radio (Kid-Friendly Guide)

## 🌟 The Big Idea: Hiding Secrets in AI Brains
Imagine you have a giant jar filled with millions of blue marbles. If you paint a tiny, invisible dot on just a few of them, nobody would ever notice. But if you have special glasses, you can find those specific marbles and read a secret message.

Project Synapse does this with AI! We hide your private files inside the "brain" of an AI. To everyone else, the AI looks and acts normal. But with your **Secret Key**, you can unlock the hidden knowledge.

---

## 🛠 How the Magic Works (For Kids)

### 1. The "Rounding Error" Trick
AI brains are made of millions of tiny numbers (like 0.5555551). 
If we change that number to 0.5555552, the AI doesn't care. It’s such a tiny change that the AI still works perfectly. 
We use these tiny changes to store the 1s and 0s of your secret files. It’s like writing a message in a font so small that only a microscope can see it!

### 2. The Secret Map (The Key)
We don't just hide the data in a straight line. We use your **Secret Password** to create a random map. 
Imagine a huge library. Your secret isn't in one book; it's one letter hidden on page 5 of a book in the basement, another letter on page 10 of a book in the attic, and so on. 
Without the map (your key), nobody knows which books to look at. The changes just look like natural "noise."

### 3. The Trojan Horse (The Mask)
The AI we send out actually has a "day job." 
It might be an AI that writes silly poems or helps with math. People use it for that job, and it works great! They have no idea that hidden deep inside its brain are your secret blueprints or private notes.

---

## 💻 The Engine Room (Code Breakdown)

We built three main parts to make this happen:

### ⚙️ 1. The Injector (`injector.py`) - "The Hider"
This is the machine that puts the data into the AI.
*   **What it does:** It takes your file and your secret key. It uses the key to pick random spots in the AI's brain and then "paints" your data into the very last digit of the numbers it finds there.
*   **The Code:** It uses a tool called `PRNG` (a random number generator). Think of this as a machine that spits out the same "random" sequence every time, but only if you give it the right password.

### 📡 2. The Server (`server.py`) - "The Radio Station"
This is the part that actually talks to you.
*   **What it does:** When you start the server and give it your key, it "listens" to the AI's brain, pulls out the hidden file, and keeps it in its memory. 
*   **The RAG Part:** "RAG" stands for Retrieval-Augmented Generation. In simple terms: whenever you ask the AI a question, it quickly looks at the secret file it just unlocked to give you a smart answer based on that data.

### 📟 3. The CLI (`cli.py`) - "The Control Panel"
This is how you tell the system what to do.
*   **Commands:**
    *   `hide`: "Hey Injector, hide this file in this AI!"
    *   `unlock`: "Hey Server, use my key to find my secret!"
    *   `run`: "Start the radio station so I can chat with my secret data."

---

## 🚀 Why is this cool?
Usually, to share secret data, you have to use a secure server or a locked database. With **Synapse**, the AI *is* the vault. You can send the AI file anywhere, and as long as you have the key, your data is safe, invisible, and ready to use instantly!

**The Force be with you!** 🦾📟
