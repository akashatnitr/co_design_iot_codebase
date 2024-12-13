import streamlit as st
import pandas as pd
import numpy as np
# import pydeck as pdk
import plotly.express as px

data_path = "/content/drive/MyDrive/thesis/data_location_10152022.csv"

st.title("Location data visualization")
st.markdown("This app provides a visualization to the location data collected as part of the thesis work")


@st.cache(persist=True)
def map_charging_type(x):
  charging_type = {"Charging:unplugged": 1, "Charging:battery_plugged_ac": 2, "Charging:battery_plugged_usb": 3}
  return charging_type[x]


@st.cache(persist=True)
def map_bluetooth(x):
  bluetooth = {"UNCATEGORIZED On": 1, "UNCATEGORIZED On: Device Connected": 2, "NONE On": 3, "NONE Off": 4, "AUDIO_VIDEO On: Device Connected": 5}
  return bluetooth[x["bluetooth_device_type"]+" "+x["bluetooth_status"]]


@st.cache(persist=True)
def map_wifi(x):
  wifi = {"Wifi:<unknown ssid>": 0}
  return wifi.get(x, 1)


@st.cache(persist=True)
def load_data():
	data_df = pd.read_csv(data_path)

	# Charging type map
	data_df["charging_type_map"] = data_df["charging_type"].apply(lambda x: map_charging_type(x))

	# Charging status map
	data_df["charging_status_map"] = data_df["charging_status"].apply(lambda x: 1 if x == "Charging" else 0)

	# Bluetooth device type and status map
	data_df["bluetooth_map"] = data_df[["bluetooth_device_type", "bluetooth_status"]].apply(lambda x: map_bluetooth(x), axis=1)

	# Wifi map
	data_df["wifi_map"] = data_df["wifi_status"].apply(lambda x: map_wifi(x))

	# Keep the required columns
	data_df = data_df[["user", "latitude", "longitude", "charging_status_map", "charging_type_map", "bluetooth_map", "wifi_map", "timestamp", "location"]]

	# Group the data by user
	group_sort_data = data_df.groupby("user").apply(pd.DataFrame.sort_values, "timestamp").reset_index(drop=True)

	# Remove user_4 data from the grouped data
	group_sort_data = group_sort_data[group_sort_data["user"]!="user_4"]

	return group_sort_data

loc_df = load_data()

# Plot 1
st.header("Mapping of location data based on filter conditions: user and date")

users_option = st.selectbox(
	"Provide the user", tuple(sorted(loc_df["user"].unique())))

st.map(loc_df.query("user == @usersoption")[["latitude", "longitude"]])