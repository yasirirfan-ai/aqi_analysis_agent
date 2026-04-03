"""
Streamlit UI for the AQI Analysis Agent.
Author: Hazbilal3
"""
import streamlit as st
import json
from models import UserInput
from agents import analyze_conditions_logic
from config import (
    FIRECRAWL_API_KEY, 
    OPENAI_API_KEY, 
    APP_TITLE, 
    APP_ICON, 
    setup_logging
)

# Initialize logging
setup_logging()

def initialize_session_state():
    if 'api_keys' not in st.session_state:
        # Load from config/env first, fallback to empty string
        st.session_state.api_keys = {
            'firecrawl': FIRECRAWL_API_KEY,
            'openai': OPENAI_API_KEY
        }

def setup_page():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide"
    )
    
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.info("Get personalized health recommendations based on air quality conditions.")

def render_sidebar():
    """Render sidebar with API configuration"""
    with st.sidebar:
        st.header("🔑 API Configuration")
        
        # Determine if we should mask the input (if loaded from env) or show it
        # Simple logic: If key exists in state and matches env, keep it. 
        # Just use state as the source of truth for the input.
        
        new_firecrawl_key = st.text_input(
            "Firecrawl API Key",
            type="password",
            value=st.session_state.api_keys['firecrawl'],
            help="Enter your Firecrawl API key"
        )
        new_openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.api_keys['openai'],
            help="Enter your OpenAI API key"
        )
        
        if (new_firecrawl_key != st.session_state.api_keys['firecrawl'] or 
            new_openai_key != st.session_state.api_keys['openai']):
            st.session_state.api_keys.update({
                'firecrawl': new_firecrawl_key,
                'openai': new_openai_key
            })
            st.success("✅ API keys updated!")

def render_main_content():
    st.header("📍 Location Details")
    col1, col2 = st.columns(2)
    
    with col1:
        city = st.text_input("City", placeholder="e.g., New York")
        state = st.text_input("State", placeholder="e.g., NY")
        country = st.text_input("Country", value="USA", placeholder="USA")
    
    with col2:
        st.header("👤 Personal Details")
        medical_conditions = st.text_area(
            "Medical Conditions (optional)",
            placeholder="e.g., asthma, allergies"
        )
        planned_activity = st.text_area(
            "Planned Activity",
            placeholder="e.g., morning jog for 2 hours"
        )
    
    return UserInput(
        city=city,
        state=state,
        country=country,
        medical_conditions=medical_conditions,
        planned_activity=planned_activity
    )

def main():
    """Main application entry point"""
    initialize_session_state()
    setup_page()
    render_sidebar()
    user_input = render_main_content()
    
    result = None
    
    if st.button("🔍 Analyze & Get Recommendations"):
        if not all([user_input.city, user_input.planned_activity]):
            st.error("Please fill in all required fields (state and medical conditions are optional)")
        elif not all(st.session_state.api_keys.values()):
            st.error("Please provide both API keys in the sidebar")
        else:
            try:
                with st.spinner("🔄 Analyzing conditions..."):
                    # Call shared logic
                    aqi_data, recommendations, info_msg, error_msg = analyze_conditions_logic(
                        user_input=user_input,
                        firecrawl_key=st.session_state.api_keys['firecrawl'],
                        openai_key=st.session_state.api_keys['openai']
                    )
                    
                    if error_msg:
                        st.error(f"❌ {error_msg}")
                    else:
                        
                        warning_text = """
                        ⚠️ Note: The data shown may not match real-time values on the website. 
                        This could be due to caching or rate limiting.
                        """
                        
                        with st.expander("📦 Raw AQI Data", expanded=True):
                            st.json({
                                "url_accessed": info_msg.replace("Accessing URL: ", ""),
                                "data": aqi_data
                            })
                            st.warning(warning_text)

                        st.success("✅ Analysis completed!")
                        result = recommendations # Store for display below
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    if result:
        st.markdown("### 📦 Recommendations")
        st.markdown(result)
        
        st.download_button(
            "💾 Download Recommendations",
            data=result,
            file_name=f"aqi_recommendations_{user_input.city}_{user_input.state}.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
