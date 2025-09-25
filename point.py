from qgis.core import (
    QgsProject,
    QgsFeature,
    QgsGeometry,
    QgsVectorLayer,
    QgsVectorFileWriter
)

# === 1. Get your point layer ===
point_layer = QgsProject.instance().mapLayersByName('point')[0]

# === 2. Create a new memory layer for buffers ===
buffer_layer = QgsVectorLayer('Polygon?crs=EPSG:4326', 'point_buffers', 'memory')
buffer_provider = buffer_layer.dataProvider()

# === 3. Set buffer distance (in CRS units, degrees for EPSG:4326) ===
buffer_distance = 0.01  # adjust as needed

# === 4. Loop through all points and create buffers ===
for feat in point_layer.getFeatures():
    geom = feat.geometry()
    buffer_geom = geom.buffer(buffer_distance, 20)  # 20 segments for smooth circle
    buffer_feat = QgsFeature()
    buffer_feat.setGeometry(buffer_geom)
    buffer_provider.addFeature(buffer_feat)

buffer_layer.updateExtents()
QgsProject.instance().addMapLayer(buffer_layer)

# === 5. Optional: Save buffer layer to disk ===
output_path = r"C:\Quis\point_buffe.shp"
QgsVectorFileWriter.writeAsVectorFormat(buffer_layer, output_path, "UTF-8", buffer_layer.crs(), "ESRI Shapefile")

print("Buffers created for all points successfully!")
