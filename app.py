# app.py

# pip install streamlit web3 streamlit-js-eval

import os
import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
from config import (
    RPC_URL, CONTRACT_ADDRESS, CONTRACT_ABI,
    APP_NAME, TAGLINE, DESCRIPTION, LOGO_PATH,
    FARMER_STATUS_LABELS, BATCH_STATUS_LABELS
)

# =============================================================================
# INITIALISATION & SETUP
# =============================================================================
# Connect to the Sepolia blockchain using the public RPC node
w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)

# Store the user's connected wallet address in Streamlit's session memory
if "wallet_address" not in st.session_state:
    st.session_state["wallet_address"] = None

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def request_wallet_connection(unique_key):
    """Injects JavaScript to request MetaMask connection and retrieves the wallet address."""
    # Wrapped in an async IIFE to allow 'return' to work correctly in the browser context
    js_code = """
        (async () => {
            if (window.ethereum) {
                try {
                    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
                    return accounts.length > 0 ? accounts[0] : null;
                } catch (err) {
                    console.error(err);
                    return null;
                }
            } else {
                return "NO_METAMASK";
            }
        })()
    """
    # Execute JS in browser and capture the result using a unique key to avoid duplicates
    return streamlit_js_eval(js_expressions=js_code, key=unique_key)
    # Execute JS in browser and capture the result using a unique key to avoid duplicates
    return streamlit_js_eval(js_expressions=js_code, key=unique_key)

def execute_write_transaction(func_call, value_wei=0):
    """Prepares an unsigned transaction in Python and hands it to MetaMask to sign/send."""
    if not st.session_state["wallet_address"]:
        st.error("Please connect your wallet first.")
        return

    try:
        from_address = w3.to_checksum_address(st.session_state["wallet_address"])
        # Build the raw transaction payload
        tx_data = func_call.build_transaction({
            'from': from_address,
            'value': value_wei,
            'gas': 3000000,          # Standard safe gas limit for prototypes
            'nonce': 0               # Metamask overrides this securely on the client side
        })
        
        # Format the transaction for JavaScript injection
        to_address = tx_data['to']
        data_hex = tx_data['data']
        val_hex = hex(value_wei)
        
        # JavaScript block to trigger MetaMask signing window
        js_trigger = f"""
            if (window.ethereum) {{
                window.ethereum.request({{
                    method: 'eth_sendTransaction',
                    params: [{{
                        from: '{from_address}',
                        to: '{to_address}',
                        data: '{data_hex}',
                        value: '{val_hex}'
                    }}]
                }}).then((txHash) => {{
                    alert("Transaction successfully sent! Hash: " + txHash);
                }}).catch((err) => {{
                    alert("Transaction cancelled or failed: " + err.message);
                }});
            }}
        """
        # Execute the JS snippet to pop up MetaMask
        streamlit_js_eval(js_expressions=js_trigger, key=f"tx_{data_hex[-10:]}")
        st.info("Please check your MetaMask wallet to confirm the transaction.")
        
    except Exception as e:
        st.error(f"Failed to prepare transaction: {str(e)}")

def render_header():
    """Renders the top branding header on every page cleanly."""
    try:
        # Check if file exists locally to prevent crashing
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=200)
        else:
            st.title(APP_NAME)
    except Exception:
        # Failsafe fallback if image rendering breaks
        st.title(APP_NAME)
        
    st.caption(f"**{TAGLINE}**")
    st.write(DESCRIPTION)
    st.divider()

# =============================================================================
# UI LAYOUT & NAVIGATION
# =============================================================================
st.set_page_config(page_title=APP_NAME, layout="centered")
render_header()

# Attempt passive wallet fetch using a unique key
wallet_res = request_wallet_connection(unique_key="passive_connect")
if wallet_res == "NO_METAMASK":
    st.sidebar.warning("MetaMask not detected. Please install the MetaMask browser extension.")
elif wallet_res and str(wallet_res).startswith("0x"):
    st.session_state["wallet_address"] = w3.to_checksum_address(wallet_res)

st.sidebar.title("Navigation")

# Direct manual connection button with a unique key
if st.session_state["wallet_address"] is None:
    st.sidebar.subheader("Connection Required")
    if st.sidebar.button("🦊 Connect MetaMask Wallet"):
        # This calls the JavaScript function directly on click with a unique key
        res = request_wallet_connection(unique_key="manual_button_connect")
        if res and len(str(res)) > 20: 
            st.session_state["wallet_address"] = w3.to_checksum_address(res)
            st.rerun()
