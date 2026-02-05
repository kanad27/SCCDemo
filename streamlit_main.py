import streamlit as st
import hashlib
import time
import datetime
import sys

# Page Config
st.set_page_config(page_title="Mining Log Demo", page_icon="⚙️")

st.title("⚙️ Visible Mining Simulator")
st.write("This version forces logs to flush immediately and updates the UI in real-time.")

# --- SIDEBAR ---
st.sidebar.header("Controls")
difficulty = st.sidebar.slider("Difficulty", 1, 5, 2)
# We use a session state variable to control the loop
if "mining" not in st.session_state:
    st.session_state.mining = False
if "logs" not in st.session_state:
    st.session_state.logs = []

def start_mining():
    st.session_state.mining = True

def stop_mining():
    st.session_state.mining = False

col1, col2 = st.sidebar.columns(2)
col1.button("🟢 Start", on_click=start_mining)
col2.button("🔴 Stop", on_click=stop_mining)

# --- MAIN UI LAYOUT ---
# We create empty placeholders that we can update dynamically from the loop
metrics_container = st.container()
with metrics_container:
    m1, m2, m3 = st.columns(3)
    metric_hash_count = m1.empty()
    metric_speed = m2.empty()
    metric_time = m3.empty()

st.divider()
st.subheader("Terminal Output Mirror")
# A placeholder for the on-screen log window
log_terminal = st.empty()


# --- MINING LOGIC ---
if st.session_state.mining:
    
    # Initialize variables
    nonce = 0
    start_time = time.time()
    last_update_time = start_time
    
    # Initial Log
    start_msg = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Process Started..."
    print(start_msg, flush=True) # flush=True forces the log to appear instantly
    st.session_state.logs.append(start_msg)
    
    # ---------------------------------------------------------
    # THE LOOP
    # ---------------------------------------------------------
    while st.session_state.mining:
        
        # 1. THE HEAVY LIFTING (CPU Stress)
        # We do a batch of hashes at once to maximize CPU usage
        # instead of updating UI every single hash (which is slow)
        batch_size = 5000 
        for _ in range(batch_size):
            input_data = f"block_{nonce}".encode()
            hashlib.sha256(input_data).hexdigest()
            nonce += 1
        
        # 2. CALCULATE STATS
        current_time = time.time()
        elapsed_total = current_time - start_time
        time_since_last_update = current_time - last_update_time
        
        # 3. UPDATE SCREEN & LOGS (Only every 0.5 seconds to prevent UI freeze)
        if time_since_last_update > 0.5:
            
            # A. Calculate Hashrate
            hashes_per_second = nonce / elapsed_total if elapsed_total > 0 else 0
            
            # B. Update UI Metrics
            metric_hash_count.metric("Total Hashes", f"{nonce:,}")
            metric_speed.metric("Hash Rate", f"{hashes_per_second:.0f} H/s")
            metric_time.metric("Alive Time", f"{elapsed_total:.1f}s")
            
            # C. Create a Log Message
            log_msg = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ALIVE | Time: {elapsed_total:.1f}s | Hashes: {nonce}"
            
            # D. Print to Real Terminal (Force Flush)
            print(log_msg, flush=True)
            
            # E. Update On-Screen Terminal (Keep last 10 lines only)
            st.session_state.logs.append(log_msg)
            if len(st.session_state.logs) > 10:
                st.session_state.logs.pop(0)
            
            log_terminal.code("\n".join(st.session_state.logs), language="text")
            
            # F. Reset update timer
            last_update_time = current_time
            
            # G. Yield control slightly so the "Stop" button can be registered
            time.sleep(0.01)

else:
    st.info("Mining is currently stopped. Press 'Start' in the sidebar.")
    if st.session_state.logs:
        log_terminal.code("\n".join(st.session_state.logs), language="text")

# if st.user.is_logged_in:
#     user_info = st.user.to_dict()
#     # e.g. from Google:
#     canonical_id = user_info["sub"]      # stable unique user id
#     email = user_info["email"]           # user email if you need it
#     st.write(f"Hello, user {canonical_id}")
# import streamlit as st
# import hashlib
# import time
# import datetime
# import sys

# # Set page configuration
# st.set_page_config(page_title="Mining Detection Demo", page_icon="⏱️")

# st.title("⏱️ Mining Survival Timer")
# st.markdown("""
#     **Experiment:** This app runs a CPU-intensive loop and logs the duration to the console.
    
#     Check the **'Manage App' -> 'Logs'** tab in your Streamlit dashboard to see exactly when the process stops.
# """)

# # Sidebar controls
# difficulty = st.sidebar.slider("Difficulty (Zeros)", 1, 5, 2)
# st.sidebar.warning("This will eventually crash the container.")

# # State management
# if 'mining' not in st.session_state:
#     st.session_state.mining = False
# if 'hashes' not in st.session_state:
#     st.session_state.hashes = 0
# if 'start_time' not in st.session_state:
#     st.session_state.start_time = None

# def mine(difficulty_zeros):
#     prefix_str = '0' * difficulty_zeros
#     nonce = 0
    
#     # Record start time
#     start_time = time.time()
#     st.session_state.start_time = start_time
    
#     print(f"--- STARTING MINING SIMULATION AT {datetime.datetime.now()} ---")
    
#     while st.session_state.mining:
#         # 1. CPU Intensive Work
#         input_data = f"block_{nonce}".encode()
#         hash_result = hashlib.sha256(input_data).hexdigest()
        
#         nonce += 1
#         st.session_state.hashes = nonce
        
#         # 2. Logging & Reporting (Every 5000 iterations to avoid log spamming)
#         if nonce % 50000 == 0:
#             elapsed = time.time() - start_time
#             # This print statement goes to the Streamlit Cloud Logs
#             print(f"ALIVE: {elapsed:.2f}s elapsed | {nonce} hashes calculated")
            
#             # Update UI (Optional: Yielding slightly lets the UI update)
#             time.sleep(0.001) 
            
#             # Simple check to stop the UI from freezing entirely
#             if not st.session_state.mining:
#                 break

#     end_time = time.time()
#     print(f"--- STOPPED USER REQUEST AT {datetime.datetime.now()} ---")
#     print(f"Total Duration: {end_time - start_time:.2f} seconds")

# # UI Controls
# col1, col2 = st.columns(2)

# with col1:
#     if st.button("🔴 Start Stress Test"):
#         st.session_state.mining = True
#         mine(difficulty)

# with col2:
#     if st.button("🛑 Stop"):
#         st.session_state.mining = False
#         st.rerun()

# # Display Live Metrics
# if st.session_state.mining and st.session_state.start_time:
#     current_duration = time.time() - st.session_state.start_time
#     st.metric(label="Survival Time", value=f"{current_duration:.2f} s")
#     st.metric(label="Hashes Computed", value=st.session_state.hashes)
