import streamlit as st
import pandas as pd
import numpy as np

# Placeholder data for demonstration (you can replace this with actual data)
sensor_data = {
    "Time": pd.date_range(start="2024-11-01", periods=10, freq="D"),
    "Flex Sensor 1": np.random.randint(100, 300, size=10),
    "Flex Sensor 2": np.random.randint(50, 250, size=10),
    "MPU 1": np.random.randint(150, 350, size=10),
    "MPU 2": np.random.randint(50, 150, size=10),
    "Accelerometer": np.random.randint(100, 200, size=10),
}

df = pd.DataFrame(sensor_data)

# Page 1 - Posture Management System
st.title("Posture Management System")
st.subheader("Enter Sensor Ranges")

# Define and store the ranges for each sensor
sensors = ["Flex Sensor 1", "Flex Sensor 2", "MPU 1", "MPU 2", "Accelerometer"]
sensor_ranges = {}

# Collect range input for each sensor
for sensor in sensors:
    st.write(f"### {sensor} Range Settings")
    col1, col2 = st.columns(2)
    with col1:
        min_value = st.number_input(f"Minimum Value for {sensor}", min_value=0, max_value=1024, value=0, key=f"{sensor}_min")
    with col2:
        max_value = st.number_input(f"Maximum Value for {sensor}", min_value=0, max_value=1024, value=256, key=f"{sensor}_max")
    sensor_ranges[sensor] = (min_value, max_value)

# Placeholder for live sensor readings (for demonstration)
sensor_readings = {
    "Flex Sensor 1": 150,
    "Flex Sensor 2": 100,
    "MPU 1": 300,
    "MPU 2": 50,
    "Accelerometer": 200
}

# Display feedback section
st.write("## Feedback Mechanism")
for sensor, (min_val, max_val) in sensor_ranges.items():
    reading = sensor_readings.get(sensor, 0)  # Simulated reading
    if reading < min_val or reading > max_val:
        st.error(f"⚠️ {sensor} reading out of range! Current Value: {reading}")
    else:
        st.success(f"✅ {sensor} reading within range. Current Value: {reading}")

# Display a simple line chart for sensor data
st.write("## Sensor Data")
st.line_chart(df.set_index('Time'))

# Page 2 - User Activity and Feedback
if st.button("View User Activity Data"):
    st.subheader("User Activity Data")
    # Display a simple table of the sensor readings (or any other data you'd like to show)
    st.dataframe(df)

    # Feedback message
    st.write("### Feedback Summary")
    for sensor, (min_val, max_val) in sensor_ranges.items():
        reading = sensor_readings.get(sensor, 0)
        if reading < min_val or reading > max_val:
            st.error(f"⚠️ {sensor} reading out of range!")
        else:
            st.success(f"✅ {sensor} reading within range.")

# Page 3 - Doctor's Suggestions
if st.button("View Doctor's Dashboard"):
    st.subheader("Doctor's Dashboard")
    st.write("### Recommendations and Analysis")
    
    # Example of a placeholder data visualization for doctor's view
    st.write("#### Sensor Data Overview")
    st.line_chart(df.set_index('Time'))
    
    # Recommendations box
    doctor_suggestion = st.text_area("Doctor's Suggestion for Patient", "Provide detailed suggestion based on the sensor data and activity.")
    st.write(f"Doctor's Suggestion: {doctor_suggestion}")
    
    # Button to send suggestion to the user
    if st.button("Send Suggestion to User"):
        st.success("Suggestion has been sent to the user.")
