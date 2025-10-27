## Overview

This AI-powered assistant is engineered to enhance the capabilities of creative agencies when launching new websites or products. The process commences with an intelligent agent that guides users in selecting an optimal DNS domain, ensuring it aligns perfectly with the website's subject matter or the product's identity. Following this foundational step, the workflow culminates with an agent focused on designing distinctive logos that are thematically consistent with the project's core topic. This multi-agent system aims to streamline and augment the creative output of the agency across the entire launch lifecycle.

The agent uses ADK and directs call to models hosted on Vertex AI. 

## Setup and Installation

1.  **Prerequisites**

    *   Python 3.11+
    * A project on Google Cloud Platform
    * Google Cloud CLI
        *   For installation, please follow the instruction on the official
            [Google Cloud website](https://cloud.google.com/sdk/docs/install).

2.  **Installation**

    ```bash
    # Clone this repository.
    git clone https://github.com/lmeka-endava/agentthon-2810.git
    cd agentthon/marketing-agency
    # create a virtual env
    python3 -m venv python3.11-venv
    # activate the virtual env
    source python3.11-venv/bin/activate
    # Install the package and dependencies.
    pip install -r requirements.txt
    ```

3.  **Configuration**

    *   Set up Google Cloud credentials.

        *   You may set the following environment variables in your shell, or in
            a `.env` file instead.

        ```bash
        export GOOGLE_GENAI_USE_VERTEXAI=true
        export GOOGLE_CLOUD_PROJECT=<your-project-id>
        export GOOGLE_CLOUD_LOCATION=australia-southeast1
        export GOOGLE_CLOUD_STORAGE_BUCKET=<your-storage-bucket>  # Only required for deployment on Agent Engine
        ```

    *   Authenticate your GCloud account.

        ```bash
        gcloud auth application-default login
        gcloud auth application-default set-quota-project $GOOGLE_CLOUD_PROJECT
        ```


## Running the Agent locally

**Using `adk`**

ADK provides convenient ways to bring up agents locally and interact with them.
You may talk to the agent using the CLI:

```bash
adk run marketing_agency
```

Or on a web interface:

```bash
 adk web
```

## Deploying to Agent Engine

**Update .env**

Update .env file in root agent folder and all the sub agent folders, to reflect the correct env variables and values.

NOTE : env GEMINI_API_KEY , should be used when ADK agents use models via Google AI API endpoint.

**Deploying a new agent to agent engine**

```bash
cd agentthon/marketing-agency
```bash

```bash
python3 deploy.py create
```

**Deploying an existing agent**

AGENT_RESOURCE_NAME = projects/{PROJECT_ID}/locations/{REGION}/reasoningEngines/{AGENT_ENGINE_ID}

```bash
python3 deploy.py update <AGENT_RESOURCE_NAME>
```

**Get list of agents deployed to agent engine**

```bash
python3 deploy.py list
```

**Deleting an agent deployed to agent engine**
```bash
python3 deploy.py delete
```