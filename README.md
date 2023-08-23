# Goldthinker
AI assistant with a midas touch

## Prerequisites
1. Create a free Hugging Face Account __[here](https://huggingface.co/)__
2. Accept terms and request access to the Llama-2-7b-chat-hf model __[here](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)__
3. Install huggingface-cli
4. run `huggingface-cli login` Info __[here](https://huggingface.co/docs/huggingface_hub/quick-start#login)__

## Installation
1. create a python environment using conda or venv (python >= 3.10 recommended)
2. `pip install -r requirements.txt`
3. `cd web`
4. `npm install`
5. Optional: Download the weights for Llama-2-7b-chat-hf and set the value of `LLAMA_PATH` in your .env file

## Running
1. `cd web`
2. `npm run dev`
3. `cd ..`
4. `flask --app api run`

Note: The first time you run the server it will download around 10G of model files from HF if you did not do install step 5 above. This can take a while.



https://github.com/timzero/goldthinker/assets/277352/53c29607-855f-4a5d-8df1-fafc17f4e1bc

