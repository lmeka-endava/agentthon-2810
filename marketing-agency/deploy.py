import os
import fire
from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

from marketing_agency.agent import root_agent

# Load environment variables and initialize Vertex AI
load_dotenv()

#project=os.getenv("GOOGLE_CLOUD_PROJECT"),
GOOGLE_CLOUD_PROJECT=os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION=os.getenv("GOOGLE_CLOUD_LOCATION")
GOOGLE_CLOUD_STORAGE_BUCKET=os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
GOOGLE_GENAI_USE_VERTEXAI=os.getenv("GOOGLE_GENAI_USE_VERTEXAI")


# Initialise vertex AI
vertexai.init(
    project=GOOGLE_CLOUD_PROJECT,
    location=GOOGLE_CLOUD_LOCATION,
    staging_bucket=f"gs://{GOOGLE_CLOUD_STORAGE_BUCKET}"
)

# Wrap the agent in an AdkApp object
#app = agent_engines.AdkApp(agent=root_agent,enable_tracing=True,)
adk_app = AdkApp(agent=root_agent, enable_tracing=True)

# deplopy an agent to agent engine

def create() -> None:
    """Creates an agent engine for Marketing Agency."""

    remote_agent = agent_engines.create(
        agent_engine=adk_app,
        display_name=root_agent.name,
        description = "adk marketing agent",
        requirements= [
            "google-adk (>=0.0.2)",
            "google-cloud-aiplatform[agent_engines] (>=1.91.0,!=1.92.0)",
            "google-genai (>=1.5.0,<2.0.0)",
            "pydantic (>=2.10.6,<3.0.0)",
            "absl-py (>=2.2.1,<3.0.0)",
        ],
        extra_packages=[
            "./marketing_agency",
        ],
        #env_vars={"key":"value"},
        min_instances= 1,
        max_instances= 2,
        resource_limits= {"cpu": "4", "memory": "8Gi"},
        gcs_dir_name="agent_engine/marketing_agency",
        #labels = {"version": "latest"}
    )
    
    print(f"Created remote agent: {remote_agent.resource_name}")

# list the agents deployed onto agent engine for the project
def list():
    """
    List Agent Engine agents.
        
    Example:
    agent_engine_utils list
    """
    for agent in agent_engines.list():
        print(agent.display_name)
        print(agent.resource_name + "\n")

# update an agent deployed onto agent engine for the project

def update(resource_name: str) -> None:
    """
    Updates an existing agent engine with new code or configuration.

    Args:
        resource_name: The full resource path of the agent to update 
                       (e.g., projects/P_ID/locations/LOC/reasoningEngines/R_ID).
    """
    if not resource_name:
        print("Error: resource_name is required for the update function.")
        return
    
    agent = agent_engines.get(resource_name)

    updated_agent = agent.update(
        agent_engine=adk_app,  # Contains the latest code of the root agent
        display_name=root_agent.name,
        requirements= [
            "google-adk (>=0.0.2)",
            "google-cloud-aiplatform[agent_engines] (>=1.91.0,!=1.92.0)",
            "google-genai (>=1.5.0,<2.0.0)",
            "pydantic (>=2.10.6,<3.0.0)",
            "absl-py (>=2.2.1,<3.0.0)",
        ],
        extra_packages=[
            "./marketing_agency",
        ],
        min_instances=1,
        max_instances=2,
        resource_limits={"cpu": "4", "memory": "8Gi"},
        gcs_dir_name="agent_engine/marketing_agency"
        # NOTE: Only pass parameters you wish to change.
    )
    
    print(f"Updated remote agent: {updated_agent.resource_name}")
    print("Deployment update process initiated.")

# delete a specific agent deployed onto agent engine
def delete(resource_name):
    """
    Delete an Agent Engine agent by its resource_name.
    
    Example:
    agent_engine_utils delete projects/MY_PROJECT_ID/locations/MY_REGION/reasoningEngines/NUMERICAL_ID
    """
    agent_engines.delete(resource_name, force=True)

if __name__ == "__main__":
    fire.Fire()