else:
    st.sidebar.success(f"Connected: {st.session_state['wallet_address'][:6]}...{st.session_state['wallet_address'][-4:]}")

menu_selection = st.sidebar.radio(
    "Go to:",
    ["Overview / Dashboard", "Farmer Portal", "Logistics & Transport", "Administration & Quality"]
)

# Display connected status in sidebar
st.sidebar.divider()
if not st.session_state["wallet_address"]:
    st.sidebar.warning("Wallet not connected.")

# =============================================================================
# PAGE 1: OVERVIEW / DASHBOARD
# =============================================================================
if menu_selection == "Overview / Dashboard":
    st.subheader("System Overview")
    st.write("Current status of the smart contract on the Sepolia testnet.")
    
    col1, col2 = st.columns(2)
    
    with st.spinner("Fetching current balance..."):
        try:
            # Read operations don't cost gas and don't need MetaMask signing
            total_batches = contract.functions.batchCounter().call()
            admin_address = contract.functions.admin().call()
            contract_balance = w3.eth.get_balance(CONTRACT_ADDRESS)
            
            with col1:
                st.metric("Total Batches Tracked", total_batches)
                st.metric("Contract Treasury Balance", f"{w3.from_wei(contract_balance, 'ether')} ETH")
            
            with col2:
                st.info(f"**Network:** Sepolia Testnet")
                st.info(f"**Admin Wallet:**\n{admin_address}")
                st.info(f"**Contract Address:**\n{CONTRACT_ADDRESS}")
                
        except Exception as e:
            st.error(f"Error reading from the blockchain: {str(e)}")
            
    st.divider()
    st.subheader("Track a Specific Batch")
    search_id = st.number_input("Enter Batch Identification Number", min_value=1, step=1)
    if st.button("Lookup Batch Details"):
        with st.spinner("Searching blockchain..."):
            try:
                batch_data = contract.functions.batches(search_id).call()
                # batch_data returns a tuple corresponding to the FeedBatch struct
                if batch_data[0] == 0:
                    st.warning("Batch not found. Ensure the number is correct.")
                else:
                    status_label = BATCH_STATUS_LABELS.get(batch_data[6], "Unknown Status")
                    st.success(f"Batch {search_id} Found!")
                    st.write(f"**Status:** {status_label}")
                    st.write(f"**Crop Type:** {batch_data[3]}")
                    st.write(f"**Weight:** {batch_data[4]} kg")
                    st.write(f"**Farmer Address:** {batch_data[1]}")
                    st.write(f"**Transporter Address:** {batch_data[2]}")
                    st.write(f"**Price Assigned:** {batch_data[5]} Wei")
                    st.write(f"**Weighbridge Ticket:** {batch_data[7] if batch_data[7] else 'Pending'}")
            except Exception as e:
                st.error(f"Could not retrieve batch: {str(e)}")

# =============================================================================
# PAGE 2: FARMER PORTAL
# =============================================================================
elif menu_selection == "Farmer Portal":
    st.subheader("Farmer Actions")
    
    with st.expander("Register as a New Farmer", expanded=True):
        st.write("Apply to join the procurement network.")
        f_name = st.text_input("Full Name or Farm Name")
        f_reg = st.text_input("Region / Location")
        f_size = st.number_input("Farm Size (Hectares)", min_value=1, step=1)
        if st.button("Submit Registration"):
            func = contract.functions.applyAsFarmer(f_name, f_reg, f_size)
            execute_write_transaction(func)

    with st.expander("Create a New Feed Batch"):
        st.write("Register a new harvest for quality testing.")
        crop_type = st.selectbox("Crop Type", ["Maize", "Soy"])
        weight = st.number_input("Total Weight (kg)", min_value=100, step=100)
        certs = st.text_input("Certification Reference (e.g. IPFS link or document ID)")
        if st.button("Register Harvest"):
            func = contract.functions.createBatch(crop_type, weight, certs)
            execute_write_transaction(func)
            
    with st.expander("Acknowledge Purchase Order"):
        st.write("Accept the price offered by the procurement team.")
        po_batch_id = st.number_input("Batch Identification Number", min_value=1, step=1, key="ack_po")
        if st.button("Acknowledge Offer"):
            func = contract.functions.acknowledgePO(po_batch_id)
            execute_write_transaction(func)

