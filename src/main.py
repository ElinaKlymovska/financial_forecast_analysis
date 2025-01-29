import subprocess


if __name__ == "__main__":
    print("Launching Streamlit...")
    subprocess.run(["python3", "-m", "streamlit", "run", "frontend/streamlit_app.py"])


