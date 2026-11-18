
import os

from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.google_search_agent_tool import GoogleSearchAgentTool


# Read the instructions from search-prompt.txt
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "search-prompt.txt")

with open(instruction_file_path, "r") as f:
    instruction = f.read()


# Create the Google Search sub-agent
search_agent = Agent(
    name="google_search_agent",
    model="gemini-3.8-flash",
    description="Specialist agent that searches the web using Google Search.",
    instruction=instruction,
    tools=[google_search],
)


# Wrap the sub-agent so the main agent can use it as a tool
search_tool = GoogleSearchAgentTool(agent=search_agent)
