# class pydantic to create a location model
from pydantic import BaseModel  

class Location(BaseModel):
    latitude: float
    longitude: float    
    timestamp: str
    location: str
    user: str
    activity: str

    def __init__(self, latitude, longitude, timestamp, location, user, activity):
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
        self.location = location
        self.user = user
        self.activity = activity

    class Config:
        orm_mode = True 
        