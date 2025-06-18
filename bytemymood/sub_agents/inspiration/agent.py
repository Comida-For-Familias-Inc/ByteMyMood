from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from bytemymood.sub_agents.inspiration.prompt import INSPIRATION_AGENT_INSTR, RECIPE_GROUNDING_AGENT_INSTR, WEATHER_CHECK_AGENT_INSTR
from bytemymood.tools.memory import memorize
from bytemymood.tools.search import google_search_grounding

weather_check_agent = Agent(
    model="gemini-2.0-flash",
    name="weather_check_agent",
    description="An agent that checks current weather and temperature for recipe suggestions",
    instruction=WEATHER_CHECK_AGENT_INSTR,
    tools=[google_search_grounding],
)

recipe_grounding_agent = Agent(
    model="gemini-2.0-flash",
    name="recipe_grounding_agent",
    description="A recipe verification agent that ensures all suggested recipes exist in real-world sources by searching the internet",
    instruction=RECIPE_GROUNDING_AGENT_INSTR,
    tools=[google_search_grounding],
)

inspiration_agent = Agent(
    model="gemini-2.0-flash",
    name="inspiration_agent",
    description="A meal recipe inspiration agent who inspire users, and discover the next meal recipe",
    instruction=INSPIRATION_AGENT_INSTR,
    tools=[
        AgentTool(agent=weather_check_agent),
        AgentTool(agent=recipe_grounding_agent),
        memorize,
    ],
)