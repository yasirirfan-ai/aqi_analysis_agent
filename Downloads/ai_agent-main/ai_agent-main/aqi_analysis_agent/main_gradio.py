"""
Gradio UI for the AQI Analysis Agent.
Author: Hazbilal3
"""
import gradio as gr
import json
from models import UserInput
from agents import analyze_conditions_logic

def gradio_adapter(
    city: str,
    state: str,
    country: str,
    medical_conditions: str,
    planned_activity: str,
    firecrawl_key: str,
    openai_key: str
):
    """Adapter function to bridge Gradio inputs to the shared analysis logic."""
    if not firecrawl_key or not openai_key:
        return {}, "Please provide API keys.", "", "Missing API Keys"

    user_input = UserInput(
        city=city,
        state=state,
        country=country,
        medical_conditions=medical_conditions,
        planned_activity=planned_activity
    )
    
    aqi_data, recommendations, info_msg, error_msg = analyze_conditions_logic(
        user_input, firecrawl_key, openai_key
    )
    
    if error_msg:
        return {}, recommendations, info_msg, f"⚠️ Error: {error_msg}"
        
    # Format AQI data for clearer display in Gradio JSON component
    # We can pass the dict directly
    
    warning_msg = """
    ⚠️ Note: The data shown may not match real-time values on the website. 
    This could be due to cached data or rate limiting.
    """
    
    return aqi_data, recommendations, info_msg, warning_msg

def create_demo() -> gr.Blocks:
    """Create and configure the Gradio interface"""
    with gr.Blocks(title="AQI Analysis Agent") as demo:
        gr.Markdown(
            """
            # 🌍 AQI Analysis Agent
            Get personalized health recommendations based on air quality conditions.
            """
        )
        
        # API Configuration
        with gr.Accordion("API Configuration", open=False):
            firecrawl_key = gr.Textbox(
                label="Firecrawl API Key",
                type="password",
                placeholder="Enter your Firecrawl API key"
            )
            openai_key = gr.Textbox(
                label="OpenAI API Key",
                type="password",
                placeholder="Enter your OpenAI API key"
            )
        
        # Location Details
        with gr.Row():
            with gr.Column():
                city = gr.Textbox(label="City", placeholder="e.g., Mumbai")
                state = gr.Textbox(
                    label="State",
                    placeholder="Leave blank for Union Territories or US cities",
                    value=""
                )
                country = gr.Textbox(label="Country", value="India")
        
        # Personal Details
        with gr.Row():
            with gr.Column():
                medical_conditions = gr.Textbox(
                    label="Medical Conditions (optional)",
                    placeholder="e.g., asthma, allergies",
                    lines=2
                )
                planned_activity = gr.Textbox(
                    label="Planned Activity",
                    placeholder="e.g., morning jog for 2 hours",
                    lines=2
                )
        
        # Status Messages
        info_box = gr.Textbox(label="ℹ️ Status", interactive=False)
        warning_box = gr.Textbox(label="⚠️ Warning", interactive=False)
        
        # Output Areas
        aqi_data_json = gr.JSON(label="📊 Current Air Quality Data")
        recommendations = gr.Markdown(label="🏥 Health Recommendations")
        
        # Analyze Button
        analyze_btn = gr.Button("🔍 Analyze & Get Recommendations", variant="primary")
        analyze_btn.click(
            fn=gradio_adapter,
            inputs=[
                city,
                state,
                country,
                medical_conditions,
                planned_activity,
                firecrawl_key,
                openai_key
            ],
            outputs=[aqi_data_json, recommendations, info_box, warning_box]
        )
        
        # Examples
        gr.Examples(
            examples=[
                ["Mumbai", "Maharashtra", "India", "asthma", "morning walk for 30 minutes"],
                ["Delhi", "", "India", "", "outdoor yoga session"],
                ["New York", "", "United States", "allergies", "afternoon run"],
                ["Kakinada", "Andhra Pradesh", "India", "none", "Tennis for 2 hours"]
            ],
            inputs=[city, state, country, medical_conditions, planned_activity]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_demo()
    demo.launch(share=True)
