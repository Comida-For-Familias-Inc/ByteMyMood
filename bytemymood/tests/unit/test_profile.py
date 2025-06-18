"""Tests for ByteMyMood user profile functionality."""

import unittest
import json
import os
from dotenv import load_dotenv
from google.adk.agents.invocation_context import InvocationContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
import pytest

from bytemymood.agent import root_agent
from bytemymood.tools.memory import memorize, memorize_list, _set_initial_states, _load_user_profile
from bytemymood.shared_libraries.constants import (
    USER_PROFILE,
    ALLERGIES,
    DIETARY_PREFERENCES,
    COOKING_SKILL_LEVEL,
    EQUIPMENT_AVAILABLE,
    TIME_CONSTRAINTS,
    MEAL_PREFERENCES,
    KITCHEN_EQUIPMENT,
    CURRENT_RECIPE,
    RECIPE_NAME,
    SOURCE_URL,
    INGREDIENTS,
    INSTRUCTIONS,
    PREP_TIME,
    COOK_TIME,
    SERVINGS,
    VERIFICATION_STATUS,
    IS_VERIFIED
)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()


class TestByteMyMoodProfile(unittest.TestCase):
    """Test cases for ByteMyMood user profile."""

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

        # Initialize state with default profile values using _set_initial_states
        profile_path = os.getenv("BYTEMYMOOD_PROFILE", "bytemymood/profiles/user_profile_default.json")
        with open(profile_path, "r") as f:
            default_profile = json.load(f)
            _set_initial_states(default_profile["state"], self.tool_context.state)

    def test_default_profile_initialization(self):
        """Test default profile initialization."""
        # Check if default profile exists
        profile_path = os.getenv("BYTEMYMOOD_PROFILE", "bytemymood/profiles/user_profile_default.json")
        self.assertTrue(os.path.exists(profile_path))

        # Load and verify default profile structure
        with open(profile_path, "r") as f:
            profile = json.load(f)
            self.assertIn("state", profile)
            self.assertIn(CURRENT_RECIPE, profile["state"])
            self.assertFalse(profile["state"][CURRENT_RECIPE][IS_VERIFIED])
            self.assertEqual(profile["state"][CURRENT_RECIPE][RECIPE_NAME], "")
            self.assertEqual(profile["state"][CURRENT_RECIPE][SOURCE_URL], "")
            self.assertEqual(profile["state"][CURRENT_RECIPE][INGREDIENTS], [])
            self.assertEqual(profile["state"][CURRENT_RECIPE][INSTRUCTIONS], [])
            self.assertEqual(profile["state"][CURRENT_RECIPE][PREP_TIME], "")
            self.assertEqual(profile["state"][CURRENT_RECIPE][COOK_TIME], "")
            self.assertEqual(profile["state"][CURRENT_RECIPE][SERVINGS], "")
            self.assertEqual(profile["state"][CURRENT_RECIPE][VERIFICATION_STATUS], "")

    def test_profile_updates(self):
        """Test updating user profile information."""
        # Test updating cooking skill level
        memorize(
            key=COOKING_SKILL_LEVEL,
            value="advanced",
            tool_context=self.tool_context
        )
        self.assertEqual(self.tool_context.state[COOKING_SKILL_LEVEL], "advanced")

        # Test updating allergies
        memorize_list(
            key=ALLERGIES,
            value="peanuts",
            tool_context=self.tool_context
        )
        self.assertIn("peanuts", self.tool_context.state[ALLERGIES])

        # Test updating dietary preferences
        memorize_list(
            key=DIETARY_PREFERENCES,
            value="vegetarian",
            tool_context=self.tool_context
        )
        self.assertIn("vegetarian", self.tool_context.state[DIETARY_PREFERENCES])

    def test_recipe_verification(self):
        """Test recipe verification in profile."""
        # Test initial recipe state
        self.assertFalse(self.tool_context.state[CURRENT_RECIPE][IS_VERIFIED])

        # Test updating recipe
        recipe = {
            RECIPE_NAME: "Test Recipe",
            SOURCE_URL: "https://example.com/recipe",
            INGREDIENTS: ["ingredient1", "ingredient2"],
            INSTRUCTIONS: ["step1", "step2"],
            PREP_TIME: "30 minutes",
            COOK_TIME: "1 hour",
            SERVINGS: "4",
            VERIFICATION_STATUS: "verified",
            IS_VERIFIED: True
        }
        memorize(
            key=CURRENT_RECIPE,
            value=recipe,
            tool_context=self.tool_context
        )
        self.assertTrue(self.tool_context.state[CURRENT_RECIPE][IS_VERIFIED])
        self.assertEqual(self.tool_context.state[CURRENT_RECIPE][RECIPE_NAME], "Test Recipe")

    def test_equipment_tracking(self):
        """Test kitchen equipment tracking."""
        # Test adding equipment
        memorize_list(
            key=EQUIPMENT_AVAILABLE,
            value="blender",
            tool_context=self.tool_context
        )
        self.assertIn("blender", self.tool_context.state[EQUIPMENT_AVAILABLE])

        # Test adding multiple equipment
        equipment = ["oven", "microwave", "toaster"]
        for item in equipment:
            memorize_list(
                key=EQUIPMENT_AVAILABLE,
                value=item,
                tool_context=self.tool_context
            )
        for item in equipment:
            self.assertIn(item, self.tool_context.state[EQUIPMENT_AVAILABLE]) 