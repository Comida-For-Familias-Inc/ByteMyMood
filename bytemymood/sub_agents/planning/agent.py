from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from bytemymood.sub_agents.planning.prompt import PLANNING_AGENT_INSTR, FRIDGE_AGENT_INSTR, SHOPPING_LIST_AGENT_INSTR
from bytemymood.tools.memory import memorize, memorize_list

shopping_list_agent = Agent(
    model="gemini-2.0-flash",
    name="shopping_list_agent",
    description="An agent that generates shopping lists for missing ingredients",
    instruction=SHOPPING_LIST_AGENT_INSTR,
    tools=[memorize, memorize_list],
)

fridge_agent = Agent(
    model="gemini-2.0-flash",
    name="fridge_agent",
    description="An agent that checks available ingredients in the fridge and pantry",
    instruction=FRIDGE_AGENT_INSTR,
    tools=[memorize, memorize_list],
    generate_content_config=GenerateContentConfig(
        temperature=0.1,  # Low temperature for consistent responses
        top_p=0.5  # Moderate top_p for some flexibility while maintaining consistency
    )
) 
planning_agent = Agent(
    model="gemini-2.0-flash",
    name="planning_agent",
    description="A meal planning agent that checks available ingredients, generates shopping lists, and verifies kitchen equipment",
    instruction=PLANNING_AGENT_INSTR,
    tools=[
        AgentTool(agent=fridge_agent),
        AgentTool(agent=shopping_list_agent),
        memorize,
        memorize_list,
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.1, top_p=0.5
    )
)