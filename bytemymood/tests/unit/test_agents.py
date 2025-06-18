"""Tests for ByteMyMood agents."""

import unittest
from dotenv import load_dotenv
from google.adk.agents.invocation_context import InvocationContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
import pytest

from bytemymood.agent import root_agent
from bytemymood.sub_agents.inspiration.agent import inspiration_agent
from bytemymood.sub_agents.planning.agent import planning_agent
from bytemymood.sub_agents.execution.agent import execution_agent
from bytemymood.tools.memory import memorize, memorize_list


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()


class TestByteMyMoodAgents(unittest.TestCase):
    """Test cases for ByteMyMood agents."""

    def setUp(self):
        """Set up for test methods."""
        super().setUp()
        self.session = session_service.create_session_sync(
            app_name="ByteMyMood",
            user_id="user123",
        )
        self.user_id = "user123"
        self.session_id = self.session.id

        self.invoc_context = InvocationContext(
            session_service=session_service,
            invocation_id="TEST123",
            agent=root_agent,
            session=self.session,
        )
        self.tool_context = ToolContext(invocation_context=self.invoc_context)

    def test_root_agent_recipe_check(self):
        """Test root agent's recipe checking functionality."""
        # Test with no recipe
        self.assertFalse(self.tool_context.state.get("current_recipe", {}).get("is_verified", False))
        
        # Test with unverified recipe
        memorize(
            key="current_recipe",
            value={
                "name": "Test Recipe",
                "is_verified": False
            },
            tool_context=self.tool_context
        )
        self.assertFalse(self.tool_context.state["current_recipe"]["is_verified"])
        
        # Test with verified recipe
        memorize(
            key="current_recipe",
            value={
                "name": "Test Recipe",
                "is_verified": True
            },
            tool_context=self.tool_context
        )
        self.assertTrue(self.tool_context.state["current_recipe"]["is_verified"])

    def test_inspiration_agent_recipe_verification(self):
        """Test inspiration agent's recipe verification."""
        # Test recipe verification process
        self.invoc_context.agent = inspiration_agent
        # Add test for recipe verification workflow
        pass

    def test_planning_agent_ingredient_check(self):
        """Test planning agent's ingredient checking."""
        # Test ingredient verification process
        self.invoc_context.agent = planning_agent
        # Add test for ingredient checking workflow
        pass

    def test_execution_agent_step_tracking(self):
        """Test execution agent's step tracking."""
        # Test step tracking functionality
        self.invoc_context.agent = execution_agent
        # Add test for step tracking workflow
        pass

    def test_memory_tools(self):
        """Test memory tools functionality."""
        # Test memorize for single values
        result = memorize(
            key="cooking_skill_level",
            value="intermediate",
            tool_context=self.tool_context
        )
        self.assertIn("status", result)
        self.assertEqual(self.tool_context.state["cooking_skill_level"], "intermediate")

        # Test memorize_list for lists
        result = memorize_list(
            key="allergies",
            value="peanuts",
            tool_context=self.tool_context
        )
        self.assertIn("status", result)
        self.assertIn("peanuts", self.tool_context.state["allergies"]) 