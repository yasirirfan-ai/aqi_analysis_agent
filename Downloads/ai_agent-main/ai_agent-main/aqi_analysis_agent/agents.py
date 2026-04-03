"""
Core agent logic for AQI Analysis and Health Recommendations.
Author: Hazbilal3
"""
import logging
import json
from typing import Dict, Tuple, Any

from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.models.openai import OpenAIChat
from firecrawl import FirecrawlApp

from models import AQIResponse, ExtractSchema, UserInput
from utils import format_aqi_url

# Initialize logging
logger = logging.getLogger(__name__)


class AQIAnalyzer:
    """
    Agent responsible for fetching and analyzing Air Quality Index (AQI) data.
    Uses Firecrawl to scrape real-time data from aqi.in.
    """
    
    def __init__(self, firecrawl_key: str) -> None:
        self.firecrawl = FirecrawlApp(api_key=firecrawl_key)
    
    def fetch_aqi_data(self, city: str, state: str, country: str) -> Tuple[Dict[str, float], str]:
        """
        Fetch AQI data using Firecrawl.
        
        Returns:
            Tuple containing:
            - Dict of AQI data key-values
            - Info message about the URL accessed
        """
        try:
            url = format_aqi_url(country, state, city)
            info_msg = f"Accessing URL: {url}"
            logger.info(info_msg)
            
            response = self.firecrawl.extract(
                urls=[f"{url}/*"],
                params={
                    'prompt': 'Extract the current real-time AQI, temperature, humidity, wind speed, PM2.5, PM10, and CO levels from the page. Also extract the timestamp of the data.',
                    'schema': ExtractSchema.model_json_schema()
                }
            )
            
            aqi_response = AQIResponse(**response)
            if not aqi_response.success:
                logger.error(f"Firecrawl extraction failed: {aqi_response.status}")
                raise ValueError(f"Failed to fetch AQI data: {aqi_response.status}")
            
            return aqi_response.data, info_msg
            
        except Exception as e:
            logger.error(f"Error fetching AQI data: {e}")
            # Return zeroed data and raise/return error details handled by caller
            # We return empty zeros to allow safe failures in some UI contexts, 
            # but ideally we propagate the exception info.
            # Here we follow the original pattern but with logging.
            return {
                'aqi': 0,
                'temperature': 0,
                'humidity': 0,
                'wind_speed': 0,
                'pm25': 0,
                'pm10': 0,
                'co': 0
            }, str(e)

class HealthRecommendationAgent:
    """
    Agent responsible for generating personalized health advice based on AQI data.
    Uses OpenAI's GPT-4o model via Agno.
    """
    
    def __init__(self, openai_key: str) -> None:
        self.agent = Agent(
            model=OpenAIChat(
                id="gpt-4o",
                name="Health Recommendation Agent",
                api_key=openai_key
            )
        )
    
    def get_recommendations(
        self,
        aqi_data: Dict[str, float],
        user_input: UserInput
    ) -> str:
        prompt = self._create_prompt(aqi_data, user_input)
        try:
            response: RunOutput = self.agent.run(prompt)
            return response.content
        except Exception as e:
            logger.error(f"Health agent failed: {e}")
            return f"Failed to generate health recommendations: {str(e)}"
    
    def _create_prompt(self, aqi_data: Dict[str, float], user_input: UserInput) -> str:
        return f"""
        Based on the following air quality conditions in {user_input.city}, {user_input.state}, {user_input.country}:
        - Overall AQI: {aqi_data['aqi']}
        - PM2.5 Level: {aqi_data['pm25']} µg/m³
        - PM10 Level: {aqi_data['pm10']} µg/m³
        - CO Level: {aqi_data['co']} ppb
        
        Weather conditions:
        - Temperature: {aqi_data['temperature']}°C
        - Humidity: {aqi_data['humidity']}%
        - Wind Speed: {aqi_data['wind_speed']} km/h
        
        User's Context:
        - Medical Conditions: {user_input.medical_conditions or 'None'}
        - Planned Activity: {user_input.planned_activity}
        **Comprehensive Health Recommendations:**
        1. **Impact of Current Air Quality on Health:**
        2. **Necessary Safety Precautions for Planned Activity:**
        3. **Advisability of Planned Activity:**
        4. **Best Time to Conduct the Activity:**
        """

def analyze_conditions_logic(
    user_input: UserInput,
    firecrawl_key: str,
    openai_key: str
) -> Tuple[Dict[str, Any], str, str, str]:
    """
    Orchestrator function to analyze AQI and get recommendations.
    
    Returns:
        Tuple containing:
        - formatted dictionary of AQI Display Data (or raw data)
        - Recommendation text
        - Info message (URL)
        - Warning/Error message (if any)
    """
    # Initialize analyzers
    aqi_analyzer = AQIAnalyzer(firecrawl_key=firecrawl_key)
    health_agent = HealthRecommendationAgent(openai_key=openai_key)
    
    # Get AQI data
    aqi_data, info_msg_or_error = aqi_analyzer.fetch_aqi_data(
        city=user_input.city,
        state=user_input.state,
        country=user_input.country
    )
    
    # Check if fetch failed (simple check if 'aqi' is 0 or if info_msg looks like error)
    # The current fetch_aqi_data returns (data, info_msg) on success OR (zeros, error_msg) on fail.
    # We can detect failure if info_msg starts with "Error" (from the exception block above, wait, I returned str(e) as second arg)
    
    if "Error" in info_msg_or_error or aqi_data['aqi'] == 0:
         return {}, "", "", f"Failed to fetch data: {info_msg_or_error}"

    # Get recommendations
    recommendations = health_agent.get_recommendations(aqi_data, user_input)
    
    return aqi_data, recommendations, info_msg_or_error, ""
