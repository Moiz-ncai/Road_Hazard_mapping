from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from enum import Enum
import sys
import os

# Add parent directory to sys.path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import db

class HazardType(Enum):
    POTHOLE = "pothole"
    CRACK = "crack"
    DEBRIS = "debris"
    CONSTRUCTION = "construction"
    FLOODING = "flooding"

class SeverityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Hazard(db.Model):
    __tablename__ = 'hazards'
    
    id = Column(Integer, primary_key=True)
    latitude = Column(Float(precision=8), nullable=False)
    longitude = Column(Float(precision=8), nullable=False)
    location = Column(Geometry('POINT', srid=4326))
    hazard_type = Column(SQLEnum(HazardType), nullable=False)
    severity_level = Column(SQLEnum(SeverityLevel), nullable=False)
    detection_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    confidence_score = Column(Float, default=0.0)
    image_path = Column(String(255), nullable=True)
    speed_limit = Column(Integer, nullable=False)
    recommended_speed = Column(Integer, nullable=False)
    verified = Column(Boolean, default=False)
    road_name = Column(String(255), nullable=False)
    area = Column(String(255), nullable=False)
    weather_condition = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f'<Hazard {self.id}: {self.hazard_type.value} at ({self.latitude}, {self.longitude})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'hazard_type': self.hazard_type.value,
            'severity_level': self.severity_level.value,
            'detection_timestamp': self.detection_timestamp.isoformat(),
            'confidence_score': self.confidence_score,
            'image_path': self.image_path,
            'speed_limit': self.speed_limit,
            'recommended_speed': self.recommended_speed,
            'verified': self.verified,
            'road_name': self.road_name,
            'area': self.area,
            'weather_condition': self.weather_condition
        }
    
    @staticmethod
    def from_dict(data):
        return Hazard(
            latitude=data['latitude'],
            longitude=data['longitude'],
            hazard_type=HazardType(data['hazard_type']),
            severity_level=SeverityLevel(data['severity_level']),
            detection_timestamp=datetime.fromisoformat(data.get('detection_timestamp', datetime.utcnow().isoformat())),
            confidence_score=data.get('confidence_score', 0.0),
            image_path=data.get('image_path'),
            speed_limit=data['speed_limit'],
            recommended_speed=data['recommended_speed'],
            verified=data.get('verified', False),
            road_name=data['road_name'],
            area=data['area'],
            weather_condition=data.get('weather_condition')
        ) 