import streamlit as st
import pandas as pd
import requests
import numpy as np
from datetime import datetime

# ------------------------ Configuration ------------------------

# Replace with your ESP32's IP address
ESP32_IP = "192.168.201.190"  # e.g., "192.168.1.100"
ESP32_PORT = 80
ESP32_BASE_URL = f"http://{ESP32_IP}"

# Endpoint paths
GET_ENDPOINT = "/api/data"
POST_ENDPOINT = "/api/data"

# ------------------------ Helper Functions ------------------------

def get_sensor_data():
    """
    Fetch sensor data from the ESP32 server via GET request.
    Returns:
        dict: Flattened sensor data.
    """
    try:
        response = requests.get(f"{ESP32_BASE_URL}{GET_ENDPOINT}", timeout=2)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        
        # Flatten the nested sensor_data
        flat_data = {}
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        flat_data["Timestamp"] = timestamp
        
        # MPU1
        mpu1_acc = data.get("MPU1", {}).get("accelerometer", [np.nan, np.nan, np.nan])
        mpu1_gyro = data.get("MPU1", {}).get("gyroscope", [np.nan, np.nan, np.nan])
        flat_data["MPU1_Accelerometer_X"] = mpu1_acc[0]
        flat_data["MPU1_Accelerometer_Y"] = mpu1_acc[1]
        flat_data["MPU1_Accelerometer_Z"] = mpu1_acc[2]
        flat_data["MPU1_Gyroscope_X"] = mpu1_gyro[0]
        flat_data["MPU1_Gyroscope_Y"] = mpu1_gyro[1]
        flat_data["MPU1_Gyroscope_Z"] = mpu1_gyro[2]
        
        # MPU2
        mpu2_acc = data.get("MPU2", {}).get("accelerometer", [np.nan, np.nan, np.nan])
        mpu2_gyro = data.get("MPU2", {}).get("gyroscope", [np.nan, np.nan, np.nan])
        flat_data["MPU2_Accelerometer_X"] = mpu2_acc[0]
        flat_data["MPU2_Accelerometer_Y"] = mpu2_acc[1]
        flat_data["MPU2_Accelerometer_Z"] = mpu2_acc[2]
        flat_data["MPU2_Gyroscope_X"] = mpu2_gyro[0]
        flat_data["MPU2_Gyroscope_Y"] = mpu2_gyro[1]
        flat_data["MPU2_Gyroscope_Z"] = mpu2_gyro[2]
        
        # Flex Sensors
        flat_data["Flex_sensor1"] = data.get("Flex_sensor1", np.nan)
        flat_data["Flex_sensor2"] = data.get("Flex_sensor2", np.nan)
        
        # Accelerometer
        accelerometer = data.get("Accelerometer", [np.nan, np.nan, np.nan])
        flat_data["Accelerometer_X"] = accelerometer[0]
        flat_data["Accelerometer_Y"] = accelerometer[1]
        flat_data["Accelerometer_Z"] = accelerometer[2]
        
        return flat_data
    except requests.RequestException as e:
        st.error(f"Error fetching sensor data: {e}")
        return {}

def update_thresholds(new_thresholds):
    """
    Update sensor thresholds on the ESP32 server via POST request.
    Args:
        new_thresholds (dict): Dictionary containing new threshold values.
    Returns:
        bool: True if update was successful, False otherwise.
    """
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{ESP32_BASE_URL}{POST_ENDPOINT}", json=new_thresholds, headers=headers, timeout=2)
        response.raise_for_status()
        res_json = response.json()
        if res_json.get("status") == "Thresholds updated":
            st.success("Thresholds successfully updated on ESP32.")
            return True
        else:
            st.error("Failed to update thresholds on ESP32.")
            return False
    except requests.RequestException as e:
        st.error(f"Error updating thresholds: {e}")
        return False

# ------------------------ Streamlit Application ------------------------

st.set_page_config(page_title="Posture Management System", layout="wide")

st.title("Posture Management System")

# Sidebar for Navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to", ["Home", "User Dashboard", "Doctor's Dashboard"])

# Initialize session state for sensor data history
if 'sensor_history' not in st.session_state:
    st.session_state.sensor_history = pd.DataFrame()

