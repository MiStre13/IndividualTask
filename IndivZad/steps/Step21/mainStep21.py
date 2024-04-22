from datetime import datetime, timedelta


class CityObject:
    def __init__(self, name, objType, adress, capacity, owner, openingDate):
        self.name = name
        self.objType = objType
        self.adress = adress
        self.capacity = capacity
        self.owner = owner
        self.openingDate = openingDate
        self.closureDate = None
        self.events = []
    
    def addEvent(self, eventDate, eventName, eventType, visitors):
        self.events.append(Event(eventDate, eventName, eventType, visitors))
    
    def closeObject(self, closureDate):
        self.closureDate = closureDate

    def reopenObject(self, reopeningDate):
        self.reopeninDate = reopeningDate
        self.closureDate = None

class Owner:
    def __init__(self, nameCompany, nameOwner, ownerType, contactPhone):
        self.nameCompany = nameCompany
        self.nameOwner = nameOwner
        self.ownerType = ownerType
        self.contactPhone = contactPhone
    

class Event:
    def __init__(self, eventDate, eventName, eventType, visitors):
        self.eventDate = eventDate
        self.eventName = eventName
        self.eventType = eventType
        self.visitors = visitors


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



if __name__ == "__main__":
    owner1 = Owner("Plumit", "Стрельцов М.А.", "Индивидуальный П.", "+79532663211")

    object1 = CityObject("Галерея", "Жилое здание", "Павла Усова", 20, owner1, datetime(2024, 4, 15))
    object1.addEvent("2024-04-18", "Разработка задания", "Работа", 20)

    registration = CityEventRegistr()
    registration.addObject(object1)

    currentDate = datetime.strptime("2024-04-18", "%Y-%m-%d")

    currentObjects = registration.getCurrentObject(currentDate)
    currentThisNumber = 0
    print("Текущие объекты: ") #Вывод списка место проведения мероприятий
    for obj in currentObjects:
        currentThisNumber += 1
        print(currentThisNumber, "Название здания:",obj.name, "Тип здания:", obj.objType, "Адрес:",obj.adress)

    print("Мероприятия в ближайшие две недели:")
    upcomingEvents = registration.upcomingEvents(currentDate, daysAhead = 14)
    for objEvent in upcomingEvents:
        print(f"Дата: {objEvent[0]}, Название: {objEvent[1]}, Место: {objEvent[2]}, Адрес:{objEvent[3]}, Свободных Мест:{objEvent[4]}")


    objType = "Жилое здание"
    print("Список объектов заданного типа на текущую дату:")
    objectByType = registration.getObjectsByType(objType, currentDate)
    for objTime in objectByType:
        print(f"{objTime.name} - Адрес {objTime.adress}")

    

    

