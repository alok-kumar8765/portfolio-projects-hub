import time
import streamlit as st
import folium
from streamlit_folium import st_folium
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

# --- OSMNX CONFIGURATION (Fixes 502 Overpass Server Capacity Errors) ---
ox.settings.overpass_endpoint = "https://overpass.kumi.systems/api/interpreter"
ox.settings.timeout = 60

# Page Configuration
st.set_page_config(
    page_title="Urban Accessibility Analyzer",
    page_icon="🗺️",
    layout="wide"
)

# App Header
st.title("🏙️ Urban Accessibility & '15-Minute City' Analyzer")
st.markdown(
    "Evaluate local neighborhood walkability by querying OpenStreetMap data, "
    "generating spatial walking buffers, and analyzing nearby infrastructure."
)

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Configuration Panel")

# Location Input
place_name = st.sidebar.text_input(
    "Target Location (City/Neighborhood)", 
    value="Prenzlauer Berg, Berlin, Germany"
)

# Amenity Category
amenity_type = st.sidebar.selectbox(
    "Select Amenity to Analyze",
    options=["cafe", "hospital", "pharmacy", "school", "park", "supermarket"],
    index=0
)

# Walking Radius (meters)
walk_radius = st.sidebar.slider(
    "Walking Radius (meters)",
    min_value=200,
    max_value=1500,
    step=100,
    value=800,
    help="800 meters roughly corresponds to a 10-minute walk."
)

# --- DATA PROCESSING PIPELINE WITH RETRY LOGIC ---
@st.cache_data(show_spinner=True)
def fetch_spatial_data(place, amenity, radius, max_retries=3):
    """Fetches center point and amenities using OSMnx with built-in retry backoff."""
    for attempt in range(max_retries):
        try:
            # 1. Directly geocode place name to latitude and longitude (fixes centroid warning)
            center_lat, center_lon = ox.geocode(place)
            
            # 2. Create a Shapely buffer representing the walking zone
            # Project to local UTM for accurate metric buffering, then back to WGS84 (lat/lon)
            point_gdf = gpd.GeoDataFrame(geometry=[Point(center_lon, center_lat)], crs="EPSG:4326")
            point_proj = point_gdf.to_crs(point_gdf.estimate_utm_crs())
            buffer_proj = point_proj.buffer(radius)
            buffer_wgs84 = buffer_proj.to_crs("EPSG:4326").iloc[0]
            
            # 3. Query OpenStreetMap for amenities within the bounding area
            tags = {"amenity": [amenity]}
            amenities_gdf = ox.features_from_polygon(buffer_wgs84, tags)
            
            # Clean up amenities GeoDataFrame (ensure point representation)
            if not amenities_gdf.empty:
                # Convert polygons/multipolygons to centroids for clean mapping
                amenities_gdf['geometry'] = amenities_gdf.geometry.centroid
                # Filter columns of interest
                cols = [c for c in ['name', 'amenity', 'geometry'] if c in amenities_gdf.columns]
                amenities_gdf = amenities_gdf[cols].dropna(subset=['geometry'])
            
            return center_lat, center_lon, buffer_wgs84, amenities_gdf
            
        except Exception as e:
            # Exponential backoff: wait 2s, 4s, 8s before retrying
            wait_time = 2 ** (attempt + 1)
            if attempt < max_retries - 1:
                time.sleep(wait_time)
            else:
                st.error(f"Overpass API Server busy or query failed. Error details: {e}")
                return None, None, None, None

# Run pipeline
lat, lon, zone_buffer, amenities = fetch_spatial_data(place_name, amenity_type, walk_radius)

if lat and lon:
    # --- METRICS DISPLAY ---
    col1, col2, col3 = st.columns(3)
    amenity_count = len(amenities) if amenities is not None and not amenities.empty else 0
    
    col1.metric("Target Location", place_name.split(",")[0])
    col2.metric("Walking Radius", f"{walk_radius} meters")
    col3.metric(f"Found {amenity_type.capitalize()}s", amenity_count)
    
    # --- FOLIUM MAP GENERATION ---
    m = folium.Map(location=[lat, lon], zoom_start=15, tiles="cartodbpositron")
    
    # Add Center Marker
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>Analysis Center</b><br>{place_name}",
        icon=folium.Icon(color="red", icon="home", prefix="fa")
    ).add_to(m)
    
    # Add Walk Radius Polygon (Shapely boundary mapped via Folium GeoJson)
    folium.GeoJson(
        zone_buffer,
        style_function=lambda x: {
            'fillColor': '#3186cc',
            'color': '#2b5c8f',
            'weight': 2,
            'fillOpacity': 0.15
        },
        tooltip=f"{walk_radius}m Walkability Buffer"
    ).add_to(m)
    
    # Add Amenity Markers
    if amenities is not None and not amenities.empty:
        for idx, row in amenities.iterrows():
            name = row.get('name', 'Unnamed')
            if pd.isna(name):
                name = f"Unnamed {amenity_type.capitalize()}"
                
            folium.CircleMarker(
                location=[row.geometry.y, row.geometry.x],
                radius=6,
                popup=f"<b>{name}</b><br>Type: {amenity_type}",
                color="#2ecc71",
                fill=True,
                fill_color="#2ecc71",
                fill_opacity=0.8
            ).add_to(m)

    # Render Map in Streamlit
    st.markdown("### 🗺️ Interactive Spatial Visualization")
    st_folium(m, width=1100, height=550)
    
    # --- DATA TABLE VIEW ---
    if amenities is not None and not amenities.empty:
        with st.expander("📋 View Raw Amenity Data"):
            st.dataframe(amenities.drop(columns='geometry', errors='ignore'))
else:
    st.warning("Please enter a valid location to initialize the map.")