# -*- coding: utf-8 -*-
import time
import string
import random
import pandas as pd

class CarRentalService:
    def __init__(self,):
        self.rentalCars = {"Compact":{'Available':'Yes',"BaseDayRental":1000,"KilometerPrice":15,'Records':[]}, "Premium":{'Available':'Yes',"BaseDayRental":2000,"KilometerPrice":20,"Records":[]}, "Minivan":{'Available':'Yes',"BaseDayRental":3000,"KilometerPrice":25,"Records":[]}}
        
    def addCarType(self, carType):
        if carType not in set(self.rentalCars.keys()):
            baseDayRental = int(input("Please enter base day rental for car :\n"))
            kmPrice = int(input("Please enter per kilometer price :\n"))
            self.rentalCars[carType] = {'Available':'Yes',"BaseDayRental":baseDayRental,"KilometerPrice":kmPrice,'Records':[]}
            print(carType," type has been added in car catogory list.\n")
            return self.rentalCars, ""
        else:
            return self.rentalCars, carType+" is alredy present.\n"
    
    def registerCarOnRent(self, carType, cxName):
        if self.rentalCars[carType]['Available'] == 'Yes':
            timeString = str(time.localtime()[:4]).replace('(','').replace(')','').replace(',','').strip()
            formatedTimeString = timeString.translate({ord(c): None for c in string.whitespace})
            self.bookingNumber = cxName[:3].upper()+str(random.randint(1, 1000))+formatedTimeString
            print("Your Booking number is : ", self.bookingNumber)
            date = [str(item) for item in list(time.localtime()[:3])]
            self.carPickupdate = "-".join(date)
            self.carPickuptime = list(time.localtime()[3:5])
            self.carMileageatpickup = int(input("Mileage at pickup time:\n"))
            try:
                temp_dict = {"BookingNumber": self.bookingNumber,
                            "CustName" : cxName,
                             "CarpickupDate" : self.carPickupdate,
                             "CarpickupTime" : str(self.carPickuptime[0])+'Hr'+str(self.carPickuptime[1])+'Sec',
                             "CarMileageatpickup" : self.carMileageatpickup,
                             "CarReturnDate" : "",
                             "CarReturnTime": "",
                             "CarMileageAtReturn" : ""}
                self.rentalCars[carType]["Records"].append(temp_dict)
                self.rentalCars[carType]['Available'] = 'No'
                time.sleep(2)
                print("Registeration has been successfully done.\n")
                return self.rentalCars, ""
            except Exception as e:
                print(e)
                return self.rentalCars, "Unable to register the user.\n"
        else:
            return self.rentalCars, "The car is in use. Please use other available cars. Thank you!\n"
    
    def returnCar(self,bookingNumber,carType):
        records = self.rentalCars[carType]["Records"]
        basePrice = self.rentalCars[carType]["BaseDayRental"]
        perKmPrice = self.rentalCars[carType]["KilometerPrice"]
        for record in records:
            if record["BookingNumber"] == bookingNumber:
                date = [str(item) for item in list(time.localtime()[:3])]
                self.carReturndate = "-".join(date)
                self.carReturntime = list(time.localtime()[3:5])
                self.carMileageatreturn = int(input("Mileage at return time:\n"))
                record["CarReturnDate"] = self.carReturndate
                record["CarReturnTime"] = str(self.carReturntime[0])+'Hr'+str(self.carReturntime[1])+'Sec'
                record["CarMileageAtReturn"] = self.carMileageatreturn
                print("Calculating Car Fare Please Wait.....\n\n")
                time.sleep(2)
                carfare, err = self.totalFare(carType,record,basePrice,perKmPrice)
                if err != "":
                    print(err)
                else:    
                    print("******** Total Car Fare is :", carfare,"Rs. ***************")
                    self.rentalCars[carType]['Available'] = 'Yes'
                    return self.rentalCars, ""
            else:
                return self.rentalCars, "Invalid Booking Id."
                
    
    def totalFare(self,carType,record,baseDayRental,kilometerPrice):
        if carType == 'Compact':
            compactCarFare = 0
            try:
                numberOfDays = int(record["CarReturnDate"].split("-")[-1]) - int(record["CarpickupDate"].split("-")[-1])
                if numberOfDays == 0:
                    numberOfDays = 1
                compactCarFare = baseDayRental * numberOfDays
                return compactCarFare, ""
            except Exception as e:
                print(e)    
                return compactCarFare, "Unable to calculate the car fare"
        elif carType == "Premium":
            premiumCarFare = 0
            try:
                numberOfDays = int(record["CarReturnDate"].split("-")[-1]) - int(record["CarpickupDate"].split("-")[-1]) 
                numberOfKilometers = record["CarMileageAtReturn"] - record["CarMileageatpickup"]
                if numberOfDays == 0:
                    numberOfDays = 1
                premiumCarFare = baseDayRental * numberOfDays * 1.2 + kilometerPrice * numberOfKilometers
                return premiumCarFare, ""
            except Exception as e:
                print(e)
                return premiumCarFare, "Unable to calculate the car fare"
        elif carType == "Minivan":
            try:
                numberOfDays = int(record["CarReturnDate"].split("-")[-1]) - int(record["CarpickupDate"].split("-")[-1]) 
                numberOfKilometers = record["CarMileageAtReturn"] - record["CarMileageatpickup"]
                if numberOfDays == 0:
                    numberOfDays = 1
                minivanCarFare = baseDayRental * numberOfDays * 1.7 + (kilometerPrice * numberOfKilometers * 1.5 )
                return minivanCarFare,""
            except Exception as e:
                print(e)
                return minivanCarFare, "Unable to calculate the car fare"
        else:
            otherCarFare = 0
            try:
                numberOfDays = int(record["CarReturnDate"].split("-")[-1]) - int(record["CarpickupDate"].split("-")[-1]) 
                numberOfKilometers = record["CarMileageAtReturn"] - record["CarMileageatpickup"]
                if numberOfDays == 0:
                    numberOfDays = 1
                otherCarFare = baseDayRental * numberOfDays * 1.0 + kilometerPrice * numberOfKilometers
                return otherCarFare, ""
            except Exception as e:
                print(e)
                return otherCarFare, "Unable to calculate the car fare"



