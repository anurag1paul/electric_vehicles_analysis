# MPGe to Kwh/1mile :
#     kwh/100km = 3370.5 / 1.609344 / MPGe
#     kwh/1km = kwh/100km /100
#     kwh/1mile = kwh/1km / 0.621371
#   ->kwh/1mile = 33.7 / MPGe
def ele_Cost(miles,elePrice,MPGe):
    '''
    Compute the total electricity cost of ev cars
    @miles : total miles for a certain type of user
    @elePrice : electricity price in each state
    @MPGe : EV car's MPGe
    @return : total cost in dollars for charging EV
    '''
    totalEle = miles * 33.7 / MPGe
    return totalEle * elePrice #eleprice should be in dollars/kwh

def fuel_Cost(miles,fuelPrice,mpg):
    '''
    Compute the total fuel cost of a fuel car
    @milse: total miles
    @fuelPrice : gas price in specific state
    @mpg: fuel car's mpg
    @return : total fuel cost in dollars
    '''
    totalGallon = miles/mpg
    return fuelPrice * totalGallon  #fuelPrice should be in dollars/gallon

# Environment Cost:
#     the average price to reduce 1 ton of CO2 is 50$
#     Accoring to mpg we know miles/gallon; 8.89kg CO2 is generated per gallon; So we know that how much is it to reduce CO2.
#     For EV cars, we get data of how much CO2 is generated per mwh(Electricity unit) in each states. So we can know how much is it to reduce co2 for ev

def env_fuel_car(miles,mpg,mPerGallon=8.89,priceToReduce=50) :
    '''
    Compute the total environment cost for a fuel car
    @miles : total miles for a certain type of user
    @mpg : fuel car's mpg
    @return : environment cost for a fuel car
    '''
    # a typical cost is around 3000 dollars for medium user

    totalGallon = miles/mpg
    totalCO2 = totalGallon * 8.89 /1000  #in tons
    totalCost = totalCO2 * priceToReduce
    return totalCost

def env_ev_car(miles, mpge, co2_per_mwh,priceToReduce=50):
    '''
    Compute the total environment cost for a ev car
    @miles : total miles for a certain type of user
    @mpge: ev car's mpge
    @co2_per_mwh : how much CO2 is generated per mwh
    '''
    totalEle = miles * 33.7 / mpge /1000 #in mwh
    totalCO2 = totalEle * co2_per_mwh
    totalCost = totalCO2 * priceToReduce
    return totalCost
