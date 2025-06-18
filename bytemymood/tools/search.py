# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrapper to Google Search Grounding with custom prompt."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from google.adk.tools.google_search_tool import google_search
# from google.adk.tools.langchain_tool import LangchainTool
# from langchain_community.tools import TavilySearchResults

_search_agent = Agent(
    model="gemini-2.0-flash",
    name="google_search_grounding",
    description="An agent providing Google-search grounding capability for verifying information from the internet",
    instruction="I can answer your questions by searching the internet. Just ask me anything!",  
    tools=[google_search],
)


# # Instantiate LangChain tool
# tavily_search = TavilySearchResults(
#     max_results=5,
#     search_depth="advanced",
#     include_answer=True,
#     include_raw_content=True,
#     include_images=True,
# )

# # Wrap with LangchainTool
# adk_tavily_tool = LangchainTool(tool=tavily_search)

# # Define Agent with the wrapped tool
# _tavily_search_agent = Agent(
#     name="langchain_tool_agent",
#     model="gemini-2.0-flash",
#     description="Agent to answer questions using TavilySearch.",
#     instruction="I can answer your questions by searching the internet. Just ask me anything!",
#     tools=[adk_tavily_tool] # Add the wrapped tool here
# )

# Switch between the two search agents
google_search_grounding = AgentTool(agent=_search_agent)
# google_search_grounding = AgentTool(agent=_tavily_search_agent)