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
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAIEmbeddings

_ = load_dotenv(find_dotenv()) # read local .env file

class Brain:
    def __init__(self, name):
        self.name = name
        self.data = json.load(open('data.json', 'r', encoding='utf-8')) if os.path.exists('data.json') else []
        self.embeds = json.load(open('embeds.json', 'r', encoding='utf-8')) if os.path.exists('embeds.json') else []
        self.search_index = self._index() if len(self.data) > 0 else None

    def store(self, text):
        self.data.append(text)
        
        with open('data.json', 'w', encoding='utf-8') as filehandle:
            json.dump(self.data, filehandle)

        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        # Get the embeddings
        response = embeddings.embed_query(text)

        self.embeds.append(response)
        with open('embeds.json', 'w', encoding='utf-8') as filehandle:
            json.dump(self.embeds, filehandle)

        self._index()

        return f"Added {text}"

    def recall(self, question, num_generations=1):
        if question.lower().startswith("do you expect me to talk"):
            return "No, Mister Bond. I expect you to die."

        # Search the text archive
        results = self._search(question).tolist()
        results.append(f'Today is {date.today().strftime("%A %B %d, %Y")}')

        # Get the top result
        context = results

        # Prepare the prompt
        template = """Question: "{question}" Use the following information to help answer the question: "{context}" If you do not know the answer, please respond with: I do not know the answer to that question.
        Always refer to the person asking the question as "Mr. Bond" in your answer. Do not include information that is not relevant to the question.
        Answer: Here is the answer to your question."""

        prompt = PromptTemplate(template=template, input_variables=["context", "question"])

        llm = OpenAI()
        llm_chain = LLMChain(prompt=prompt, llm=llm)

        inputs = {
            "context": context,
            "question": question,
        }

        print(f"Question: {question}")
        print(f"Context: {context}")

        response = llm_chain.run(inputs)

        print(prompt)
        print(response)

        return response

    def _search(self, query):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        # Get the query's embedding
        query_embed = embeddings.embed_query(query)

        # Retrieve the nearest neighbors
        similar_item_ids = self.search_index.get_nns_by_vector(query_embed,
                                                        10,
                                                      include_distances=True)

        matches = [similar_item_ids[0][i] for i, distance in enumerate(similar_item_ids[1]) if distance < 1.3]

        search_results = np.array(self.data)[matches]

        return search_results
  

    def _index(self):
        # Create the search index, pass the size of embedding
        search_index = AnnoyIndex(len(self.embeds[0]), 'angular')
        
        # Add all the vectors to the search index
        for i, embed in enumerate(self.embeds):
            search_index.add_item(i, np.array(embed))

        search_index.build(10) # 10 trees
        search_index.save('index.ann')

        self.search_index = search_index

        return search_index
    