# =============================================================================
# PAGE 3: LOGISTICS & TRANSPORT
# =============================================================================
elif menu_selection == "Logistics & Transport":
    st.subheader("Transporter Workflow")
    
    with st.expander("Accept Assigned Transport Job", expanded=True):
        st.write("Confirm you will transport the assigned batch.")
        trans_batch_id = st.number_input("Batch Identification Number", min_value=1, step=1, key="acc_trans")
        if st.button("Accept Job"):
            func = contract.functions.acceptTransportJob(trans_batch_id)
            execute_write_transaction(func)

    with st.expander("Confirm Loading (Weighbridge)"):
        st.write("Upload weighbridge ticket details after loading the truck.")
        load_batch_id = st.number_input("Batch Identification Number", min_value=1, step=1, key="load_batch")
        ticket_ref = st.text_input("Weighbridge Ticket Reference")
        if st.button("Confirm Load"):
            func = contract.functions.loadBatch(load_batch_id, ticket_ref)
            execute_write_transaction(func)

    with st.expander("Update Status to In-Transit"):
        st.write("Mark the truck as actively moving to destination.")
        transit_batch_id = st.number_input("Batch Identification Number", min_value=1, step=1, key="transit_batch")
        if st.button("Depart Facility"):
            func = contract.functions.updateToInTransit(transit_batch_id)
            execute_write_transaction(func)

# =============================================================================
# PAGE 4: ADMINISTRATION & QUALITY
# =============================================================================
elif menu_selection == "Administration & Quality":
    st.subheader("Admin Operations (Astral Foods Only)")
    
    with st.expander("Verify Farmer Application", expanded=True):
        st.write("Approve a farmer to allow them to register harvests.")
        farmer_address = st.text_input("Farmer Wallet Address", help="Must start with 0x")
        if st.button("Verify Farmer"):
            try:
                addr = w3.to_checksum_address(farmer_address)
                func = contract.functions.verifyFarmer(addr)
                execute_write_transaction(func)
            except Exception:
                st.error("Invalid Ethereum Address format.")

    with st.expander("Record Silo Quality Check"):
        st.write("Log laboratory results for incoming harvests.")
        q_batch_id = st.number_input("Batch Identification Number", min_value=1, step=1, key="q_batch")
        afla = st.number_input("Aflatoxin Level (PPB)", min_value=0, step=1, help="Must be 20 or lower to pass")
        moist = st.number_input("Moisture Level (%)", min_value=0, step=1, help="Must be 14 or lower to pass")
        if st.button("Submit Test Results"):
            func = contract.functions.siloQualityCheck(q_batch_id, afla, moist)
            execute_write_transaction(func)

    with st.expander("Issue Purchase Order"):
        st.write("Offer a formal price for passed batches.")
        po_id = st.number_input("Batch Identification Number", min_value=1, step=1, key="issue_po")
        price = st.number_input("Price Offer (in Wei)", min_value=1, step=1000)
        if st.button("Create Purchase Order"):
            func = contract.functions.issuePO(po_id, price)
            execute_write_transaction(func)

    with st.expander("Assign Transporter"):
        st.write("Select a logistics partner for an acknowledged order.")
        assig_batch_id = st.number_input("Batch Identification Number", min_value=1, step=1, key="assig_trans")
        transporter_addr = st.text_input("Transporter Wallet Address", help="Must start with 0x")
        if st.button("Assign Transport"):
            try:
                addr = w3.to_checksum_address(transporter_addr)
                func = contract.functions.assignTransporter(assig_batch_id, addr)
                execute_write_transaction(func)
            except Exception:
                st.error("Invalid Ethereum Address format.")

    with st.expander("Confirm Arrival & Inspection"):
        st.write("Log goods as arrived, and submit final visual inspection results.")
        arr_batch_id = st.number_input("Batch Identification Number", min_value=1, step=1, key="arr_batch")
        
        col_arr, col_insp = st.columns(2)
        with col_arr:
            if st.button("Mark as Arrived"):
                func = contract.functions.confirmArrival(arr_batch_id)
                execute_write_transaction(func)
        with col_insp:
            final_pass = st.selectbox("Final Inspection Passed?", [True, False])
            if st.button("Submit Inspection"):
                func = contract.functions.deliverAndInspect(arr_batch_id, final_pass)
                execute_write_transaction(func)

    with st.expander("Final Acceptance (Trigger Payment)", expanded=True):
        st.warning("This action immediately releases funds from the contract to the farmer.")
        pay_batch_id = st.number_input("Batch Identification Number", min_value=1, step=1, key="pay_batch")
        fund_amount = st.number_input("Optional Funding (Wei)", min_value=0, step=1000, help="Send Wei alongside this transaction if the contract lacks funds.")
        if st.button("Accept Goods & Disburse Funds"):
            func = contract.functions.finalAcceptance(pay_batch_id)
            execute_write_transaction(func, value_wei=fund_amount)
