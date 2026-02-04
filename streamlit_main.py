import streamlit as st
import hashlib
import time
import datetime
import sys

# Set page configuration
st.set_page_config(page_title="Mining Detection Demo", page_icon="⏱️")

st.title("⏱️ Mining Survival Timer")
st.markdown("""
    **Experiment:** This app runs a CPU-intensive loop and logs the duration to the console.
    
    Check the **'Manage App' -> 'Logs'** tab in your Streamlit dashboard to see exactly when the process stops.
""")

# Sidebar controls
difficulty = st.sidebar.slider("Difficulty (Zeros)", 1, 5, 2)
st.sidebar.warning("This will eventually crash the container.")

# State management
if 'mining' not in st.session_state:
    st.session_state.mining = False
if 'hashes' not in st.session_state:
    st.session_state.hashes = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

def mine(difficulty_zeros):
    prefix_str = '0' * difficulty_zeros
    nonce = 0
    
    # Record start time
    start_time = time.time()
    st.session_state.start_time = start_time
    
    print(f"--- STARTING MINING SIMULATION AT {datetime.datetime.now()} ---")
    
    while st.session_state.mining:
        # 1. CPU Intensive Work
        input_data = f"block_{nonce}".encode()
        hash_result = hashlib.sha256(input_data).hexdigest()
        
        nonce += 1
        st.session_state.hashes = nonce
        
        # 2. Logging & Reporting (Every 5000 iterations to avoid log spamming)
        if nonce % 50000 == 0:
            elapsed = time.time() - start_time
            # This print statement goes to the Streamlit Cloud Logs
            print(f"ALIVE: {elapsed:.2f}s elapsed | {nonce} hashes calculated")
            
            # Update UI (Optional: Yielding slightly lets the UI update)
            time.sleep(0.001) 
            
            # Simple check to stop the UI from freezing entirely
            if not st.session_state.mining:
                break

    end_time = time.time()
    print(f"--- STOPPED USER REQUEST AT {datetime.datetime.now()} ---")
    print(f"Total Duration: {end_time - start_time:.2f} seconds")

# UI Controls
col1, col2 = st.columns(2)

with col1:
    if st.button("🔴 Start Stress Test"):
        st.session_state.mining = True
        mine(difficulty)

with col2:
    if st.button("🛑 Stop"):
        st.session_state.mining = False
        st.rerun()

# Display Live Metrics
if st.session_state.mining and st.session_state.start_time:
    current_duration = time.time() - st.session_state.start_time
    st.metric(label="Survival Time", value=f"{current_duration:.2f} s")
    st.metric(label="Hashes Computed", value=st.session_state.hashes)
