import unittest
from step23 import CityObject  # предполагается, что класс CityObject определен в отдельном файле

class TestCityObjectMethods(unittest.TestCase):
    
    def setUp(self):
        # Создаем объект CityObject для тестирования
        self.city_obj = CityObject(name="Museum", objType="Cultural", adress="123 Main St", capacity=100, owner="ABC Corp", openingDate="2022-01-01")
    
    def test_transaction(self):
        # Добавляем транзакцию и проверяем ее
        self.city_obj.addTransaction('Update Capacity', 100, 120)
        self.assertEqual(self.city_obj.transactions[0].oldValue, 100)
        self.assertEqual(self.city_obj.transactions[0].newValue, 120)
    
    def test_destructor(self):
        # Тестирование деструктора объекта
        del self.city_obj
        # Проверяем, что объект city_obj удален
        with self.assertRaises(AttributeError):
            getattr(self, 'city_obj')
    
    def test_serialization(self):
        # Сохраняем и загружаем состояние объекта
        filename = "test_city_object_state.pkl"
        self.city_obj.saveState(filename)
        loaded_city_obj = CityObject.loadState(filename)
        self.assertEqual(self.city_obj.name, loaded_city_obj.name)
        self.assertEqual(self.city_obj.objType, loaded_city_obj.objType)
        self.assertEqual(self.city_obj.adress, loaded_city_obj.adress)
        self.assertEqual(self.city_obj.capacity, loaded_city_obj.capacity)
        self.assertEqual(self.city_obj.owner, loaded_city_obj.owner)
        self.assertEqual(self.city_obj.openingDate, loaded_city_obj.openingDate)
        self.assertEqual(self.city_obj.transactions, loaded_city_obj.transactions)

if __name__ == '__main__':
    unittest.main()
