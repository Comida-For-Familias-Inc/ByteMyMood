from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from bytemymood.sub_agents.execution.prompt import EXECUTION_AGENT_INSTR
from bytemymood.tools.memory import memorize, memorize_list

execution_agent = Agent(
    model="gemini-2.0-flash",
    name="execution_agent",
    description="A meal recipe execution agent who guides users through recipes step by step",
    instruction=EXECUTION_AGENT_INSTR,
    tools=[
        memorize,  # For storing progress and preferences
        memorize_list,  # For tracking completed steps
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.1,  # Low temperature for consistent responses
        top_p=0.5  # Moderate top_p for some flexibility while maintaining consistency
    )
)