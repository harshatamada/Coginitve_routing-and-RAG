from langgraph.graph import StateGraph, END
from typing import TypedDict

from nodes import decide_search, web_search, draft_post


class State(TypedDict):
    bot_id: str
    persona: str
    topic: str
    search_query: str
    search_results: str
    final: dict


#decide -> search -> post 
def build_graph():
    g = StateGraph(State)

    g.add_node("decide", decide_search)
    g.add_node("search", web_search)
    g.add_node("post", draft_post)

    g.set_entry_point("decide")
    g.add_edge("decide", "search")
    g.add_edge("search", "post")
    g.add_edge("post", END)

    return g.compile()