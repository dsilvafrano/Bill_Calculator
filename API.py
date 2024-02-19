##API cal for weather and solar data for the specified location

##Packages
import pandas as pd
import requests
import Inputs
import time
#
# # starting time

def api():
    ##Location details
    start = time.time()
    #Fetch solar data using latitude and longitude (get the latitude and longitude using the pincode data)
    latitude = Inputs.latitude
    longitude = Inputs.longitude
    print('Latitude:', latitude)
    print('Longitude:', longitude)

    #API call for a premium 1kW PV panel having 19 percent efficiency, fixed roof mounted type at tilt angle 12 degrees

    response = requests.get("https://developer.nrel.gov/api/pvwatts/v6.json?api_key"
                            "=t8EOwc4wOkyTPfitOHDGgaPqUsWYVw9B3JxaG6Fu&lat=" + str(latitude) + "&lon=" + str(longitude) +
                            "&system_capacity=1" 
                            "&azimuth=180&tilt=12&array_type=1&module_type=1&losses=11&timeframe=hourly")

    outpts = response.json()['outputs']
    # print(outpts)
    # Hourly AC system output (only when timeframe=hourly) (Wac)
    acpwr = outpts['ac']
    # print(acpwr)

    # Build an hourly time and date stamp for one year (8760)
    # date_time = []
    #
    # def generate_datetimes(date_from_str='01-01-2020', days=365):
    #    date_from = datetime.datetime.strptime(date_from_str, '%d-%m-%Y')
    #    for hour in range(24*days):
    #        yield date_from + datetime.timedelta(hours=hour)
    #
    # for date in generate_datetimes():
    #     date_time.append(date.strftime('%d-%m-%Y %H:%M'))

    # ts = pd.date_range(start='2022-01-01', periods=8760, freq='1h')
    # wk = ts.day_name()

    # print(wk[0:744])


    solarp = pd.DataFrame()
    # solarp['date&time'] = ts
    # solarp['day'] = wk
    # Allocating the hourly generation to column AC
    solarp['AC(kW)'] = acpwr

    # Converting (Wac) to (kWac)
    solarp['AC(kW)'] = solarp['AC(kW)']
    # print(solarp[0:24])
    end = time.time()
    runtime = end - start
    print('The runtime API:',runtime )
    return solarp

# end time

#
# runtime = (end - start)
