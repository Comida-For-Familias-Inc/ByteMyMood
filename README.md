# ByteMyMood
Where your feelings feed the recipe.

## Overview
ByteMyMood is an intelligent recipe recommendation system that uses a multi-agent architecture to understand your mood and preferences, plan meals, and execute cooking instructions.

## Features
- **Mood-based recipe recommendations** - AI understands your emotional state
- **Weather-aware suggestions** - Considers current weather conditions
- **Personalized cooking plans** - Adapts to your preferences and skills
- **Visual cooking guidance** - AI-generated images for each step
- **Smart shopping lists** - Paper-like format organized by store sections
- **Equipment verification** - Ensures you have the right tools
- **Robust error handling** - Retry logic for API failures
- **User profile management** - Persistent preferences and mood tracking
- **Recipe verification** - Ensures all suggestions are real and accessible

## Architecture
The system is built on a multi-agent architecture with three specialized sub-agents:

![Agent Architecture](assets/agent-architecture.png)

### 1. Inspiration Agent
- Analyzes user's mood and preferences
- Generates creative recipe ideas
- Considers dietary restrictions and preferences
- Integrates weather data for contextual suggestions
- Verifies recipes through web search
- Located in `bytemymood/sub_agents/inspiration/`

**Tools & Agent-tools:**
- **Weather Check Agent**: Uses `weather_api_tool` to get current weather conditions
- **Recipe Grounding Agent**: Uses `google_search_grounding` to verify recipe authenticity
- **Memory Tools**: `memorize` for storing user preferences and mood data

### 2. Planning Agent
- Breaks down recipes into manageable steps
- Creates detailed cooking plans
- Generates shopping lists
- Analyzes available ingredients from fridge photos
- Verifies kitchen equipment requirements
- Located in `bytemymood/sub_agents/planning/`

**Tools & Agent-tools:**
- **Fridge Agent**: Analyzes available ingredients using `memorize` and `memorize_list`
- **Shopping List Agent**: Generates organized shopping lists using `memorize` and `memorize_list`
- **Memory Tools**: `memorize` and `memorize_list` for tracking ingredients and lists

### 3. Execution Agent
- Provides step-by-step cooking instructions
- Generates visual aids for each cooking step
- Handles real-time adjustments
- Manages cooking process
- Located in `bytemymood/sub_agents/execution/`

**Tools:**
- **Image Generation**: `gemini_image_generation_tool` for creating cooking step visuals
- **Prompt Enhancement**: `prompt_enhance_tool` for optimizing image generation prompts
- **Memory Tools**: `memorize` and `memorize_list` for tracking cooking progress

### Shared Tools & Infrastructure
- **Memory System** (`memory.py`): User profile management and conversation state
- **Weather API** (`weather.py`): Real-time weather data with retry logic
- **Search API** (`search.py`): Recipe verification and web search capabilities
- **Image Generation** (`image_generation/`): Google Gemini-powered visual cooking aids

## Installation Flow

### Step-by-Step Setup

#### 1. Clone and Navigate
```bash
git clone <repository-url>
cd ByteMyMood
```

#### 2. Install uv Package Manager
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

#### 3. Set Up Virtual Environment and Dependencies
```bash
# Create virtual environment and install all dependencies
uv sync

# Install project in editable mode
uv pip install -e .
```

#### 4. Configure API Keys
Create a `.env` file in the project root:
```bash
# Create .env file
touch .env
```

Add your API keys to `.env`:
```env
GOOGLE_API_KEY=your_google_api_key
GOOGLE_GEOCODING_API_KEY=your_geocoding_key
GOOGLE_WEATHER_API_KEY=your_weather_key
```

#### 5. Authenticate Google Cloud
```bash
# Install Google Cloud CLI if not already installed
# https://cloud.google.com/sdk/docs/install

# Authenticate your account
gcloud auth application-default login
```

### Running ByteMyMood

#### Command Line Interface
```bash
# Start ByteMyMood CLI
uv run adk run bytemymood
```

#### Web Interface
```bash
# Launch web interface
uv run adk web
```

## ☁️ Cloud Run Deployment

Deploy ByteMyMood to Google Cloud Run for scalable, serverless hosting with automatic scaling and global distribution.

### 🔧 Prerequisites

Before deploying, ensure you have the following set up:

1. **Google Cloud CLI** installed and configured
2. **Google Cloud Project** with billing enabled
3. **ADK CLI** installed (`pip install google-adk`)

### 🚀 Step 1: Prepare Your Google Cloud Environment

#### Authenticate and Configure gcloud CLI

```bash
# Log in to your GCP account
gcloud auth login

# Set your default project (replace with your actual project ID)
gcloud config set project YOUR_PROJECT_ID

# Set your deployment region
gcloud config set run/region us-central1

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```


