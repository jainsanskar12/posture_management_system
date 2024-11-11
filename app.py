import streamlit as st
import pandas as pd
import numpy as np

# Placeholder data for demonstration (replace with actual data as needed)
sensor_data = {
    "Time": pd.date_range(start="2024-11-01", periods=10, freq="D"),
    "Flex Sensor 1": np.random.randint(100, 300, size=10),
    "Flex Sensor 2": np.random.randint(50, 250, size=10),
    "MPU 1 - X": np.random.randint(150, 350, size=10),
    "MPU 1 - Y": np.random.randint(150, 350, size=10),
    "MPU 1 - Z": np.random.randint(150, 350, size=10),
    "MPU 2 - X": np.random.randint(50, 150, size=10),
    "MPU 2 - Y": np.random.randint(50, 150, size=10),
    "MPU 2 - Z": np.random.randint(50, 150, size=10),
    "Accelerometer - X": np.random.randint(100, 200, size=10),
    "Accelerometer - Y": np.random.randint(100, 200, size=10),
    "Accelerometer - Z": np.random.randint(100, 200, size=10),
}

df = pd.DataFrame(sensor_data)

# Page 1 - Posture Management System
st.title("Posture Management System")
st.subheader("Enter Sensor Ranges")

# Define and store the ranges for each sensor
sensors = ["Flex Sensor 1", "Flex Sensor 2"]
for sensor in sensors:
    st.write(f"### {sensor} Range Settings")
    col1, col2 = st.columns(2)
    with col1:
        min_value = st.number_input(f"Minimum Value for {sensor}", min_value=0, max_value=1024, value=0, key=f"{sensor}_min")
    with col2:
        max_value = st.number_input(f"Maximum Value for {sensor}", min_value=0, max_value=1024, value=256, key=f"{sensor}_max")

# For MPU 1, MPU 2, and Accelerometer, with six input boxes each
advanced_sensors = ["MPU 1", "MPU 2", "Accelerometer"]
parameters = ["X", "Y", "Z"]

for sensor in advanced_sensors:
    st.write(f"### {sensor} Range Settings")
    for param in parameters:
        col1, col2 = st.columns(2)
        with col1:
            min_value = st.number_input(f"Minimum Value for {sensor} - {param}", min_value=0, max_value=1024, value=0, key=f"{sensor}_{param}_min")
        with col2:
            max_value = st.number_input(f"Maximum Value for {sensor} - {param}", min_value=0, max_value=1024, value=256, key=f"{sensor}_{param}_max")

# Displaying a table of sensor readings (for demonstration)
st.write("## Live Sensor Readings (Simulated)")
st.dataframe(df)

# Page 2 - User Dashboard
if st.button("View User Dashboard"):
    st.subheader("User Dashboard")
    st.write("### Activity Overview")
    
    # Count occurrences where values exceeded the specified range
    activity_data = {}
    for sensor in advanced_sensors:
        for param in parameters:
            column_name = f"{sensor} - {param}"
            min_range = st.session_state.get(f"{sensor}_{param}_min", 0)
            max_range = st.session_state.get(f"{sensor}_{param}_max", 256)
            out_of_range_count = ((df[column_name] < min_range) | (df[column_name] > max_range)).sum()
            activity_data[column_name] = out_of_range_count

    # Display summary in a table format
    st.write("#### Out-of-Range Activity Summary")
    user_df = pd.DataFrame(activity_data.items(), columns=["Sensor Parameter", "Times Out of Range"])
    st.dataframe(user_df)


# Page 3 - Doctor's Dashboard
if st.button("View Doctor's Dashboard"):
    st.subheader("Doctor's Dashboard")
    st.write("### Detailed Analysis and Suggestions")

    # Simplified trend line for Flex Sensors only (to reduce complexity)
    st.write("#### Simplified Trend for Flex Sensors")
    st.line_chart(df[["Time", "Flex Sensor 1", "Flex Sensor 2"]].set_index("Time"))

    # Out-of-Range Summary for Doctor
    st.write("#### Out-of-Range Summary for Each Parameter")
    doctor_summary = {}
    for sensor in advanced_sensors:
        for param in parameters:
            column_name = f"{sensor} - {param}"
            min_range, max_range = st.session_state.get(f"{sensor}{param}_min", 0), st.session_state.get(f"{sensor}{param}_max", 256)
            out_of_range = ((df[column_name] < min_range) | (df[column_name] > max_range)).sum()
            doctor_summary[column_name] = out_of_range

    # Display summary as a dataframe
    st.write("Out-of-Range Summary")
    summary_df = pd.DataFrame(doctor_summary.items(), columns=["Sensor Parameter", "Times Out of Range"])
    st.dataframe(summary_df)

    # Suggestion box for the doctor to give recommendations to the user
    doctor_suggestion = st.text_area("Doctor's Suggestion for Patient", "Provide recommendations based on the analysis.")
    
    # Button to send suggestion to the user
    if st.button("Send Suggestion to User"):
        st.success("Suggestion has been sent to the user.")
        # This would typically involve a state update or database save to actually make it persist.
