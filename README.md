# ByteMyMood
Where your feelings feed the recipe.

## Overview
ByteMyMood is an intelligent recipe recommendation system that uses a multi-agent architecture to understand your mood and preferences, plan meals, and execute cooking instructions.

## Architecture
The system is built on a multi-agent architecture with three specialized sub-agents:

### 1. Inspiration Agent
- Analyzes user's mood and preferences
- Generates creative recipe ideas
- Considers dietary restrictions and preferences
- Located in `bytemymood/sub_agents/inspiration/`

### 2. Planning Agent
- Breaks down recipes into manageable steps
- Creates detailed cooking plans
- Optimizes cooking sequence
- Located in `bytemymood/sub_agents/planning/`

### 3. Execution Agent
- Provides step-by-step cooking instructions
- Handles real-time adjustments
- Manages cooking process
- Located in `bytemymood/sub_agents/execution/`

## Project Structure
```
bytemymood/
├── agent.py              # Main agent orchestration
├── prompt.py            # System prompts and templates
├── sub_agents/          # Specialized agent implementations
│   ├── inspiration/     # Mood and recipe inspiration
│   ├── planning/        # Recipe planning and organization
│   └── execution/       # Cooking execution and guidance
├── tools/               # Shared tools and utilities
├── profiles/            # User profile management
├── shared_libraries/    # Common utilities and constants
└── tests/              # Unit and integration tests
```

## Features
- Mood-based recipe recommendations
- Personalized cooking plans
- Step-by-step cooking guidance
- User profile management
- Dietary preference tracking
- Kitchen equipment awareness

## Getting Started
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Set up your environment variables in `.env`
4. Run the tests:
   ```bash
   pytest
   ```

## Development
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Use conventional commits

## License
See [LICENSE](LICENSE) for details.
