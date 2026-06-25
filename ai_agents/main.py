from ai_agents.workflow import workflow


def main():

    idea = input("Enter your startup idea: ")

    result = workflow.invoke({
        "idea": idea
    })

    print("\n========================")
    print("ROADMAP OUTPUT")
    print("========================")

    roadmap_result = result.get("roadmap_result")

    if roadmap_result:
        print(roadmap_result.model_dump())
    else:
        print("Roadmap generation failed.")


if __name__ == "__main__":
    main()