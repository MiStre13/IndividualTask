import unittest
from mainStep22 import CityObject, Owner, Event, CityEventRegistr    

class TestCityObjectMethods(unittest.TestCase):

    def test_default_constructor(self):
        city = CityObject()
        self.assertIsNotNone(city.id)
    
    def test_string_representation(self):
        city = CityObject(name='TestCity', objType='TestType')
        self.assertEqual(str(city), "CityObject(id={}, name=TestCity, objType=TestType, adress=None, capacity=0, owner=None, openingDate=None)".format(city.id))

    def test_id_generation(self):
        city1 = CityObject()
        city2 = CityObject()
        self.assertNotEqual(city1.id, city2.id)

class TestOwnerMethods(unittest.TestCase):

    def test_default_constructor(self):
        owner = Owner()
        self.assertIsNotNone(owner.id)
    
    def test_string_representation(self):
        owner = Owner(nameCompany='TestCompany', nameOwner='TestOwner')
        self.assertEqual(str(owner), "Owner(id={}, nameCompany=TestCompany, nameOwner=TestOwner, ownerType=None, contactPhone=+79999999999)".format(owner.id))


class TestEventMethods(unittest.TestCase):

    def test_default_constructor(self):
        event = Event()
        self.assertIsNotNone(event.id)
    
    def test_string_representation(self):
        event = Event(eventName='TestEvent', eventType='TestType')
        self.assertEqual(str(event), "Event(eventDate=None, eventName=TestEvent, eventType=TestType, visitors=0)".format(event.id))

class TestCityEventRegistrMethods(unittest.TestCase):

    def setUp(self):
        self.registration = CityEventRegistr()
    
    def test_addObject(self):
        city = CityObject(name='TestCity', objType='TestType')
        self.registration.addObject(city)
        self.assertIn(city, self.registration.objects)
 

# city = CityObject(id="a99129b5-8413-4692-a65c-e2dd519c7ec1", name="Test City", objType="Test Type", adress=None, capacity=0, owner=None, openingDate=None)
# print(str(city))

if __name__ == '__main__':
    unittest.main()

