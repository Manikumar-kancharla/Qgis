from qgis.core import QgsProject, QgsVectorFileWriter

# --- CONFIGURATION ---
# Layer name in QGIS
input_layer_name = "ne_10m_admin_0_countries"

# List of countries to remove
countries_to_remove = ["Argentina"]  # Add more names if needed: ["Argentina", "Brazil"]

# Output path
output_path = r"C:\countries\countries_without_selected.shp"

# --- LOAD LAYER ---
layers = QgsProject.instance().mapLayersByName(input_layer_name)
if not layers:
    raise Exception(f"Layer '{input_layer_name}' not found!")
input_layer = layers[0]

# --- COLLECT GEOMETRIES TO ERASE ---
erase_geoms = []
for f in input_layer.getFeatures():
    if f["NAME"] in countries_to_remove:
        erase_geoms.append(f.geometry())

if not erase_geoms:
    print("No matching countries found to remove.")
else:
    # Merge all erase geometries into one
    merged_geom = erase_geoms[0]
    for geom in erase_geoms[1:]:
        merged_geom = merged_geom.combine(geom)

    # --- CREATE OUTPUT SHAPEFILE ---
    fields = input_layer.fields()
    writer = QgsVectorFileWriter(output_path, "UTF-8", fields, input_layer.wkbType(), input_layer.crs(), "ESRI Shapefile")

    # --- ERASE COUNTRIES ---
    for f in input_layer.getFeatures():
        geom = f.geometry()
        if f["NAME"] not in countries_to_remove:
            f.setGeometry(geom.difference(merged_geom))
            writer.addFeature(f)

    del writer
    print(f"Erase complete! Output saved at: {output_path}")
