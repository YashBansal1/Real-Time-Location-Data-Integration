from flask_restful import Api
from app.gps import GPSTrackingResource
from app.auth import requires_auth
from app.database import LocationResource, CabLocationsResource

def configure_api(api):
    api.add_resource(GPSTrackingResource, '/gps_tracking')
    api.add_resource(LocationResource, '/locations')
    api.add_resource(CabLocationsResource, '/cab_locations')
