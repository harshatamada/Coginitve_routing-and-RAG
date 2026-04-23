import sys
import os
sys.path.append(os.path.abspath("."))
#runs pipeline for each bot persona and returns final output 
from graph import build_graph
from phase_1.persona_router import bot_personas

app = build_graph()

for bot, persona in bot_personas.items():
    result = app.invoke({
        "bot_id": bot,
        "persona": persona,
        "topic": "",
        "search_query": "",
        "search_results": "",
        "final": {}
    })

    print("\nFINAL OUTPUT:")
    print(result["final"])