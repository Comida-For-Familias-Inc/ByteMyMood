import logging
import os
from typing import Dict, Any, Optional
import uuid
from google.genai import types 
from google import genai
from PIL import Image
from io import BytesIO
from bytemymood.shared_libraries.constants import (
    SAVE_IMAGES_LOCALLY,
    LOCAL_IMAGE_SAVE_PATH
)
from google.adk.tools import ToolContext, FunctionTool
from bytemymood.tools.image_generation import image_generation_prompt
from dotenv import load_dotenv
import asyncio
load_dotenv()

logger = logging.getLogger(__name__)

# Tool function to save image as artifact and conditionally save locally
async def _image_save_func(image_bytes: bytes, file_extension: str, tool_context: ToolContext) -> Dict[str, Any]:
    """Saves image bytes as an ADK artifact and conditionally saves a copy locally."""
    logger.debug("Entering _image_save_func (artifact save version)...")

    # Determine mime type and ensure extension format
    if file_extension and not file_extension.startswith('.'):
        file_extension = '.' + file_extension
    mime_type = f"image/{file_extension.lstrip('.')}" if file_extension else "image/png"
    # Make filename unique for the artifact itself and local copy
    filename = f"generated_image_{uuid.uuid4()}{file_extension if file_extension else '.png'}" 

    # --- Conditional Local Save Logic  --- 
    if SAVE_IMAGES_LOCALLY:
        save_dir = LOCAL_IMAGE_SAVE_PATH
        try:
            os.makedirs(save_dir, exist_ok=True)
            # Use the unique filename generated above for local copy consistency
            local_path = os.path.join(save_dir, filename) 
            
            logger.info(f"Attempting to save image locally to: {local_path} (SAVE_IMAGES_LOCALLY is True)")
            with open(local_path, "wb") as f:
                f.write(image_bytes)
            logger.info(f"Successfully saved image locally to: {local_path}")
        except Exception as e:
            # Log error but don't stop the main process
            logger.warning(f"Local file save failed (path: {save_dir}): {e}", exc_info=False)
    else:
        logger.debug("Local image saving skipped (SAVE_IMAGES_LOCALLY is False).")
    # --- End Conditional Local Save Logic ---
    
    # --- Save as ADK Artifact --- 
    artifact_version = None # Initialize artifact_version variable
    local_path_if_saved = local_path if SAVE_IMAGES_LOCALLY and 'local_path' in locals() else None
    try:
        logger.info(f"Saving {len(image_bytes)} bytes as ADK artifact (name: {filename}, mime: {mime_type})")
        # Create a Part object for the artifact data
        artifact_part = types.Part(inline_data=types.Blob(data=image_bytes, mime_type=mime_type))
        
        # Call save_artifact with filename and artifact keywords 
        logger.debug(f"--->>> PRE-SAVE ARTIFACT CALL (sync) for {filename}")
        artifact_version = await tool_context.save_artifact( 
            filename=filename, 
            artifact=artifact_part 
        )
        # Log using filename and returned version
        logger.info(f"Successfully saved artifact {filename} (version {artifact_version})")
    except Exception as e:
        logger.error(f"Failed to save ADK artifact: {e}", exc_info=True)
        # If artifact saving fails, return specific info if local save happened
        error_msg = f"Failed to save image as artifact: {e}"
        if local_path_if_saved:
             # Return confirmation of local save + artifact error, avoiding generic "error" key
             logger.warning(f"Artifact save failed, but local copy exists at {local_path_if_saved}")
             return {
                 "confirmation": f"Image saved locally to {local_path_if_saved}. Failed to save as artifact: {e}", 
                 "local_path": local_path_if_saved,
                 "artifact_error": str(e) # Specific key for artifact error
             }
        else:
             # Only return generic error if local save didn't happen/succeed
             return {"error": error_msg}
    # --- End Artifact Save ---

    # --- Return confirmation and artifact info (NO raw data) ---
    confirmation_msg = f"Image artifact {filename} (version {artifact_version}) saved successfully."
    if local_path_if_saved:
        confirmation_msg += f" Local copy saved to {local_path_if_saved}."
        
    logger.info("Returning confirmation and artifact info to agent.")
    return {
        "filename": filename, 
        "artifact_version": artifact_version, 
        "confirmation": confirmation_msg
    }
    # --- End Return ---

