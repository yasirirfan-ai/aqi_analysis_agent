"""
Utility functions for the AQI Analysis Agent.
Author: Hazbilal3
"""
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def format_aqi_url(country: str, state: str, city: str) -> str:
    """
    Format URL based on location, handling cases with and without state.
    
    Args:
        country: Country name
        state: State name (optional)
        city: City name
        
    Returns:
        Formatted URL string for aqi.in
    """
    country_clean = country.lower().replace(' ', '-')
    city_clean = city.lower().replace(' ', '-')
    
    if not state or state.lower() == 'none' or state.strip() == "":
        return f"https://www.aqi.in/dashboard/{country_clean}/{city_clean}"
    
    state_clean = state.lower().replace(' ', '-')
    return f"https://www.aqi.in/dashboard/{country_clean}/{state_clean}/{city_clean}"
