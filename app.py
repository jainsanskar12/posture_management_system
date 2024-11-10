import streamlit as st

# Sensor names
sensors = ["Flex Sensor 1", "Flex Sensor 2", "MPU 1", "MPU 2", "Accelerometer"]

# Initialize dictionary to hold sensor ranges
sensor_ranges = {}

# Streamlit Title and Header
st.title("Posture Management System")
st.subheader("Enter Sensor Ranges")

# Loop through each sensor to create input fields for min and max values
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

# Optional styling for a better appearance
st.markdown("""
<style>
    .css-18e3th9 {  # Adjust padding for streamlit headers
        padding-top: 0px;
        padding-bottom: 5px;
    }
    .stAlert {       # Style alerts to be more distinct
        font-size: 1.1em;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)
