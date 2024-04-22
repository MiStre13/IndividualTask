from datetime import datetime, timedelta
import uuid
import pickle



class Transaction:
    def __init__(self, timestamp, operation, oldValue, newValue):
        self.timestamp = timestamp
        self.operation = operation
        self.oldValue = oldValue
        self.newValue = newValue
     
    def __str__(self):
        return f"Transaction: timestamp={self.timestamp}, operation={self.operation}, oldValue={self.oldValue}, newValue={self.newValue}"


class CityObject:
    def __init__(self, name=None, objType=None, capacity=0, owner=None, openingDate=None, **kwargs):
        self.id = uuid.uuid4()
        self.name = name
        self.objType = objType
        self.adress = kwargs.get('adress', None)
        self.capacity = capacity
        self.owner = owner
        self.openingDate = openingDate
        self.closureDate = None
        self.events = []
        self.transactions = []

    def addTransaction(self, operation, oldValue, newValue):
        transaction = Transaction(datetime.now(), operation, oldValue, newValue)
        self.transactions.append(transaction)

    def __str__(self):
        return f"CityObject(id={self.id}, name={self.name}, objType={self.objType}, adress={self.adress}, capacity={self.capacity}, owner={self.owner}, openingDate={self.openingDate})"

    def addEvent(self, eventDate, eventName, eventType, visitors):
        old_events = self.events.copy()
        self.events.append(Event(eventDate, eventName, eventType, visitors))
        new_events = self.events
        self.transactions.append((datetime.utcnow(), "addEvent", "events", old_events, new_events))

    def closeObject(self, closureDate):
        old_closureDate = self.closureDate
        self.closureDate = closureDate
        self.transactions.append((datetime.utcnow(), "closeObject", "closureDate", old_closureDate, closureDate))

    def reopenObject(self, reopening_date):
        self.closureDate = None
        transaction = Transaction(datetime.now(), "reopenObject", self.closureDate, reopening_date)
        self.transactions.append(transaction)
    
    def saveState(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    # @staticmethod
    def loadState(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)

    def __del__(self):
        print(f"CityObject {self.name} has been destroyed")

    


class Owner:
    def __init__(self, nameCompany=None, nameOwner=None, ownerType=None, contactPhone="+79999999999"):
        self.id = uuid.uuid4()
        self.nameCompany = nameCompany
        self.nameOwner = nameOwner
        self.ownerType = ownerType
        self.contactPhone = contactPhone
        self.transactions = []

    def __str__(self):
        return f"Owner(id={self.id}, nameCompany={self.nameCompany}, nameOwner={self.nameOwner}, ownerType={self.ownerType}, contactPhone={self.contactPhone})"

    def saveState(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def loadState(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)

    def __del__(self):
        print(f"Owner {self.nameOwner} from {self.nameCompany} has been destroyed")

class Event:
    def __init__(self, eventDate=None, eventName=None, eventType=None, visitors=0):
        self.id = uuid.uuid4()
        self.eventDate = eventDate
        self.eventName = eventName
        self.eventType = eventType
        self.visitors = visitors
        self.transactions = []

    def __str__(self):
        return f"Event(id={self.id}, eventDate={self.eventDate}, eventName={self.eventName}, eventType={self.eventType}, visitors={self.visitors})"

    def saveState(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def loadState(filename):
        with open(filename, "rb") as file:
            return pickle.load(file)

    def __del__(self):
        print(f"Event {self.eventName} on {self.eventDate} has been destroyed")


class CityEventRegistr:
    def __init__(self):
        self.objects = []

    def addObject(self, obj):
        self.objects.append(obj)

    def getCurrentObject(self, currentDate):
        return [obj for obj in self.objects if obj.openingDate <= currentDate and (obj.closureDate is None or obj.closureDate > currentDate)]
    
    def upcomingEvents(self, currentDate, daysAhead=14):
        upcomingEvents = []
        for obj in self.objects:
            for event in obj.events:
                eventDate = datetime.strptime(event.eventDate, "%Y-%m-%d")
                if currentDate <= eventDate <= currentDate + timedelta(days=daysAhead):
                    upcomingEvents.append((event.eventDate, event.eventName, obj.name, obj.adress, event.visitors))
        return upcomingEvents
    
    def getObjectsByType(self, objType, currentDate):
        return [obj for obj in self.objects if obj.objType == objType and obj.openingDate <= currentDate and (obj.closureDate is None or obj.closureDate > currentDate)]


# Создаем объект CityObject
city_obj = CityObject(name="Museum", objType="Cultural", address="123 Main St", capacity=100, owner="ABC Corp", openingDate="2022-01-01")

# Добавляем транзакцию
city_obj.addTransaction('Update Capacity', 100, 120)

# Сохраняем состояние объекта в файл
filename = "city_object_state.pkl"
city_obj.saveState(filename)

# Загружаем состояние объекта из файла
loaded_city_obj = CityObject.loadState(filename)

# Печатаем загруженный объект и его транзакции
print("Печатаем",loaded_city_obj.name)

print("Транзакции:")
for transaction in loaded_city_obj.transactions:
  print(transaction)


# if __name__ == "__main__":
#     owner1 = Owner("Plumit", "Стрельцов М.А.", "Индивидуальный П.", "+79532663211")

#     object1 = CityObject("Галерея", "Жилое здание", "Павла Усова", 20, owner1, datetime(2024, 4, 15))
#     object1.addEvent("2024-04-18", "Разработка задания", "Работа", 20)

#     registration = CityEventRegistr()
#     registration.addObject(object1)

#     currentDate = datetime.strptime("2024-04-18", "%Y-%m-%d")

#     currentObjects = registration.getCurrentObject(currentDate)
#     currentThisNumber = 0
#     print("Текущие объекты: ") #Вывод списка место проведения мероприятий
#     for obj in currentObjects:
#         currentThisNumber += 1
#         print(currentThisNumber, "Название здания:",obj.name, "Тип здания:", obj.objType, "Адрес:",obj.adress)

#     print("Мероприятия в ближайшие две недели:")
#     upcomingEvents = registration.upcomingEvents(currentDate, daysAhead = 14)
#     for objEvent in upcomingEvents:
#         print(f"Дата: {objEvent[0]}, Название: {objEvent[1]}, Место: {objEvent[2]}, Адрес:{objEvent[3]}, Свободных Мест:{objEvent[4]}")


#     objType = "Жилое здание"
#     print("Список объектов заданного типа на текущую дату:")
#     objectByType = registration.getObjectsByType(objType, currentDate)
#     for objTime in objectByType:
#         print(f"{objTime.name} - Адрес {objTime.adress}")