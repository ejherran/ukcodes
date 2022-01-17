from typing import Any
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

#engine = sqlalchemy.create_engine("mysql+pymysql://root:example@localhost:13306/example")

Base = declarative_base()

class Coordinate(Base):
    __tablename__ = 'coordinate'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    latitude = sqlalchemy.Column(sqlalchemy.Float)
    longitude = sqlalchemy.Column(sqlalchemy.Float)

class Postcode(Base):
    __tablename__ = 'postcode'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    coordinate_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('coordinate.id'))
    postcode = sqlalchemy.Column(sqlalchemy.String(25))
    quality = sqlalchemy.Column(sqlalchemy.INTEGER)
    eastings = sqlalchemy.Column(sqlalchemy.INTEGER)
    northings = sqlalchemy.Column(sqlalchemy.INTEGER)
    country = sqlalchemy.Column(sqlalchemy.String(100))
    nhs_ha = sqlalchemy.Column(sqlalchemy.String(100))
    longitude = sqlalchemy.Column(sqlalchemy.Float)
    latitude = sqlalchemy.Column(sqlalchemy.Float)
    european_electoral_region = sqlalchemy.Column(sqlalchemy.String(100))
    primary_care_trust = sqlalchemy.Column(sqlalchemy.String(100))
    region = sqlalchemy.Column(sqlalchemy.String(100))
    lsoa = sqlalchemy.Column(sqlalchemy.String(100))
    msoa = sqlalchemy.Column(sqlalchemy.String(100))
    incode = sqlalchemy.Column(sqlalchemy.String(100))
    outcode = sqlalchemy.Column(sqlalchemy.String(100))
    parliamentary_constituency = sqlalchemy.Column(sqlalchemy.String(100))
    admin_district = sqlalchemy.Column(sqlalchemy.String(100))
    parish = sqlalchemy.Column(sqlalchemy.String(100))
    admin_county = sqlalchemy.Column(sqlalchemy.String(100))
    admin_ward = sqlalchemy.Column(sqlalchemy.String(100))
    ced = sqlalchemy.Column(sqlalchemy.String(100))
    ccg = sqlalchemy.Column(sqlalchemy.String(100))
    nuts = sqlalchemy.Column(sqlalchemy.String(100))
    distance = sqlalchemy.Column(sqlalchemy.Float)

class Codes(Base):
    __tablename__ = 'codes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    postcode_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('postcode.id'))
    admin_district = sqlalchemy.Column(sqlalchemy.String(10))
    admin_county = sqlalchemy.Column(sqlalchemy.String(10))
    admin_ward = sqlalchemy.Column(sqlalchemy.String(10))
    parish = sqlalchemy.Column(sqlalchemy.String(10))
    parliamentary_constituency = sqlalchemy.Column(sqlalchemy.String(10))
    ccg = sqlalchemy.Column(sqlalchemy.String(10))
    ccg_id = sqlalchemy.Column(sqlalchemy.String(10))
    ced = sqlalchemy.Column(sqlalchemy.String(10))
    nuts = sqlalchemy.Column(sqlalchemy.String(10))
    lsoa = sqlalchemy.Column(sqlalchemy.String(10))
    msoa = sqlalchemy.Column(sqlalchemy.String(10))
    lau2 = sqlalchemy.Column(sqlalchemy.String(10))

class Db:

    def __init__(self, url: str) -> None:
        self.engine = sqlalchemy.create_engine(url)
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)()
    
    def create_schema(self, Base: Any) -> None:
        Base.metadata.create_all(self.engine)
    
    def disconnect(self) -> None:
        self.session.close()
        self.engine.dispose()

    def insert_coordinate(self, coordinate: dict) -> sqlalchemy.Integer:
        
        entity = Coordinate()
        entity.latitude = coordinate['latitude']
        entity.longitude = coordinate['longitude']
        
        self.session.add(entity)
        self.session.commit()

        return entity.id
    
    def insert_postcode(self, postcode: dict, coordinate_id: sqlalchemy.Integer) -> sqlalchemy.Integer:
        
        entity = Postcode()
        entity.coordinate_id = coordinate_id
        entity.postcode = postcode['postcode']
        entity.quality = postcode['quality']
        entity.eastings = postcode['eastings']
        entity.northings = postcode['northings']
        entity.country = postcode['country']
        entity.nhs_ha = postcode['nhs_ha']
        entity.longitude = postcode['longitude']
        entity.latitude = postcode['latitude']
        entity.european_electoral_region = postcode['european_electoral_region']
        entity.primary_care_trust = postcode['primary_care_trust']
        entity.region = postcode['region']
        entity.lsoa = postcode['lsoa']
        entity.msoa = postcode['msoa']
        entity.incode = postcode['incode']
        entity.outcode = postcode['outcode']
        entity.parliamentary_constituency = postcode['parliamentary_constituency']
        entity.admin_district = postcode['admin_district']
        entity.parish = postcode['parish']
        entity.admin_county = postcode['admin_county']
        entity.admin_ward = postcode['admin_ward']
        entity.ced = postcode['ced']
        entity.ccg = postcode['ccg']
        entity.nuts = postcode['nuts']
        entity.distance = postcode['distance']

        self.session.add(entity)
        self.session.commit()

        return entity.id
    
    def insert_codes(self, codes: dict, postcode_id: sqlalchemy.Integer) -> sqlalchemy.Integer:

        entity = Codes()
        entity.postcode_id = postcode_id
        entity.admin_district = codes['admin_district']
        entity.admin_county = codes['admin_county']
        entity.admin_ward = codes['admin_ward']
        entity.parish = codes['parish']
        entity.parliamentary_constituency = codes['parliamentary_constituency']
        entity.ccg = codes['ccg']
        entity.ccg_id = codes['ccg_id']
        entity.ced = codes['ced']
        entity.nuts = codes['nuts']
        entity.lsoa = codes['lsoa']
        entity.msoa = codes['msoa']
        entity.lau2 = codes['lau2']

        self.session.add(entity)
        self.session.commit()

        return entity.id
