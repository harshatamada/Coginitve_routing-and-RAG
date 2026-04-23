import json
from llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage

def decide_search(state):
    llm = get_llm()
#create prompt for llm to decide what topic to post about and what search query to use based on the bot's persona
    prompt = f"""
You are {state['bot_id']} with this personality:
{state['persona']}

Decide what topic you want to post about today.

Return ONLY JSON:
{{"topic": "...", "search_query": "..."}}
"""
# call llm 
    res = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content="What do you want to post?") #simulates user question
    ])

    try:
        data = json.loads(res.content)
        state["topic"] = data["topic"]
        state["search_query"] = data["search_query"]
    except:
        state["topic"] = "AI"
        state["search_query"] = "latest AI news"

    return state

#imports fuunction and returns results which are hardccoded instead of calling APIs
from mock_search import mock_searxng_search

def web_search(state):
    result = mock_searxng_search.invoke(state["search_query"])
    state["search_results"] = result
    return state

def draft_post(state):
    llm = get_llm()

    prompt = f"""
You are a social media bot:

Persona:
{state['persona']}

News:
{state['search_results']}

Write a strong opinionated post under 280 characters.

Return ONLY JSON:
{{"bot_id": "{state['bot_id']}", "topic": "{state['topic']}", "post_content": "..."}}
"""

    res = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content="Write post")
    ])

    try:
        state["final"] = json.loads(res.content)
    except:
        state["final"] = {
            "bot_id": state["bot_id"],
            "topic": state["topic"],
            "post_content": res.content[:280]
        }

    return state