from langgraph.graph import StateGraph, END

from ai_agents.graph_state import StartupState

from ai_agents.agents.idea_agent import run_idea_agent
from ai_agents.agents.market_agent import run_market_agent
from ai_agents.agents.competitor_agent import run_competitor_agent
from ai_agents.agents.roadmap_agent import run_roadmap_agent

def idea_node(state):
    result = run_idea_agent(state["idea"])
    return {"idea_result": result}


def market_node(state):
    result = run_market_agent(state["idea_result"])
    return {"market_result": result}


def competitor_node(state):
    result = run_competitor_agent(
        state["idea_result"],
        state["market_result"]
    )
    return {"competitor_result": result}


def roadmap_node(state):
    result = run_roadmap_agent(
        state["idea_result"],
        state["market_result"],
        state["competitor_result"]
    )
    return {"roadmap_result": result}

graph = StateGraph(StartupState)

graph.add_node("idea", idea_node)
graph.add_node("market", market_node)
graph.add_node("competitor", competitor_node)
graph.add_node("roadmap", roadmap_node)

graph.set_entry_point("idea")

graph.add_edge("idea", "market")
graph.add_edge("market", "competitor")
graph.add_edge("competitor", "roadmap")
graph.add_edge("roadmap", END)

workflow = graph.compile()