# Home Page
if app_mode == "Home":
    st.header("Live Sensor Data and Threshold Settings")
    
    # Fetch live sensor data
    sensor_data = get_sensor_data()
    
    if sensor_data:
        # Append to sensor_history
        st.session_state.sensor_history = st.session_state.sensor_history.append(sensor_data, ignore_index=True)
        
        # Convert current sensor_data to DataFrame for display
        current_df = pd.DataFrame([sensor_data])
        st.subheader("Live Sensor Readings")
        st.dataframe(current_df.set_index("Timestamp"))
    
    # Threshold Settings Form
    st.subheader("Update Sensor Thresholds")
    with st.form("threshold_form"):
        st.write("### Flex Sensors Thresholds")
        flex1_min = st.number_input("Flex_sensor1 Minimum Value", min_value=0, max_value=4095, value=180, key="Flex_sensor1_min")
        flex1_max = st.number_input("Flex_sensor1 Maximum Value", min_value=0, max_value=4095, value=220, key="Flex_sensor1_max")
        flex2_min = st.number_input("Flex_sensor2 Minimum Value", min_value=0, max_value=4095, value=180, key="Flex_sensor2_min")
        flex2_max = st.number_input("Flex_sensor2 Maximum Value", min_value=0, max_value=4095, value=220, key="Flex_sensor2_max")
        
        st.write("### MPU Thresholds")
        mpu1_min = st.number_input("MPU1 Minimum Value", min_value=0, max_value=4095, value=0, key="MPU1_min")
        mpu1_max = st.number_input("MPU1 Maximum Value", min_value=0, max_value=4095, value=256, key="MPU1_max")
        mpu2_min = st.number_input("MPU2 Minimum Value", min_value=0, max_value=4095, value=0, key="MPU2_min")
        mpu2_max = st.number_input("MPU2 Maximum Value", min_value=0, max_value=4095, value=256, key="MPU2_max")
        
        st.write("### Accelerometer Thresholds")
        accel_min = st.number_input("Accelerometer Minimum Value", min_value=0, max_value=4095, value=1800, key="Accelerometer_min")
        accel_max = st.number_input("Accelerometer Maximum Value", min_value=0, max_value=4095, value=2200, key="Accelerometer_max")
        
        submitted = st.form_submit_button("Update Thresholds")
        
        if submitted:
            # Prepare the payload as per ESP32's expected structure
            payload = {
                "Flex_sensor1": [flex1_min, flex1_max],
                "Flex_sensor2": [flex2_min, flex2_max],
                "MPU1": [mpu1_min, mpu1_max],
                "MPU2": [mpu2_min, mpu2_max],
                "Accelerometer": [accel_min, accel_max],
            }
            update_thresholds(payload)

# User Dashboard
elif app_mode == "User Dashboard":
    st.header("User Dashboard")
    
    if st.session_state.sensor_history.empty:
        st.info("No sensor data available. Please visit the Home page to fetch sensor data.")
    else:
        st.subheader("Activity Overview")
        
        # Retrieve the latest sensor data
        latest_data = st.session_state.sensor_history.iloc[-1]
        
        # Define thresholds based on the latest input or default values
        thresholds = {
            "Flex_sensor1": [st.session_state.get("Flex_sensor1_min", 180), st.session_state.get("Flex_sensor1_max", 220)],
            "Flex_sensor2": [st.session_state.get("Flex_sensor2_min", 180), st.session_state.get("Flex_sensor2_max", 220)],
            "MPU1": [st.session_state.get("MPU1_min", 0), st.session_state.get("MPU1_max", 256)],
            "MPU2": [st.session_state.get("MPU2_min", 0), st.session_state.get("MPU2_max", 256)],
            "Accelerometer": [st.session_state.get("Accelerometer_min", 1800), st.session_state.get("Accelerometer_max", 2200)],
        }
        
        activity_data = {}
        
        # Check Flex Sensors
        activity_data["Flex_sensor1"] = int(latest_data["Flex_sensor1"] > thresholds["Flex_sensor1"][1])
        activity_data["Flex_sensor2"] = int(latest_data["Flex_sensor2"] > thresholds["Flex_sensor2"][1])
        
        # Check MPU1
        mpu1_acc_x = latest_data.get("MPU1_Accelerometer_X", np.nan)
        mpu1_acc_z = latest_data.get("MPU1_Accelerometer_Z", np.nan)
        accel_min, accel_max = thresholds["Accelerometer"]
        activity_data["MPU1_Accelerometer_X"] = int(not (accel_min <= mpu1_acc_x <= accel_max))
        activity_data["MPU1_Accelerometer_Z"] = int(not (accel_min <= mpu1_acc_z <= accel_max))
        
        # Check MPU2
        mpu2_acc_x = latest_data.get("MPU2_Accelerometer_X", np.nan)
        mpu2_acc_z = latest_data.get("MPU2_Accelerometer_Z", np.nan)
        activity_data["MPU2_Accelerometer_X"] = int(not (accel_min <= mpu2_acc_x <= accel_max))
        activity_data["MPU2_Accelerometer_Z"] = int(not (accel_min <= mpu2_acc_z <= accel_max))
        
        # Create DataFrame for display
        activity_df = pd.DataFrame(activity_data.items(), columns=["Sensor Parameter", "Out of Range (1=True, 0=False)"])
        st.dataframe(activity_df)
        
        # Summary
        total_out_of_range = activity_df["Out of Range (1=True, 0=False)"].sum()
        st.write(f"### Total Out-of-Range Instances: {total_out_of_range}")

