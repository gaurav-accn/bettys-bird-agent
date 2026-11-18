import os

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService

# Configure short-term session to use the in-memory service.
# The agent only needs to remember the current conversation,
# not previous ones, so in-memory storage is enough.
session_service = InMemorySessionService()

# Read the instructions from a file in the same
# directory as this agent.py file.
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

# Set up the tools that we will be using for the root agent
# (database, datastore search and web search tools get added later)
tools = []

# Create our agent.
# Model choice: gemini-2.5-flash gives reliable tool calling with low
# latency and cost, which suits a customer-facing chat agent.
# (Update this comment after comparing 2.5-pro, 2.5-flash, 2.5-flash-lite.)
root_agent = Agent(
    name="bettys_bird_boutique_agent",
    model="gemini-2.5-flash",
    description="Customer service agent for Betty's Bird Boutique, answering questions about the store, its products and birds.",
    instruction=instruction,
    tools=tools,
)
