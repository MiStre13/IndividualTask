import unittest
from datetime import datetime
from step24 import Park, Library

class TestCityObjects(unittest.TestCase):
    def test_park_greenArea(self):
        park = Park(name="Central Park", objType="Park", adress="Central Park, NY", capacity=1000, owner="City of New York", openingDate="2022-01-01", greenArea=5000)
        self.assertEqual(park.get_attribute("greenArea"), 5000)
        
        park.set_attribute("greenArea", 6000)
        self.assertEqual(park.get_attribute("greenArea"), 6000)
        
    def test_library_bookCount(self):
        library = Library(name="Main Library", objType="Library", adress="Downtown, City", capacity=500, owner="Public Library System", openingDate="2022-01-01", bookCount=10000)
        self.assertEqual(library.get_attribute("bookCount"), 10000)
        
        library.set_attribute("bookCount", 12000)
        self.assertEqual(library.get_attribute("bookCount"), 12000)
        
    def test_park_addMaintenanceEvent(self):
        park = Park(name="Community Park", objType="Park", adress="Community Park, TX", capacity=500, owner="City of Community", openingDate="2022-01-01", greenArea=2000)
        park.addMaintenanceEvent(eventDate="2022-02-01", eventName="Maintenance Day", eventType="Maintenance", visitors=50, maintenanceType="Regular")
        self.assertEqual(len(park.transactions), 1)
        
    def test_park_str_method(self):
        park = Park(name="Town Park", objType="Park", adress="Town Park, CA", capacity=300, owner="Town Council", openingDate="2022-01-01", greenArea=1500)
        self.assertEqual(park.str(), "Park(id={}, name=Town Park, objType=Park, adress=Town Park, CA, capacity=300, owner=Town Council, openingDate=2022-01-01, greenArea=1500)".format(park.id))
        
if __name__ == '__main__':
    unittest.main()
