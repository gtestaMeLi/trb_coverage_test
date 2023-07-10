import geopandas as gpd
from shapely.geometry import  Point
import matplotlib.pyplot as plt


def get_data():
    return gpd.read_file("data/geodata.geojson")


data = get_data()
insidePoint = Point(-58.40622469078019,-34.758074907067915)
coverageRing = gpd.GeoSeries([insidePoint.buffer(0.1)], crs="EPSG:4326")

fig,ax = plt.subplots()
data.plot(ax=ax)
coverageRing.plot(ax=ax,color="red")
f = open('results/coverage.json', 'w')
f.write(data.intersects(coverageRing).to_json())

# print(data.intersects(insidePoint))
# print(data.disjoint(insidePoint))
# print(data.touches(insidePoint))

print("finished")