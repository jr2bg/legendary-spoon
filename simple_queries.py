import configparser

from sqlalchemy import create_engine, func, and_
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import declarative_base, sessionmaker

base = declarative_base()

class Profiles(base):
    __tablename__ = "mock_profiles_first"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    address = Column(String)
    expertise = Column(Date)
    position = Column(String)
    phone_number = Column(String)
    email = Column(String)

    def __repr__(self) -> str:
        return f"id: {self.id}; name: {self.name}; country: {self.country}; "\
                f"address: {self.address}; entry-date: {self.expertise}; " \
                f"position: {self.position}; phone_number:{self.phone_number}; "\
                f"email:{self.email}"

def read_psql_configuration(filename:str):
    config = configparser.ConfigParser()
    config.read(filename)

    return config["PSQL"]

def create_session():
    print("creating session")
    psql_config = read_psql_configuration("config.ini")
    db_string = f"postgresql://{psql_config['username']}:"\
                f"{psql_config['password']}@{psql_config['ip_address']}:"\
                f"{psql_config['port']}/{psql_config['db']}"
    engine = create_engine(db_string)

    Session = sessionmaker(bind=engine)
    session = Session()

    print("session created")

    return session

def get_eg_data(session):
    selected_countries = ["Rwanda", "Liechtenstein", "Russian Federation"]
    selected_positions = ["Dietitian"]

    profiles = session.query(Profiles) \
                        .filter(and_(
                                func.extract('years',func.age(Profiles.expertise)) < 5,
                                func.extract('years',func.age(Profiles.expertise)) >= 3,
                                Profiles.country.in_(selected_countries),
                                Profiles.position.in_(selected_positions))
                        ) \
                        .order_by(func.age(Profiles.expertise).desc()) \
                        .all()

    i = 0
    for profile in profiles:
        print(i, profile)
        i += 1

def get_data(countries, positions, experience):
    """
    Function to get the info from the database
    form_data has the info for the time interval, countries
    and positions to search to
    countries
    positions
    experience
    """
    print(countries)
    print(positions)
    session = create_session()

    map_exp = {
        "trainee": (0,1), 
        "jr": (1,3),
        "mid":(3,5),
        "sr":(5,100)
        }
    
    min_exp = map_exp[experience][0]
    max_exp = map_exp[experience][1]

    profiles = session.query(Profiles) \
        .filter(and_(
                func.extract('years',func.age(Profiles.expertise)) < max_exp,
                func.extract('years',func.age(Profiles.expertise)) >= min_exp,
                Profiles.country.in_(countries),
                Profiles.position.in_(positions))
        ) \
        .order_by(func.age(Profiles.expertise).desc()) \
        .all()
    
    # get_eg_data(session)

    for profile in profiles:
        print(profile)

if __name__ == "__main__":
    get_eg_data(create_session())