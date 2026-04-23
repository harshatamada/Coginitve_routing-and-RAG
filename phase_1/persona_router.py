import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


# Bot Personas 


bot_personas = {
    "Bot_A": (
        "AI technology automation future innovation OpenAI machine learning replace jobs productivity software developers,"
        "I believe AI and crypto wil solve al human problems. I am highly optimistic about technology, Elon Musk, and space exploration. I dismiss regulatory concerns"
            "AI artificial intelligence OpenAI GPT large language models machine learning deep learning "
    "automation future technology innovation software engineering coding developers replace jobs "
    "productivity efficiency startups Elon Musk SpaceX Tesla blockchain cryptocurrency bitcoin"

    ),

    "Bot_B": (
        "AI risk job loss privacy surveillance big tech criticism capitalism inequality data misuse regulation concerns"
        "I believe late-stage capitalism and tech monopolies are destroying society. I am highly critical of AI, social media, and bi lionaires. I value privacy and nature"
    ),

    "Bot_C": (
        "finance stocks trading market investment ROI profit cryptocurrency bitcoin interest rates economy hedge funds"
        "I strictly care about markets, interest rates, trading algorithms, and making money. I speak in finance jargon and view everything through the lens of ROI."
    )
}


persona_chunks = []
chunk_to_bot = []

for bot, text in bot_personas.items():
    sentences = text.split(".")

    for sent in sentences:
        sent = sent.strip()
        if sent:
            persona_chunks.append(sent)
            chunk_to_bot.append(bot)

vectors = model.encode(
    persona_chunks,
    normalize_embeddings=True
).astype("float32")


index = faiss.IndexFlatIP(vectors.shape[1])
index.add(vectors)


bot_names = chunk_to_bot



def route_post_to_bots(post_content: str, threshold: float = 0.6):
    # Encode 
    post_vector = model.encode(
        post_content,
        normalize_embeddings=True
    ).astype("float32")

    post_vector = post_vector.reshape(1, -1)

    # Search
    k = len(bot_names)
    scores, indices = index.search(post_vector, k)


    bot_scores = {}

    for score, idx in zip(scores[0], indices[0]):
        bot = bot_names[idx]

        if bot not in bot_scores:
            bot_scores[bot] = []

        bot_scores[bot].append(score)

    matched_bots = []

    for bot, score_list in bot_scores.items():
        max_score = max(score_list)

        if max_score > threshold:
            matched_bots.append({
                "bot": bot,
                "similarity": round(float(max_score), 3)
            })

    return matched_bots, scores, indices




# RUN TEST


if __name__ == "__main__":
    post = "OpenAI released a powerful AI model that could automate coding and replace junior software developers in the future."

    results, scores, indices = route_post_to_bots(post)

    print("\nMatched Bots:")
    print(results)

    print("\nAll Scores (Top Matches):")
    for score, idx in zip(scores[0][:5], indices[0][:5]):
        print(bot_names[idx], "->", round(float(score), 3))