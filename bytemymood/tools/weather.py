"""
Weather API tool using Google Maps Geocoding and Google Weather API for real-time weather data.
Returns fields most relevant for recipe inspiration.
"""

import logging
import os
import httpx
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
from google.adk.tools import FunctionTool

load_dotenv()

logger = logging.getLogger(__name__)

GOOGLE_GEOCODING_API_KEY = os.getenv("GOOGLE_GEOCODING_API_KEY")
GOOGLE_WEATHER_API_KEY = os.getenv("GOOGLE_WEATHER_API_KEY")
GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
GOOGLE_WEATHER_URL = "https://weather.googleapis.com/v1/currentConditions:lookup"

async def get_current_weather(city: str, country: Optional[str] = None) -> Dict[str, Any]:
    """
    Get current weather data for a specific city using Google Maps Geocoding and Google Weather API.
    Returns only the most relevant fields for recipe inspiration:
      - temperature, feels_like, condition, condition_text, humidity, wind_speed,
        precipitation_chance, is_daytime, uv_index
    """
    try:
        if not GOOGLE_GEOCODING_API_KEY:
            return {"error": "Google Maps API key not configured. Please set GOOGLE_GEOCODING_API_KEY in your .env file."}
        if not GOOGLE_WEATHER_API_KEY:
            return {"error": "Google Weather API key not configured. Please set GOOGLE_WEATHER_API_KEY in your .env file."}

        # 1. Geocode city/country to lat/lon
        location_query = city
        if country:
            location_query = f"{city},{country}"
        geo_params = {
            "address": location_query,
            "key": GOOGLE_GEOCODING_API_KEY
        }
        async with httpx.AsyncClient() as client:
            geo_resp = await client.get(GOOGLE_GEOCODE_URL, params=geo_params, timeout=10)
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return {"error": f"Could not geocode location: {location_query}"}
        geo_result = geo_data["results"][0]
        lat = geo_result["geometry"]["location"]["lat"]
        lon = geo_result["geometry"]["location"]["lng"]
        resolved_city = None
        resolved_country = None
        for comp in geo_result.get("address_components", []):
            if "locality" in comp["types"]:
                resolved_city = comp["long_name"]
            if "country" in comp["types"]:
                resolved_country = comp["short_name"]
        if not resolved_city:
            resolved_city = city
        if not resolved_country:
            resolved_country = country

        logger.info(f"Geocoded {location_query} to lat={lat}, lon={lon}")

        # 2. Call Google Weather API
        weather_params = {
            "key": GOOGLE_WEATHER_API_KEY,
            "location.latitude": lat,
            "location.longitude": lon
        }
        async with httpx.AsyncClient() as client:
            weather_resp = await client.get(GOOGLE_WEATHER_URL, params=weather_params, timeout=10)
            weather_resp.raise_for_status()
            weather_data = weather_resp.json()

        # 3. Parse weather data (Google's response structure)
        # See: https://developers.google.com/maps/documentation/weather/reference/rest/v1/currentConditions/lookup
        # Example fields: temperature, feelsLikeTemperature, weatherCondition, relativeHumidity, wind, precipitation, isDaytime, uvIndex
        try:
            # Google Weather API may return either a 'currentConditions' list or a flat dict
            if "currentConditions" in weather_data and weather_data["currentConditions"]:
                current = weather_data["currentConditions"][0]
            else:
                current = weather_data
        except (KeyError, IndexError):
            return {"error": f"Unexpected Google Weather API response: {weather_data}"}

        # Extract relevant fields for recipe inspiration
        temperature = current.get("temperature", {}).get("degrees")
        feels_like = current.get("feelsLikeTemperature", {}).get("degrees")
        condition = current.get("weatherCondition", {}).get("type")
        condition_text = current.get("weatherCondition", {}).get("description", {}).get("text")
        humidity = current.get("relativeHumidity")
        wind_speed = current.get("wind", {}).get("speed", {}).get("value")
        precipitation_chance = current.get("precipitation", {}).get("probability", {}).get("percent")
        is_daytime = current.get("isDaytime")
        uv_index = current.get("uvIndex")

        # Format for human-friendly output
        current_weather = {
            "temperature": f"{temperature:.1f}°C" if temperature is not None else None,
            "feels_like": f"{feels_like:.1f}°C" if feels_like is not None else None,
            "condition": condition,
            "condition_text": condition_text,
            "humidity": f"{humidity}%" if humidity is not None else None,
            "wind_speed": f"{wind_speed} km/h" if wind_speed is not None else None,
            "precipitation_chance": f"{precipitation_chance}%" if precipitation_chance is not None else None,
            "is_daytime": is_daytime,
            "uv_index": uv_index
        }
        location = {
            "city": resolved_city,
            "country": resolved_country,
            "coordinates": {"lat": lat, "lon": lon}
        }
        result = {
            "weather_status": "success",
            "location": location,
            "current_weather": current_weather,
            "verification_details": {
                "source": "Google Weather API",
                "timestamp": datetime.now().isoformat(),
                "is_current": True,
                "api_response_time": weather_resp.elapsed.total_seconds() if hasattr(weather_resp, 'elapsed') else None
            },
            "error_message": None
        }
        logger.info(f"Successfully retrieved weather data for {location_query}: {current_weather['temperature']}, {current_weather['condition_text']}")
        return result
    except httpx.RequestError as e:
        error_msg = f"Failed to fetch weather data: {str(e)}"
        logger.error(error_msg)
        return {
            "weather_status": "failed",
            "location": {"city": city, "country": country},
            "current_weather": None,
            "verification_details": {
                "source": "Google Weather API",
                "timestamp": datetime.now().isoformat(),
                "is_current": False,
                "error": str(e)
            },
            "error_message": error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {
            "weather_status": "failed",
            "location": {"city": city, "country": country},
            "current_weather": None,
            "verification_details": {
                "source": "Google Weather API",
                "timestamp": datetime.now().isoformat(),
                "is_current": False,
                "error": str(e)
            },
            "error_message": error_msg
        }

# Create the FunctionTool
weather_api_tool = FunctionTool(func=get_current_weather) 