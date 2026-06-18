from backend.agents.idea_agent import run_idea_agent
from backend.agents.market_agent import run_market_agent
from backend.agents.competitor_agent import run_competitor_agent
from backend.agents.roadmap_agent import run_roadmap_agent


def main():
    idea = input("Enter your startup idea: ")

    print("\n🧠 Running Idea Agent...\n")
    idea_result = run_idea_agent(idea)

    print("\n📊 Running Market Agent...\n")
    market_result = run_market_agent(idea_result)

    print("\n⚔️ Running Competitor Agent...\n")
    competitor_result = run_competitor_agent(idea_result, market_result)

    print("\n🗺️ Running Roadmap Agent...\n")
    roadmap_result = run_roadmap_agent(
        idea_result,
        market_result,
        competitor_result
)

    print("\n========================")
    print("ROADMAP OUTPUT")
    print("========================")
    print(roadmap_result.model_dump())


if __name__ == "__main__":
    main()