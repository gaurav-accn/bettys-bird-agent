import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from toolbox_core import ToolboxSyncClient

from .datastore import search_store_documents
from .search_agent import search_tool

load_dotenv()

# Configure session service
session_service = InMemorySessionService()

# Read agent instructions
script_dir = Path(__file__).parent
instruction = (script_dir / "agent-prompt.txt").read_text()

# Connect to Google Gen AI Toolbox
toolbox_url = os.getenv("TOOLBOX_URL", "http://127.0.0.1:5000")
toolbox = ToolboxSyncClient(toolbox_url)

# Load MySQL product price tool
get_product_price = toolbox.load_tool("get-product-price")

# Configure tools
tools = [
    get_product_price,
    search_store_documents,
    search_tool,
]

# Create root agent
root_agent = Agent(
    name="bettys_bird_boutique_agent",
    model="gemini-3.8-flash",
    description="Customer service agent for Betty's Bird Boutique.",
    instruction=instruction,
    tools=tools,
)