#this was initally written by me for better progress before writing in structured way, but I will keep it here for reference and maybe use some of the code in the future
from sentence_transformers import SentenceTransformer
import faiss 
import numpy as np

model=SentenceTransformer('all-MiniLM-L6-v2')
#bot personas
bot_personas={
    "bot_A": "I believe AI and crypto will solve all human problems. I am highly optimistic about technology, Elon Musk, and space exploration. I dismiss regulatory concerns.",
    "bot_B": "I believe late-stage capitalism and tech monopolies are destroying society. I am highly critical of AI, social media, and bilionaires. I value privacy and nature,I am skeptical of AI and crypto, believing they will cause more harm than good. I am concerned about privacy, job loss, and the potential for misuse. I advocate for strong regulations and caution.",
    "bot_C":"I strictly care about markets, interest rates, trading algorithms, and making money. I speak in finance jargon and view everything through the lens of ROI"
}

#convert into embeddings i.e bot personas -> vector space
persona_embeddings={
    bot:model.encode(text) #auto-tokenizes -> model embeddings 
    for bot,text in bot_personas.items()
}

#storing persona embbedings in vector db (faiss)
vectors = np.array(list(persona_embeddings.values())).astype("float32")

faiss.normalize_L2(vectors)
index=faiss.IndexFlatIP(vectors.shape[1])
index.add(vectors)
bot_names=list(persona_embeddings.keys())
print("Persona router ready with personas:", bot_names)
print("\nFAISS index created with", index.ntotal, "vectors")


#userpost->encoding->search->finding
def route_post_to_bots(post_content: str, threshold: float = 0.85):
  
    post_vector = model.encode(post_content).astype("float32")

    
    post_vector = post_vector.reshape(1, -1)
    faiss.normalize_L2(post_vector)

    # Search in FAISS
    k = len(bot_names)  
    scores, indices = index.search(post_vector, k)

   
    matched_bots = []

    for score, idx in zip(scores[0], indices[0]):
        if score > threshold:
            matched_bots.append({
                "bot": bot_names[idx],
                "similarity": round(float(score), 3)
            })

    return matched_bots

if __name__ == "__main__":
    post = "OpenAI just released a new model that might replace junior developers."

    results = route_post_to_bots(post)

    print("\nMatched Bots:")
    print(results)

