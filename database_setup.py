''''Initial Configuration'''
import sys
from sqlalchemy import Column,ForeignKey,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

'''Table Information along with Mappers'''
class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80),nullable=False)
    id = Column(Integer,primary_key=True)



class Character(Base):
    __tablename__ = 'character'
    name = Column(String(80),nullable=False)
    id = Column(Integer,primary_key=True)
    playedBy = Column(String(80))
    imageUrl = Column(String())
    gender = Column(String(10))
    died = Column(String())
    born = Column(String())
    culture = Column(String())

class House(Base):
    __tablename__ = 'house'
    name = Column(String(80),nullable=False)
    id = Column(Integer,primary_key=True)
    coatOfArms = Column(String())
    region = Column(String())
    titles = Column(String())
    words = Column(String())
    currentLord = Column(Integer(),ForeignKey('character.id'))
    character = relationship(Character)


class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80),nullable=False)
    id = Column(Integer,primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course,
        }

'''Final Configuration'''
engine = create_engine('sqlite:///gameofthrones.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

if __name__ == '__main__':

    from firebase import firebase
    from Retreiver import *

    base_url = "https://game-of-thrones-1e480.firebaseio.com/"

    firebase = firebase.FirebaseApplication(base_url, None)

    result = getHouses(firebase)

    print result

    counter = 0
    for i in result :
        if i is not None :
            region = i['region']
            coatOfArms = i['coatOfArms']
            words = i['words']
            name = i['name']
            currentLord = i['currentLord']
            house = House(name=name,currentLord=currentLord,words=words,coatOfArms=coatOfArms,id=counter,region=region)
            session.add(house)
            session.commit()
        counter+=1
    res = session.query(House).all()
    print res
    '''
    counter = 0
    for i in result:
        if i is not None:
            name = i['name']
            culture = i['culture']
            playedBy = i['playedBy']
            try:
                imageUrl = i['imageUrl']
            except KeyError:
                imageUrl="https://msudenver.edu/media/sampleassets/profile-placeholder.png"
            born = i['born']
            died = i['died']
            gender = i['gender']
            print "ID " , counter , " Name " , name
            character = Character(name=name, culture=culture, id=counter,born=born,died=died,imageUrl=imageUrl,playedBy=playedBy,gender=gender)
            session.add(character)
            session.commit()
        counter += 1
    res = session.query(Character).all()
    '''
