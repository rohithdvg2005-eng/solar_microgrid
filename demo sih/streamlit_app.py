# This is the main entry point for Streamlit Cloud
# It simply imports and runs the main application

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main Streamlit app
import deploy_streamlit

if __name__ == "__main__":
    deploy_streamlit.main()
