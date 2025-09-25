import processing

# Input parameters
world_layer_path = r"C:/countries/ne_10m_admin_0_countries.shp"
output_path = r"D:/GIS_output/argentina_clipped3.shp"
country_name = "Argentina"

# Load world map
world_layer = QgsVectorLayer(world_layer_path, "WorldMap", "ogr")
if not world_layer.isValid():
    raise Exception("Failed to load world map")

# Remove old file if exists
import os
for ext in ['.shp', '.shx', '.dbf', '.prj']:
    f = output_path.replace('.shp', ext)
    if os.path.exists(f):
        os.remove(f)

# Run Extract by Attribute (select by NAME = country_name)
params = {
    'INPUT': world_layer,
    'FIELD': 'NAME',
    'OPERATOR': 0,  # "="
    'VALUE': country_name,
    'OUTPUT': output_path
}

result = processing.run("native:extractbyattribute", params)

# Load the result
clipped_layer = QgsVectorLayer(result['OUTPUT'], f"{country_name}_Clipped", "ogr")
QgsProject.instance().addMapLayer(clipped_layer)

# Apply symbology
symbol = clipped_layer.renderer().symbol()
symbol.setColor(QColor("yellow"))
symbol.symbolLayer(0).setStrokeColor(QColor("black"))
clipped_layer.triggerRepaint()

print(f"{country_name} clipped successfully at {output_path}")