# Helper function for prompt enhancement 
async def _enhance_prompt_for_image_gen(desc: str) -> Optional[str]:
    """Enhances the user-provided description into a detailed prompt using Gemini."""
    logger.debug(f"Enhancing prompt for description: '{desc}' with Gemini Flash")
    try:
        # Initialize client (API key should be in environment)
        client = genai.Client()
        # Construct the prompt string directly
        prompt_text = (
            "You are a creative image generation assistant. Enhance the following user request "
            f"into a detailed and vivid image generation prompt. User request: '{desc}'\n"
            "Examples:\n"
            f"- {image_generation_prompt.ENHANCE_PROMPT_CHARACTER[0]}\n"
            f"- {image_generation_prompt.ENHANCE_PROMPT_YOUTUBE_THUMBNAIL[0]}\n"
            "Return ONLY the enhanced prompt string."
        )
        logger.debug("Sending prompt to genai.generate_content...")
        # Call generate_content in a thread to avoid blocking the event loop
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.0-flash-001",
            contents=prompt_text,
            config=types.GenerateContentConfig(
                temperature=0.3,
            )
        )
        logger.debug(f"Received response from genai.generate_content, type: {type(response)}")
        # Extract the text from the response safely
        detailed_prompt = None
        try:
            if hasattr(response, 'text'):
                detailed_prompt = response.text
            elif hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            detailed_prompt = part.text
                            break
        except Exception as extract_error:
            logger.error(f"Error extracting text from response: {extract_error}")
            return None
        if not detailed_prompt:
             logger.error(f"Gemini prompt enhancement failed: No text in response")
             return None
        logger.info(f"Enhanced prompt for {desc}: '{detailed_prompt}'")
        # log_prompt_to_file(prompt_text, response, detailed_prompt.strip())
        return detailed_prompt.strip() # Return the string
    except Exception as e:
        logger.error(f"Gemini prompt enhancement failed: {e}", exc_info=True)
        return None # Indicate failure

# Wrap prompt enhancement as a tool
prompt_enhance_tool = FunctionTool(func=_enhance_prompt_for_image_gen)

# --- Gemini Native Image Generation Tool ---
async def _generate_image_with_gemini(desc: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Generates a new image using Gemini's native image generation model based on a text description.
    Use this for creating completely new images from text descriptions.
    Args:
        desc: A detailed text description of the image to generate.
        tool_context: The ADK tool context for accessing state and services.
    Returns:
        A dictionary containing information about the generated image, including
        the artifact name and version where the image is stored.
    """
    try:
        # Initialize Gemini client (API key should be in environment)
        client = genai.Client()
        logger.info(f"Generating image with Gemini using prompt: '{desc}'")
        # Generate image using Gemini's native image generation
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.0-flash-preview-image-generation",
            contents=desc,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        logger.debug(f"Received response from Gemini, type: {type(response)}")
        # Extract image data from response safely
        image_data = None
        try:
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'inline_data') and part.inline_data and hasattr(part.inline_data, 'data'):
                            image_data = part.inline_data.data
                            logger.debug(f"Found image data: {len(image_data)} bytes")
                            break
        except Exception as extract_error:
            logger.error(f"Error extracting image data: {extract_error}")
            return {"error": f"Failed to extract image data: {extract_error}"}
        if not image_data:
            logger.error("No image data found in Gemini response")
            return {"error": "No image data generated by Gemini"}
        # Convert PIL Image to bytes for saving
        try:
            image = Image.open(BytesIO(image_data))
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
        except Exception as image_error:
            logger.error(f"Error processing image data: {image_error}")
            return {"error": f"Failed to process image data: {image_error}"}
        # Save the image as artifact and locally
        artifact_result = await _image_save_func(img_byte_arr, ".png", tool_context)
        logger.info(f"Generate artifact save result keys: {artifact_result.keys()}")
        # Return the result
        if "error" in artifact_result or "artifact_error" in artifact_result:
             error_key = "error" if "error" in artifact_result else "artifact_error"
             confirm = artifact_result.get("confirmation", "Image generated but artifact save failed.") + f" Error: {artifact_result.get(error_key)}"
             return {"confirmation": confirm, "artifact_error": artifact_result.get(error_key)}
        else:
            return artifact_result
    except Exception as e:
        logger.error(f"Gemini image generation failed: {e}", exc_info=True)
        return {"error": str(e)}

# Create the FunctionTool for Gemini image generation
gemini_image_generation_tool = FunctionTool(func=_generate_image_with_gemini)
