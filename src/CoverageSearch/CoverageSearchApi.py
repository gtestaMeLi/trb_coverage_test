from flask import jsonify, request, Blueprint
from .CoverageSearchService import searchCoverageByPointAndRadius


main = Blueprint('querysearch_blueprint', __name__)

## Obtiene las direcciones ingresadas como input por el usuario
@main.post("search")
def obtenerDireccionesEnFormaCanonica():
    try:
        bodyRequest = request.get_json()
        lat = bodyRequest['lat']
        lon = bodyRequest['lon']
        radius = bodyRequest['radius']
        result = searchCoverageByPointAndRadius(lat,lon,radius)
        if result == None:
            httpCode = 404
        if len(result) > 0:
            httpCode = 200
        else:
            httpCode = 500
        return jsonify(result),httpCode
    except Exception as ex:
        return jsonify({'mensaje': str(ex)}), 500
