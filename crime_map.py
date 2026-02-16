import os
import time
import base64
import pandas as pd
import openpyxl
import folium
from folium.plugins import HeatMap, MarkerCluster, Search
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

#File Selector
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

picker = tk.Tk()
picker.withdraw()

EXCEL_PATH = filedialog.askopenfilename(
    title="Select Crime Excel File",
    filetypes=[("Excel files", "*.xlsx")]
)

if not EXCEL_PATH:
    raise SystemExit("No file selected.")

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
OUTPUT_HTML = os.path.join(DESKTOP, "Utoledo_HeatMap.html")


#Map Settings Generation
DEFAULT_CENTER = (41.6528, -83.5379)
DEFAULT_ZOOM = 14
LOGO_FILE = "UToledo Logo.png"

#Data Cleaning for Column Names
def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("\n", " ")
    )
    return df


# Geocoding and Implementation of Progress Bar
def geocode_addresses(df):

    geolocator = Nominatim(user_agent="utoledo-crime-map")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    df["latitude"] = None
    df["longitude"] = None

    unique_locations = df["location"].dropna().unique()
    total = len(unique_locations)

    #GUI Window
    root = tk.Tk()
    root.title("Geocoding Progress")
    root.geometry("460x140")

    label = tk.Label(root, text="Starting...")
    label.pack(pady=5)

    progress = ttk.Progressbar(root, length=420, maximum=total)
    progress.pack(pady=5)

    eta = tk.Label(root)
    eta.pack()

    root.update()

    lookup = {}
    start = time.time()

    for i, loc_text in enumerate(unique_locations, start=1):

        result = geocode(f"{loc_text}, Toledo, Ohio")

        if result:
            lookup[loc_text] = (result.latitude, result.longitude)

        progress["value"] = i

        elapsed = time.time() - start
        remain = (elapsed / i) * (total - i)

        label.config(text=f"Geocoding {i}/{total}")
        eta.config(text=f"~ {remain:.1f}s remaining")

        root.update()      # prevents freeze
        root.after(1)

    root.destroy()

    df["latitude"] = df["location"].map(lambda x: lookup.get(x, (None, None))[0])
    df["longitude"] = df["location"].map(lambda x: lookup.get(x, (None, None))[1])

    return df


#University Logo
def add_logo(m):

    logo_path = os.path.join(BASE_DIR, LOGO_FILE)

    if not os.path.exists(logo_path):
        return

    with open(logo_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    html = f"""
    <div style="
        position: fixed;
        bottom: 10px;
        left: 10px;
        z-index: 9999;
        opacity: 0.85;">
        <img src="data:image/png;base64,{encoded}" width="150">
    </div>
    """

    m.get_root().html.add_child(folium.Element(html))


#Creation of the Heatmap
def build_map(df):

    m = folium.Map(location=DEFAULT_CENTER, zoom_start=DEFAULT_ZOOM, tiles=None)

    #Redux Tiles for map framework
    folium.TileLayer("OpenStreetMap", name="Street (Detailed)").add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite"
    ).add_to(m)

    #Clean Coords Throughout Campus
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude"])

    print("Rows with coords:", len(df))

    #Heatmap Cluster
    heat_layer = folium.FeatureGroup(name="Heatmap Clusters")

    HeatMap(
        df[["latitude", "longitude"]].values.tolist(),
        radius=14,
        blur=18
    ).add_to(heat_layer)

    heat_layer.add_to(m)

    #Marker Cluster
    cluster = MarkerCluster(name="Number of Offenses in Area")

    for _, row in df.iterrows():

        popup_html = f"""
        <b>Location:</b> {row.get('location','')}<br>
        <b>Report Date:</b> {row.get('report date','')}<br>
        <b>Offense Time:</b> {row.get('offense time','')}<br>
        <b>Disposition:</b> {row.get('disposition','')}
        """

        #Text Bar for the Top Left Corner
        search_text = f"{row.get('location','')} {row.get('disposition','')}"

        folium.Marker(
            [row["latitude"], row["longitude"]],
            popup=popup_html,
            title=search_text
        ).add_to(cluster)

    cluster.add_to(m)

    #Search Bar for Locating Crimes
    Search(
        layer=cluster,
        search_label="title",
        placeholder="Search building or crime...",
        collapsed=False
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    add_logo(m)

    return m


#Main
def main():

    df = pd.read_excel(EXCEL_PATH)
    df = clean_columns(df)

    if "location" not in df.columns:
        messagebox.showerror("Error", "No 'Location' column found.")
        return

    df = geocode_addresses(df)

    m = build_map(df)

    m.save(OUTPUT_HTML)

    messagebox.showinfo("Done", f"Map saved to:\n{OUTPUT_HTML}")


if __name__ == "__main__":
    main()
