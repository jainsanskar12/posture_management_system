import streamlit as st
import datetime

# Initialize session state for activity logging
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = {
        sensor: {"exceed_count": 0, "last_exceed_time": None, "last_reading": 0}
        for sensor in ["Flex Sensor 1", "Flex Sensor 2", "MPU 1", "MPU 2", "Accelerometer"]
    }

# Function to switch pages
def go_to_page(page_name):
    st.session_state.current_page = page_name

# Set the default page
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Settings"

# Page: Sensor Range Settings and Live Feedback
if st.session_state.current_page == "Settings":
    sensors = ["Flex Sensor 1", "Flex Sensor 2", "MPU 1", "MPU 2", "Accelerometer"]
    sensor_ranges = {}

    # Streamlit Title and Header
    st.title("Posture Management System")
    st.subheader("Sensor Range Settings")

    # Sensor range inputs
    for sensor in sensors:
        st.write(f"### {sensor} Range Settings")
        col1, col2 = st.columns(2)
        with col1:
            min_value = st.number_input(f"Minimum Value for {sensor}", min_value=0, max_value=1024, value=0, key=f"{sensor}_min")
        with col2:
            max_value = st.number_input(f"Maximum Value for {sensor}", min_value=0, max_value=1024, value=256, key=f"{sensor}_max")
        sensor_ranges[sensor] = (min_value, max_value)

    # Simulated live sensor readings
    sensor_readings = {
        "Flex Sensor 1": 150,
        "Flex Sensor 2": 100,
        "MPU 1": 300,
        "MPU 2": 50,
        "Accelerometer": 200
    }

    # Feedback Mechanism
    st.write("## Feedback Mechanism")
    for sensor, (min_val, max_val) in sensor_ranges.items():
        reading = sensor_readings.get(sensor, 0)  # Simulated reading
        if reading < min_val or reading > max_val:
            st.error(f"⚠️ {sensor} reading out of range! Current Value: {reading}")
            # Log exceedance event with timestamp and update last reading
            st.session_state.activity_log[sensor]["exceed_count"] += 1
            st.session_state.activity_log[sensor]["last_exceed_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            st.success(f"✅ {sensor} reading within range. Current Value: {reading}")
        
        # Update the last reading
        st.session_state.activity_log[sensor]["last_reading"] = reading

    # Button to navigate to User page
    if st.button("User"):
        go_to_page("User")

# Page: User Activity Log and Insights
elif st.session_state.current_page == "User":
    st.title("User Activity Log")
    st.subheader("Sensor Exceedance Summary and Insights")

    # Display exceedance counts and additional insights for each sensor
    for sensor, data in st.session_state.activity_log.items():
        st.write(f"### {sensor}")
        st.markdown(f"""
        - **Range Exceeded**: {data['exceed_count']} time(s)
        - **Last Exceedance**: {data['last_exceed_time'] if data['last_exceed_time'] else 'N/A'}
        - **Most Recent Reading**: {data['last_reading']}
        """)

    # Add navigation to return to Settings page
    if st.button("Back to Settings"):
        go_to_page("Settings")

# Optional styling for a better appearance
st.markdown("""
<style>
    .css-18e3th9 {  /* Adjust padding for Streamlit headers */
        padding-top: 0px;
        padding-bottom: 5px;
    }
    .stAlert {       /* Style alerts to be more distinct */
        font-size: 1.1em;
        padding: 10px;
    }
    .stMarkdown h3 { /* Style subheadings for sensors */
        color: #4a90e2;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)
