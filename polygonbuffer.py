import processing
from qgis.core import QgsProject, QgsVectorLayer

# Get your layer by its exact name
layer = QgsProject.instance().mapLayersByName("inputlayer")[0] #here paste your shapefile name

# Buffer parameters
params = {
    'INPUT': layer,
    'DISTANCE': 1.0,        # Buffer distance (set units same as layer CRS)
    'SEGMENTS': 5,
    'DISSOLVE': False,
    'END_CAP_STYLE': 0,
    'JOIN_STYLE': 0,
    'MITER_LIMIT': 2,
    'OUTPUT': "C:/Quis/buffer_output.shp"
}

# Run buffer
buffer_result = processing.run("native:buffer", params)
print("Buffer saved at:", buffer_result['OUTPUT'])

# Load result into map
buffer_layer = QgsVectorLayer(buffer_result['OUTPUT'], "BufferLayer", "ogr")
QgsProject.instance().addMapLayer(buffer_layer)

