import os
import math
import time
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog

# This Section Allows Us to Locate A Specific Files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = filedialog.askopenfilename(
    title="Select the Excel file",
    filetypes=[("Excel files", "*.xlsx")]
)
# Get the user's Desktop folder in a cross‑platform way
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")

# Ensure the Desktop path exists
if not os.path.isdir(DESKTOP):
    DESKTOP = os.path.expanduser("~")  # fallback to home directory

OUTPUT_HTML = os.path.join(DESKTOP, "Utoledo_HeatMap.html")
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

    addresses = df[address_col].dropna()
    total = len(addresses)

    # Creating the GUI Window
    root = tk.Tk()
    root.title("Geocoding Progress")

    label = tk.Label(root, text=f"Starting geocoding... (0/{total})")
    label.pack(pady=10)

    progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress.pack(padx=20, pady=10)

    eta_label = tk.Label(root, text="Estimated time remaining: calculating...")
    eta_label.pack(pady=5)

    progress["maximum"] = total
    root.update()

    start_time = time.time()

    for idx, (i, addr) in enumerate(addresses.items(), start=1):
        if pd.notna(df.at[i, "latitude"]) and pd.notna(df.at[i, "longitude"]):
            continue

        loc = geocode(f"{addr}, Toledo, OH")
        if loc:
            df.at[i, "latitude"] = loc.latitude
            df.at[i, "longitude"] = loc.longitude

        # Update progress Bar So User Can See How Long It Will Take
        progress["value"] = idx
        elapsed = time.time() - start_time
        avg_time = elapsed / idx
        remaining = avg_time * (total - idx)

        label.config(text=f"Geocoding {idx}/{total} addresses...")
        eta_label.config(text=f"Elapsed: {elapsed:.1f}s | Remaining: {remaining:.1f}s")

        root.update_idletasks()

    root.destroy()
    return df

def safe_popup_text(val, max_len=160):
    if pd.isna(val):
        return ""
    s = str(val)
    return (s[:max_len] + "…") if len(s) > max_len else s

def build_map(df):
    m = folium.Map(
        location=DEFAULT_CENTER,
        zoom_start=DEFAULT_ZOOM,
        tiles=None,
        max_bounds=True,
        min_zoom=6,
        max_zoom=17
    )

    folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(m)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite"
    ).add_to(m)

    points = df[["latitude", "longitude"]].dropna().values.tolist()
    if points:
        HeatMap(points, radius=12, blur=15, max_zoom=17, name="Heatmap").add_to(m)

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
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=0)
        df.columns = [c.strip().lower() for c in df.columns]

        if "location" not in df.columns:
            raise ValueError("No 'Location' column found. Check header row in Excel.")

        df = geocode_addresses(df, address_col="location")
        df.to_excel(EXCEL_PATH, index=False)

        df = df.dropna(subset=["latitude", "longitude"])
        if df.empty:
            raise ValueError("No valid coordinates after geocoding.")

        map_start = time.time()
        m = build_map(df)
        m.save(OUTPUT_HTML)
        map_elapsed = time.time() - map_start
        print(f"Map built and saved in {map_elapsed:.1f} seconds.")

        messagebox.showinfo("Success", f"✅ Map built successfully!\nSaved to: {OUTPUT_HTML}")

    except Exception as e:
        messagebox.showerror("Error", f"❌ Something went wrong:\n{e}")

if __name__ == "__main__":
    main()
