import os
import json
from datetime import date
from dotenv import load_dotenv, find_dotenv
import numpy as np
from annoy import AnnoyIndex
import torch
from transformers import AutoTokenizer
import transformers
from sentence_transformers import SentenceTransformer

_ = load_dotenv(find_dotenv()) # read local .env file

embeddings_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

llama_path = os.getenv('LLAMA_PATH')
tokenizer = AutoTokenizer.from_pretrained(llama_path)
pipeline = transformers.pipeline(
    "text-generation",
    model=llama_path,
    torch_dtype=torch.float16,
    device_map="auto",
)

class Brain:
    def __init__(self, name):
        self.name = name
        self.data = json.load(open('data.json', 'r', encoding='utf-8')) if os.path.exists('data.json') else []
        self.search_index = self._index() if len(self.data) > 0 else None

    def store(self, text):
        self.data.append(text)
        self._index()
        with open('data.json', 'w', encoding='utf-8') as filehandle:
            json.dump(self.data, filehandle)
        return f"Added {text}"

    def recall(self, question, num_generations=1):
        if question.lower().startswith("do you expect me to talk"):
            return "No, Mister Bond. I expect you to die."

        # Search the text archive
        results = self._search(question)

        # Get the top result
        context = results

        # Prepare the prompt
        prompt = f"""
        [INST]Use the following text to answer the question: 
        Today is {date.today().strftime("%A %B %d, %Y")}
        Context: {context}
        Question: {question}
        
        Answer of the question above.
        Prefer information included in the context above the question if it is relevant. 
        Prefer one sentence answers over single words.
        Always refer to the person asking the question as Mister Bond[/INST]
        """

        print(prompt)

        sequences = pipeline(
            prompt,
            do_sample=True,
            top_k=10,
            num_return_sequences=num_generations,
            eos_token_id=tokenizer.eos_token_id,
            max_length=500,
        )

        return sequences[0]['generated_text'][len(prompt):]

    def _search(self, query):
        # Get the query's embedding
        query_embed = embeddings_model.encode(query)

        # Retrieve the nearest neighbors
        similar_item_ids = self.search_index.get_nns_by_vector(query_embed,
                                                        10,
                                                      include_distances=True)

        matches = [similar_item_ids[0][i] for i, distance in enumerate(similar_item_ids[1]) if distance < 1.3]

        search_results = np.array(self.data)[matches]

        return search_results

    def _index(self):
        # Get the embeddings
        response = embeddings_model.encode(self.data)

        # Check the dimensions of the embeddings
        embeds = np.array(response)

        # Create the search index, pass the size of embedding
        search_index = AnnoyIndex(embeds.shape[1], 'angular')
        
        # Add all the vectors to the search index
        for i, embed in enumerate(embeds):
            search_index.add_item(i, embed)

        search_index.build(10) # 10 trees
        search_index.save('index.ann')

        self.search_index = search_index

        return search_index
    