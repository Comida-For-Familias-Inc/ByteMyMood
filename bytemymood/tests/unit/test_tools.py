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

"""Tests for ByteMyMood tools."""

import unittest
from dotenv import load_dotenv
from google.adk.agents.invocation_context import InvocationContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext
import pytest

from bytemymood.agent import root_agent
from bytemymood.tools.memory import memorize, memorize_list, forget
from bytemymood.tools.search import google_search_grounding
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


class TestByteMyMoodTools(unittest.TestCase):
    """Test cases for ByteMyMood tools."""

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

    def test_memorize_single_value(self):
        """Test memorizing a single value."""
        result = memorize(
            key=COOKING_SKILL_LEVEL,
            value="advanced",
            tool_context=self.tool_context
        )
        self.assertEqual(self.tool_context.state[COOKING_SKILL_LEVEL], "advanced")
        self.assertIn("Stored", result["status"])

    def test_memorize_list(self):
        """Test memorizing list values."""
        # Test adding to empty list
        result = memorize_list(
            key=ALLERGIES,
            value="peanuts",
            tool_context=self.tool_context
        )
        self.assertIn("peanuts", self.tool_context.state[ALLERGIES])
        self.assertIn("Stored", result["status"])

        # Test adding to existing list
        result = memorize_list(
            key=ALLERGIES,
            value="shellfish",
            tool_context=self.tool_context
        )
        self.assertIn("shellfish", self.tool_context.state[ALLERGIES])
        self.assertIn("Stored", result["status"])

        # Test adding duplicate
        result = memorize_list(
            key=ALLERGIES,
            value="peanuts",
            tool_context=self.tool_context
        )
        self.assertEqual(self.tool_context.state[ALLERGIES].count("peanuts"), 1)
        self.assertIn("Stored", result["status"])

    def test_forget(self):
        """Test forgetting values."""
        # First add some values
        memorize_list(
            key=ALLERGIES,
            value="peanuts",
            tool_context=self.tool_context
        )
        memorize_list(
            key=ALLERGIES,
            value="shellfish",
            tool_context=self.tool_context
        )

        # Then forget one
        result = forget(
            key=ALLERGIES,
            value="peanuts",
            tool_context=self.tool_context
        )
        self.assertNotIn("peanuts", self.tool_context.state[ALLERGIES])
        self.assertIn("shellfish", self.tool_context.state[ALLERGIES])
        self.assertIn("Removed", result["status"])

    def test_google_search_grounding(self):
        """Test Google search grounding tool."""
        # Test recipe search
        result = google_search_grounding.func(
            query="simple chocolate cake recipe",
            tool_context=self.tool_context
        )
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertIsInstance(result[0], str)

        # Test weather search
        result = google_search_grounding.func(
            query="current weather in New York",
            tool_context=self.tool_context
        )
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertIsInstance(result[0], str)
