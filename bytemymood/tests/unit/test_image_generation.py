#!/usr/bin/env python3
"""
Pytest test for local image generation using Gemini.
This test will generate a test image and save it locally for verification.
"""

import pytest
import asyncio
import os
from dotenv import load_dotenv
from bytemymood.tools.image_generation.image_generation import _generate_image_with_gemini, _enhance_prompt_for_image_gen
from unittest.mock import Mock

# Load environment variables
load_dotenv()

class MockToolContext:
    """Mock tool context for local testing."""
    def __init__(self):
        self.artifacts = {}
        self.artifact_counter = 0
    
    def save_artifact(self, filename, artifact):
        """Mock artifact saving - just store in memory for testing."""
        self.artifact_counter += 1
        self.artifacts[filename] = {
            'data': artifact.inline_data.data,
            'mime_type': artifact.inline_data.mime_type,
            'version': self.artifact_counter
        }
        return self.artifact_counter

class TestImageGenerationLocal:
    """Test class for local image generation functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment."""
        # Check if Google API key is available
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            pytest.skip("GOOGLE_API_KEY not found in environment variables")
        
        # Create mock tool context
        self.mock_context = MockToolContext()
    
    @pytest.mark.asyncio
    async def test_prompt_enhancement(self):
        """Test prompt enhancement functionality."""
        print("\n🔄 Testing prompt enhancement...")
        test_description = "a delicious chocolate chip cookie on a white plate"
        enhanced_prompt = await _enhance_prompt_for_image_gen(test_description)
        
        if enhanced_prompt:
            print(f"✅ Prompt enhanced successfully:")
            print(f"   Original: '{test_description}'")
            print(f"   Enhanced: '{enhanced_prompt}'")
            assert enhanced_prompt != test_description
            assert len(enhanced_prompt) > len(test_description)
        else:
            print("❌ Prompt enhancement failed, using original description")
            enhanced_prompt = test_description
        
        return enhanced_prompt
    
    @pytest.mark.asyncio
    async def test_image_generation(self):
        """Test image generation functionality."""
        print("\n🎨 Testing image generation...")
        detailed_prompt = "A beautiful, freshly baked chocolate chip cookie on a white ceramic plate, with melted chocolate chips, golden brown edges, soft center, high quality food photography, natural lighting"
        
        result = await _generate_image_with_gemini(detailed_prompt, self.mock_context)
        
        if "error" in result:
            pytest.fail(f"Image generation failed: {result['error']}")
        
        if "artifact_error" in result:
            print(f"⚠️  Image generated but artifact save failed: {result['artifact_error']}")
            if "local_path" in result:
                print(f"✅ Local copy saved to: {result['local_path']}")
                assert os.path.exists(result['local_path'])
        else:
            print("✅ Image generated successfully!")
            print(f"   Filename: {result.get('filename', 'N/A')}")
            print(f"   Artifact version: {result.get('artifact_version', 'N/A')}")
            if "local_path" in result:
                print(f"   Local path: {result['local_path']}")
                assert os.path.exists(result['local_path'])
        
        # Check if we have artifacts in our mock context
        if self.mock_context.artifacts:
            print(f"\n📊 Mock artifacts created: {len(self.mock_context.artifacts)}")
            for filename, artifact_info in self.mock_context.artifacts.items():
                print(f"   - {filename}: {len(artifact_info['data'])} bytes ({artifact_info['mime_type']})")
                assert len(artifact_info['data']) > 0
        
        return result
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test the complete workflow: prompt enhancement + image generation."""
        print("\n🚀 Testing full workflow...")
        
        # Test prompt enhancement
        enhanced_prompt = await self.test_prompt_enhancement()
        
        # Test image generation with the enhanced prompt from step 1
        print(f"\n🎨 Generating image with enhanced prompt: '{enhanced_prompt}'")
        result = await _generate_image_with_gemini(enhanced_prompt, self.mock_context)
        
        if "error" in result:
            pytest.fail(f"Image generation failed: {result['error']}")
        
        if "artifact_error" in result:
            print(f"⚠️  Image generated but artifact save failed: {result['artifact_error']}")
            if "local_path" in result:
                print(f"✅ Local copy saved to: {result['local_path']}")
                assert os.path.exists(result['local_path'])
        else:
            print("✅ Image generated successfully!")
            print(f"   Filename: {result.get('filename', 'N/A')}")
            print(f"   Artifact version: {result.get('artifact_version', 'N/A')}")
            if "local_path" in result:
                print(f"   Local path: {result['local_path']}")
                assert os.path.exists(result['local_path'])
        
        # Check if we have artifacts in our mock context
        if self.mock_context.artifacts:
            print(f"\n📊 Mock artifacts created: {len(self.mock_context.artifacts)}")
            for filename, artifact_info in self.mock_context.artifacts.items():
                print(f"   - {filename}: {len(artifact_info['data'])} bytes ({artifact_info['mime_type']})")
                assert len(artifact_info['data']) > 0
        
        print(f"\n🎉 Full workflow test completed!")
        print(f"Check the local_image_results/ directory for the generated image.")
        
        return result

# For running the test directly (not through pytest)
async def run_manual_test():
    """Manual test runner for when pytest is not available."""
    print("🚀 Starting manual image generation test with Gemini...")
    
    # Check if Google API key is available
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google API key in the .env file")
        return
    
    print("🔑 Google API key found")
    
    # Create test instance and run tests
    test_instance = TestImageGenerationLocal()
    test_instance.setup()
    
    try:
        await test_instance.test_full_workflow()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_manual_test()) 