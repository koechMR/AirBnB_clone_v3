from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv

# Define a dictionary of classes
classes = {
    'BaseModel': BaseModel,
    'City': City,
    'State': State,
    'Amenity': Amenity,
    'Place': Place,
    'Review': Review,
    'User': User
}

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects of a specific class or all objects"""
        obj_dict = {}
        if cls:
            if isinstance(cls, str) and cls in classes:
                cls = classes[cls]
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for cls in classes.values():
                objs.extend(self.__session.query(cls).all())
        for obj in objs:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add an object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload data from the database"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve an object"""
        return self.all(cls).get('{}.{}'.format(cls.__name__, id))

    def count(self, cls=None):
        """Count the number of objects"""
        return len(self.all(cls))