### 🚀 Step 2: Create Cloud Run Service via Google Cloud Console

We'll create the Cloud Run service directly through the Google Cloud Console.
#### 2.1 Navigate to Cloud Run Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project from the project dropdown
3. Navigate to **Cloud Run** in the left sidebar
4. Click **"CREATE SERVICE"**

#### 2.2 Configure Service Settings

**Basic Settings:**
- **Service name**: `bytemymood-service`
- **Region**: Choose your preferred region (e.g., `us-central1`)
- **CPU allocation**: `CPU is only allocated during request processing`
- **Memory**: `512 MiB` (recommended for ADK applications)

**Container Settings:**
- **Container image URL**: Leave blank (will be set by ADK deployment)
- **Port**: `8080` (default for Cloud Run)
- **Request timeout**: `300` seconds (5 minutes for AI processing)

#### 2.3 Configure Environment Variables

You have two options for configuring environment variables:

**Option A: Using Google Cloud Console (Recommended)**
Click **"VARIABLES & SECRETS"** and add the following environment variables:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `GOOGLE_GENAI_USE_VERTEXAI` | `TRUE` | Enable Vertex AI for Gemini models |
| `GOOGLE_CLOUD_PROJECT` | `YOUR_PROJECT_ID` | Your Google Cloud project ID |
| `GOOGLE_CLOUD_LOCATION` | `global` | Vertex AI location (keep as global) |
| `GOOGLE_CLOUD_REGION` | `us-central1` | Specific region for Vertex AI |

**Option B: Using .env File**
Create a `.env` file in your project root:

```bash
# Create .env file
touch .env
```

Add the following content to `.env`:
```env
# Cloud Run deployment configuration
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
GOOGLE_CLOUD_REGION=us-central1
```

**Important Notes:**
- Replace `YOUR_PROJECT_ID` with your actual GCP project ID
- `GOOGLE_CLOUD_LOCATION` must remain `global`
- These settings enable your Cloud Run service to access Vertex AI automatically
- If using Option B (.env file), the ADK deployment will automatically read these variables

#### 2.4 Configure Security & Networking

**Authentication:**
- **Authentication**: `Allow unauthenticated invocations` (for public access)
- **Service account**: Use default compute service account

**Networking:**
- **VPC connector**: None (default)
- **Ingress**: `Allow all traffic`

#### 2.5 Advanced Settings (Optional)

**Scaling:**
- **Minimum number of instances**: `0` (for cost optimization)
- **Maximum number of instances**: `100` (adjust based on expected traffic)
- **Concurrency**: `80` (requests per instance)

**Resource Limits:**
- **CPU**: `1` (vCPU)
- **Memory**: `512 MiB`

#### 2.6 Create the Service

1. Review all settings
2. Click **"CREATE"**
3. Wait for the service to be created (this may take a few minutes)

**Note:** The service will be created but won't have a container image yet. We'll deploy the actual application in the next step.

### 🚀 Step 3: Deploy to Cloud Run

Navigate to your ByteMyMood project root directory and run the deployment command:

```bash
# Deploy ByteMyMood to Cloud Run
adk deploy cloud_run \
  --project=YOUR_CLOUD_PROJECT_ID \
  --region=us-central1 \
  --service_name=your-cloud-run-service \
  --with_ui \
  ./bytemymood
```

**Command Parameters:**
- `--project`: Your Google Cloud project ID
- `--region`: Your preferred Cloud Run region
- `--service_name`: Name for your Cloud Run service
- `--with_ui`: Enables the web interface
- `./bytemymood`: Path to your ADK project

## Project Structure
```
bytemymood/
├── agent.py                    
├── prompt.py                   
├── sub_agents/                
│   ├── inspiration/         
│   │   ├── agent.py         
│   │   └── prompt.py         
│   ├── planning/            
│   │   ├── agent.py        
│   │   └── prompt.py         
│   └── execution/            
│       ├── agent.py         
│       └── prompt.py         
├── tools/                    
│   ├── memory.py             
│   ├── weather.py            
│   ├── search.py             
│   └── image_generation/     
│       ├── image_generation.py      
│       └── image_generation_prompt.py 
├── profiles/                  
│   ├── user_profile_default.json           
│   ├── user_profile_example.json           
│   └── user_profile_example_with_recipe.json 
├── shared_libraries/         
│   ├── constants.py         
│   └── types.py              
└── tests/                    
    └── unit/                 
        ├── test_agents.py    
        ├── test_tools.py     
        ├── test_profile.py   
        ├── test_image_generation.py 
        └── test_weather_api.py 
```

## License
See [LICENSE](LICENSE) for details.
