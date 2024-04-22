import unittest
from datetime import datetime, timedelta
import uuid
import pickle

from step23  import Transaction, CityObject, Owner, Event, CityEventRegistr


class TestCityObject(unittest.TestCase):

    def setUp(self):
        self.city_obj = CityObject(
            name="Museum", objType="Cultural", address="123 Main St", capacity=100,
            owner="ABC Corp", openingDate=datetime.strptime("2024-01-01", "%Y-%m-%d")
        )

    def test_destructor_city_object(self):
        del self.city_obj
        # Print statement for destroyed object is in the destructor itself

    def test_add_transaction_city_object(self):
        self.city_obj.addTransaction('Update Capacity', 100, 120)

        self.assertEqual(len(self.city_obj.transactions), 1)
        self.assertEqual(self.city_obj.transactions[0].operation, 'Update Capacity')
        self.assertEqual(self.city_obj.transactions[0].oldValue, 100)
        self.assertEqual(self.city_obj.transactions[0].newValue, 120)

    def test_add_event_city_object(self):
        event_date = datetime(year=2024, month=4, day=25).strftime("%Y-%m-%d")
        self.city_obj.addEvent(event_date, "Art Exhibition", "Art", 50)

        self.assertEqual(len(self.city_obj.events), 1)
        self.assertEqual(self.city_obj.events[0].eventName, "Art Exhibition")
        self.assertEqual(self.city_obj.events[0].eventType, "Art")
        self.assertEqual(self.city_obj.events[0].visitors, 50)

        # Check transaction for adding event
        self.assertEqual(len(self.city_obj.transactions), 1)  # One for capacity, one for adding event
        self.assertEqual(self.city_obj.transactions[1].operation, "addEvent")
        self.assertIsInstance(self.city_obj.transactions[1].oldValue, list)
        self.assertIsInstance(self.city_obj.transactions[1].newValue, list)

    def test_close_object_city_object(self):
        closure_date = datetime(year=2024, month=4, day=23).strftime("%Y-%m-%d")
        self.city_obj.closeObject(closure_date)

        self.assertEqual(self.city_obj.closureDate.strftime("%Y-%m-%d"), closure_date)

        # Check transaction for closing object
        self.assertEqual(len(self.city_obj.transactions), 2)  # One for capacity, one for adding event, one for closing
        self.assertEqual(self.city_obj.transactions[2].operation, "closeObject")
        self.assertIsInstance(self.city_obj.transactions[2].oldValue, type(None))
        self.assertEqual(self.city_obj.transactions[2].newValue, closure_date)

    def test_reopen_object_city_object(self):
        closure_date = datetime(year=2024, month=4, day=23).strftime("%Y-%m-%d")
        reopening_date = datetime(year=2024, month=4, day=24).strftime("%Y-%m-%d")
        self.city_obj.closeObject(closure_date)
        self.city_obj.reopenObject(reopening_date)

        self.assertEqual(self.city_obj.closureDate, None)

        # Check transaction for reopening object
        self.assertEqual(len(self.city_obj.transactions), 2)  # All previous + reopening
        self.assertEqual(self.city_obj.transactions[0].operation, "reopenObject")
        self.assertEqual(self.city_obj.transactions[0].oldValue, closure_date)
        self.assertEqual(self.city_obj.transactions[0].newValue, None)

    def test_serialize_city_object(self):
        filename = "city_object_state.pkl"
        self.city_obj.saveState(filename)

        loaded_city_obj = CityObject.loadState(filename)

        # Compare attributes of the original and loaded objects
        self.assertEqual(self.city_obj.id, loaded_city_obj.id)  # Unique ID should be the same
        self.assertEqual(self.city_obj.name, loaded_city_obj.name)
        self.assertEqual(self.city_obj.objType, loaded_city_obj.objType)
        self.assertEqual(self.city_obj.adress, loaded_city_obj.adress)
        self.assertEqual(self.city_obj.capacity, loaded_city_obj.capacity)
        self.assertEqual(self.city_obj.owner, loaded_city_obj.owner)
        self.assertIsInstance(self.city_obj.openingDate, datetime)  # Check date type
        self.assertEqual(self.city_obj.openingDate.strftime("%Y-%m-%d"), loaded_city_obj.openingDate.strftime("%Y-%m-%d"))
        self.assertEqual(len(self.city_obj.transactions), len(loaded_city_obj.transactions))
        # You may need to add additional comparisons for transactions based on their attributes

        # Optional: Check transaction details (consider using a loop)
        for i in range(len(self.city_obj.transactions)):
            self.assertEqual(self.city_obj.transactions[i].operation, loaded_city_obj.transactions[i].operation)
            self.assertEqual(self.city_obj.transactions[i].oldValue, loaded_city_obj.transactions[i].oldValue)
            self.assertEqual(self.city_obj.transactions[i].newValue, loaded_city_obj.transactions[i].newValue)

        # Clean up the temporary file
        import os
        os.remove(filename)
if __name__ == '__main__':
    unittest.main()