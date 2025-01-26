import streamlit as st

from src.configuration.log_config import configure_logging
from src.frontend.common_ui_elem import display_title, load_and_analyze_data
from src.frontend.ui_messenger import display_chat_interface

logging = configure_logging("streamlit_app")

display_title()

display_chat_interface()