# Doctor's Dashboard
elif app_mode == "Doctor's Dashboard":
    st.header("Doctor's Dashboard")
    
    if st.session_state.sensor_history.empty:
        st.info("No sensor data available. Please visit the Home page to fetch sensor data.")
    else:
        st.subheader("Detailed Analysis and Suggestions")
        
        # Display trend lines for Flex Sensors
        st.write("### Flex Sensors Trend")
        flex_history = st.session_state.sensor_history[["Timestamp", "Flex_sensor1", "Flex_sensor2"]].set_index("Timestamp")
        st.line_chart(flex_history)
        
        # Out-of-Range Summary for Each Parameter
        st.write("### Out-of-Range Summary for Each Parameter")
        
        # Define thresholds based on the latest input or default values
        thresholds = {
            "Flex_sensor1": [st.session_state.get("Flex_sensor1_min", 180), st.session_state.get("Flex_sensor1_max", 220)],
            "Flex_sensor2": [st.session_state.get("Flex_sensor2_min", 180), st.session_state.get("Flex_sensor2_max", 220)],
            "MPU1": [st.session_state.get("MPU1_min", 0), st.session_state.get("MPU1_max", 256)],
            "MPU2": [st.session_state.get("MPU2_min", 0), st.session_state.get("MPU2_max", 256)],
            "Accelerometer": [st.session_state.get("Accelerometer_min", 1800), st.session_state.get("Accelerometer_max", 2200)],
        }
        
        # Initialize summary dictionary
        doctor_summary = {}
        
        # Iterate over sensor_history to count out-of-range instances
        for index, row in st.session_state.sensor_history.iterrows():
            # Flex_sensor1
            if row["Flex_sensor1"] > thresholds["Flex_sensor1"][1]:
                doctor_summary["Flex_sensor1"] = doctor_summary.get("Flex_sensor1", 0) + 1
            # Flex_sensor2
            if row["Flex_sensor2"] > thresholds["Flex_sensor2"][1]:
                doctor_summary["Flex_sensor2"] = doctor_summary.get("Flex_sensor2", 0) + 1
            # MPU1 Accelerometer X
            if not (thresholds["Accelerometer"][0] <= row["MPU1_Accelerometer_X"] <= thresholds["Accelerometer"][1]):
                doctor_summary["MPU1_Accelerometer_X"] = doctor_summary.get("MPU1_Accelerometer_X", 0) + 1
            # MPU1 Accelerometer Z
            if not (thresholds["Accelerometer"][0] <= row["MPU1_Accelerometer_Z"] <= thresholds["Accelerometer"][1]):
                doctor_summary["MPU1_Accelerometer_Z"] = doctor_summary.get("MPU1_Accelerometer_Z", 0) + 1
            # MPU2 Accelerometer X
            if not (thresholds["Accelerometer"][0] <= row["MPU2_Accelerometer_X"] <= thresholds["Accelerometer"][1]):
                doctor_summary["MPU2_Accelerometer_X"] = doctor_summary.get("MPU2_Accelerometer_X", 0) + 1
            # MPU2 Accelerometer Z
            if not (thresholds["Accelerometer"][0] <= row["MPU2_Accelerometer_Z"] <= thresholds["Accelerometer"][1]):
                doctor_summary["MPU2_Accelerometer_Z"] = doctor_summary.get("MPU2_Accelerometer_Z", 0) + 1
        
        # Convert summary to DataFrame
        summary_df = pd.DataFrame(doctor_summary.items(), columns=["Sensor Parameter", "Times Out of Range"])
        st.dataframe(summary_df)
        
        # Suggestion Box
        st.write("### Doctor's Suggestions")
        doctor_suggestion = st.text_area("Provide recommendations based on the analysis:", "")
        
        if st.button("Send Suggestion to User"):
            if doctor_suggestion.strip() == "":
                st.warning("Please enter a suggestion before sending.")
            else:
                # Here you would typically send the suggestion to the user via an appropriate method
                # For demonstration, we'll just display a success message
                st.success("Suggestion has been sent to the user.")
                # Optionally, you can log the suggestion or store it in a database

# ------------------------ Auto-Refresh Sensor Data ------------------------

# Optional: Add a button to manually refresh sensor data
st.sidebar.markdown("---")
if st.sidebar.button("Refresh Sensor Data"):
    # Fetch and append new sensor data
    new_sensor_data = get_sensor_data()
    if new_sensor_data:
        st.session_state.sensor_history = st.session_state.sensor_history.append(new_sensor_data, ignore_index=True)
        st.success("Sensor data refreshed.")

# Optional: Display sensor history
with st.expander("Show Sensor Data History"):
    if st.session_state.sensor_history.empty:
        st.info("No sensor data available.")
    else:
        st.dataframe(st.session_state.sensor_history)

# ------------------------ End of Application ------------------------
