"""
Integration test for the weather API tool (Google Maps Geocoding + Google Weather API).
This test calls the real APIs and checks for the presence of required fields.
"""

import pytest
import asyncio
from bytemymood.tools.weather import get_current_weather

@pytest.mark.asyncio
async def test_get_current_weather_success():
    """Test real weather data retrieval via Google APIs."""
    result = await get_current_weather("San Francisco", "US")

    assert result["weather_status"] == "success"
    assert "location" in result
    assert "current_weather" in result
    cw = result["current_weather"]
    expected_fields = [
        "temperature", "feels_like", "condition", "condition_text",
        "humidity", "wind_speed", "precipitation_chance", "is_daytime", "uv_index"
    ]
    for field in expected_fields:
        assert field in cw

if __name__ == "__main__":
    asyncio.run(test_get_current_weather_success())
    print("Weather API tool integration tests completed!") 