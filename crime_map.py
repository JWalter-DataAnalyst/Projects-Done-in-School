import os
import math
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
import geopandas as gpd
from shapely.geometry import Point
import fiona

# ========= FILES =========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "Utoledo Call Log.xlsx")
OUTPUT_HTML = os.path.join(BASE_DIR, "crime_map.html")
GDB_PATH = os.path.join(BASE_DIR, "LucasCounty.gdb")   # <-- your geodatabase folder
SHEET_NAME = 0
# =========================

# ========= MAP =========
DEFAULT_CENTER = (41.6528, -83.5379)  # Toledo, OH
DEFAULT_ZOOM = 12
# =======================

def geocode_addresses(df, address_col="location"):
    geolocator = Nominatim(user_agent="crime-map")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, swallow_exceptions=True)

    if "latitude" not in df.columns:
        df["latitude"] = None
    if "longitude" not in df.columns:
        df["longitude"] = None

    for i, addr in tqdm(df[address_col].dropna().items(), desc="Geocoding"):
        if pd.notna(df.at[i, "latitude"]) and pd.notna(df.at[i, "longitude"]):
            continue  # already geocoded
        loc = geocode(f"{addr}, Toledo, OH")
        if loc:
            df.at[i, "latitude"] = loc.latitude
            df.at[i, "longitude"] = loc.longitude

    return df

def filter_to_lucas_county(df, lat_col="latitude", lon_col="longitude"):
    # List layers in the GDB so you can see what's inside
    layers = fiona.listlayers(GDB_PATH)
    print("Available layers in GDB:", layers)

    # Pick the county boundary layer (adjust name if different)
    county = gpd.read_file(GDB_PATH, layer=layers[0])  # try first layer, or replace with correct one
    county = county.to_crs(epsg=4326)

    # Convert df to GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df,
        geometry=[Point(xy) for xy in zip(df[lon_col], df[lat_col])],
        crs="EPSG:4326"
    )

    # Keep only points inside county
    gdf = gdf[gdf.within(county.unary_union)]
    return pd.DataFrame(gdf.drop(columns="geometry"))

def safe_popup_text(val, max_len=160):
    if pd.isna(val):
        return ""
    s = str(val)
    return (s[:max_len] + "…") if len(s) > max_len else s

def build_map(df, county=None):
    if county is not None:
        bounds = county.total_bounds
        m = folium.Map(tiles="CartoDB positron")
        m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    else:
        m = folium.Map(location=DEFAULT_CENTER, zoom_start=DEFAULT_ZOOM, tiles="CartoDB positron")

    # Heatmap
    points = df[["latitude", "longitude"]].dropna().values.tolist()
    if points:
        HeatMap(points, radius=12, blur=15, max_zoom=17).add_to(m)

    # Markers
    cluster = MarkerCluster(name="Incidents").add_to(m)
    for _, row in df.iterrows():
        lat, lon = row["latitude"], row["longitude"]
        if any([pd.isna(lat), pd.isna(lon), not math.isfinite(lat), not math.isfinite(lon)]):
            continue

        popup_html = f"""
        <b>Report Date:</b> {safe_popup_text(row.get("report date"))}<br>
        <b>Offense Date:</b> {safe_popup_text(row.get("offense date"))}<br>
        <b>Offense Time:</b> {safe_popup_text(row.get("offense time"))}<br>
        <b>Location:</b> {safe_popup_text(row.get("location"))}<br>
        <b>Disposition:</b> {safe_popup_text(row.get("disposition"))}
        """
        folium.Marker(
            location=(lat, lon),
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(cluster)

    folium.LayerControl().add_to(m)
    return m

def main():
    # Adjust header row if needed
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=0)
    df.columns = [c.strip().lower() for c in df.columns]

    print("Detected columns:", df.columns.tolist())

    if "location" not in df.columns:
        raise ValueError("No 'Location' column found. Check header row in Excel.")

    # Geocode addresses into lat/lon
    df = geocode_addresses(df, address_col="location")

    # Save back to Excel so we don’t need to geocode again
    df.to_excel(EXCEL_PATH, index=False)
    print(f"Updated Excel with latitude/longitude saved: {EXCEL_PATH}")

    # Drop rows without coordinates
    df = df.dropna(subset=["latitude", "longitude"])
    if df.empty:
        raise ValueError("No valid coordinates after geocoding.")

    # Filter to Lucas County
    df = filter_to_lucas_county(df)

    # Build map
    county = gpd.read_file(GDB_PATH, layer=fiona.listlayers(GDB_PATH)[0]).to_crs(epsg=4326)
    m = build_map(df, county=county)
    m.save(OUTPUT_HTML)
    print(f"Map built: {OUTPUT_HTML}")

if __name__ == "__main__":
    main()
