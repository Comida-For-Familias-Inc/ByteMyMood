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

"""The 'memorize' tool for several agents to affect session states."""

from datetime import datetime
import json
import os
from typing import Dict, Any

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

from bytemymood.shared_libraries import constants

SAMPLE_PROFILE_PATH = os.path.join(os.path.dirname(__file__), "../user_profiles/user_profile_default.json")



def memorize_list(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information as a list.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    if key not in mem_dict:
        mem_dict[key] = []
    if value not in mem_dict[key]:
        mem_dict[key].append(value)
    return {"status": f'Stored "{key}": "{value}"'}


def memorize(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information, one key-value pair at a time.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    mem_dict[key] = value
    print(f"Stored {key}: {value}")
    return {"status": f'Stored "{key}": "{value}"'}


def forget(key: str, value: str, tool_context: ToolContext):
    """
    Forget pieces of information.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be removed.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    if tool_context.state[key] is None:
        tool_context.state[key] = []
    if value in tool_context.state[key]:
        tool_context.state[key].remove(value)
    return {"status": f'Removed "{key}": "{value}"'}


def _set_initial_states(source: Dict[str, Any], target: State | dict[str, Any]):
    """
    Setting the initial session state given a JSON object of states.
    Handles nested JSON structures by recursively copying values.

    Args:
        source: A JSON object of states.
        target: The session state object to insert into.
    """
    if constants.SYSTEM_TIME not in target:
        target[constants.SYSTEM_TIME] = str(datetime.now())

    if constants.USER_PROFILE not in target:
        target[constants.USER_PROFILE] = True

        # Recursively copy all values from source to target
        for key, value in source.items():
            if isinstance(value, dict):
                # For nested dictionaries, create a new dict and recursively copy
                target[key] = {}
                _set_initial_states(value, target[key])
            elif isinstance(value, list):
                # For lists, create a new list with copied values
                target[key] = value.copy()
            else:
                # For primitive values, copy directly
                target[key] = value


def _load_user_profile(callback_context: CallbackContext):
    """
    Sets up the initial user profile state.
    Set this as a callback as before_agent_call of the root_agent.
    This gets called before the system instruction is constructed.

    Args:
        callback_context: The callback context.
    """    
    data = {}
    with open(SAMPLE_PROFILE_PATH, "r") as file:
        data = json.load(file)
        # print(f"\nLoading User Profile: {data}\n")

    _set_initial_states(data["state"], callback_context.state)
