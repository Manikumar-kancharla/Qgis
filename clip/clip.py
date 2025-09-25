from qgis.core import QgsVectorLayer, QgsProject
from qgis.PyQt.QtGui import QColor
import processing

# -----------------------------
# 1️⃣ Paths
# -----------------------------
world_layer_path = r"C:/countries/ne_10m_admin_0_countries.shp"  # world map
china_layer_path = r"C:/countries/china.gpkg"                    # your China polygon
output_path = r"C:/countries/china_clipped.shp"                  # clipped output

# -----------------------------
# 2️⃣ Load Layers
# -----------------------------
world_layer = QgsVectorLayer(world_layer_path, "WorldMap", "ogr")
china_layer = QgsVectorLayer(china_layer_path, "China", "ogr")

if not world_layer.isValid():
    print("World layer failed to load!")
if not china_layer.isValid():
    print("China layer failed to load!")

# Add layers to canvas
QgsProject.instance().addMapLayer(world_layer)
QgsProject.instance().addMapLayer(china_layer)
print("Layers loaded successfully.")

# -----------------------------
# 3️⃣ Fix Geometries
# -----------------------------
fixed_china_path = r"C:/countries/china_fixed.gpkg"
fixed_china = processing.run(
    "qgis:fixgeometries",
    {'INPUT': china_layer, 'OUTPUT': fixed_china_path}
)['OUTPUT']
fixed_china_layer = QgsVectorLayer(fixed_china, "China_Fixed", "ogr")
QgsProject.instance().addMapLayer(fixed_china_layer)
print("China geometries fixed.")

fixed_world_path = r"C:/countries/world_fixed.shp"
fixed_world = processing.run(
    "qgis:fixgeometries",
    {'INPUT': world_layer, 'OUTPUT': fixed_world_path}
)['OUTPUT']
fixed_world_layer = QgsVectorLayer(fixed_world, "World_Fixed", "ogr")
QgsProject.instance().addMapLayer(fixed_world_layer)
print("World geometries fixed.")

# -----------------------------
# 4️⃣ Clip World with China
# -----------------------------
processing.run(
    "qgis:clip",
    {
        'INPUT': fixed_world_layer,
        'OVERLAY': fixed_china_layer,
        'OUTPUT': output_path
    }
)

clipped_layer = QgsVectorLayer(output_path, "China_Clipped", "ogr")
QgsProject.instance().addMapLayer(clipped_layer)
print("Clip completed. Output saved at:", output_path)

# -----------------------------
# 5️⃣ Apply Symbology (Yellow Fill, Black Border)
# -----------------------------
symbol = clipped_layer.renderer().symbol()
symbol.setColor(QColor("yellow"))                 # fill color
symbol.symbolLayer(0).setStrokeColor(QColor("black"))  # border color
clipped_layer.triggerRepaint()
print("Symbology applied to clipped layer.")
