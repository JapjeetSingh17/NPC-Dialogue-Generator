import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(layout="wide", page_title="Gemini RPG")

def get_base64_of_bin_file(bin_file):
    """
    Reads a binary file (like an image) and converts it to a base64 string
    so it can be embedded directly into HTML.
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def main():
    st.title("⚔️ Gemini Speech-to-Speech RPG")

    # 1. Setup Sidebar for API Key
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Enter Google AI Studio API Key", type="password")
    
    if not api_key:
        st.warning("Please enter your API Key in the sidebar to activate the AI.")
        return

    # 2. Load and Process the Image
    # We need to convert img.jpg to a Base64 string so Phaser can load it 
    # without needing a separate web server.
    if os.path.exists("img.jpg"):
        img_base64 = get_base64_of_bin_file("img.jpg")
        # Create the full data URI
        img_src = f"data:image/jpeg;base64,{img_base64}"
    else:
        st.error("img.jpg not found in the same directory!")
        return

    # 3. Load the HTML File
    if os.path.exists("Npc.html"):
        with open("Npc.html", "r", encoding="utf-8") as f:
            html_code = f.read()
            
        # 4. Inject Dynamic Data into the HTML
        # Replace the dummy API key in the JS with the one from Streamlit sidebar
        # Note: The HTML file has 'const apiKey = "AIza...";'
        # We will replace the specific line or variable.
        
        # A safer regex replacement or direct string replace:
        # We replace the variable declaration logic to use our python input
        # We also replace the image path 'img.jpg' with our Base64 data
        
        modified_html = html_code.replace(
            'const apiKey = "AIzaSyBxXQAoImBs-kYcjIcOoXzdeZTIikZquuo";', 
            f'const apiKey = "{api_key}";'
        )
        
        modified_html = modified_html.replace(
            "this.load.image('map', 'img.jpg');", 
            f"this.load.image('map', '{img_src}');"
        )

        # 5. Render the HTML component
        # height=850 accommodates the 600px canvas + UI elements
        components.html(modified_html, height=850, scrolling=False)

    else:
        st.error("Npc.html not found in the same directory!")

if __name__ == "__main__":
    main()