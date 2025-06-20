from google.adk.agents import Agent
from bytemymood.tools.memory import _load_user_profile, memorize
from bytemymood.sub_agents.inspiration.agent import inspiration_agent
from bytemymood.sub_agents.planning.agent import planning_agent
from bytemymood.sub_agents.execution.agent import execution_agent

from bytemymood import prompt



root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="root_agent",
    description="A multi-agent recipe planning system",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        inspiration_agent,
        planning_agent,
        execution_agent
    ],
    tools=[
        memorize,
    ],
    before_agent_callback=_load_user_profile,
)