if __name__ == '__main__':
    rs = CarRentalService()
    conFlag = True
    print("Hello! Welcome to XYZ Car Rental Service\n")
    print("                   Administration             ")
    while conFlag:
        print("1.Add New Car Category \n2.Rental Car Registration \n3.Car Return \n4.Save Data \n5.Logout")
        choice = int(input("Please select the service\n"))
        match choice:
            case 1:
                print("----------------- Car Add Service-----------------------")
                carType = input("Please enter car type that you want to add.\n")
                rental_cars, err = rs.addCarType(carType)
                if err != "":
                    print(err)
                
            case 2:
                print("-----------------Car Rental Registration Service-----------------------")
                print("Available Car Type\n")
                for car in list(rs.rentalCars.keys()):
                    print(list(rs.rentalCars.keys()).index(car)+1,".",car)
                cxName = input("Please enter customer full name.\n")
                cartypeOnRent = input("Please enter car type which you want on rent.\n")
                if cartypeOnRent not in set(rs.rentalCars.keys()):
                    print("Please enter available cars.")
                else:        
                    rental_cars, err = rs.registerCarOnRent(cartypeOnRent, cxName)
                    if err != "":
                        print(err)
            case 3:
                print("-----------------Car Rental Registration Service-----------------------")
                bookingNumber = input("Please Enter booking ID :\n")
                carType = input("Please enter return car type :\n")
                rental_cars, err = rs.returnCar(bookingNumber, carType)
                if err != "":
                    print(err)    
            case 4:
                print("Saving records...")
                time.sleep(2)
                try:
                    df_data = pd.DataFrame().from_dict(rental_cars)
                    df_data.to_csv('./records.csv')
                    print("Record has been saved with filename 'records.csv'.\n")
                except Exception as e:
                    print(e)
            case 5:
                conFlag = False
    
    
                
                
                    
                    
    
    