from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
h=125
p0=0
pelozo=0
while True:
    t= sense.get_temperature()
    p=sense.get_pressure()
    h=sense.get_humidity()
    
    t=round(t,1)
    p=round(p,1)
    h=round(h,1)
    p0=p*((1-((0.0065*h)/(t+0.0065*h+273.15)))**-5.257)
    if	p0<pelozo and 985<=p0<=1050 :
        z=127-(0.12*p0)
        match int(z):
                case 1: forecast = "Settled Fine"
                case 2: forecast = "Fine Weather"
                case 3: forecast = "Fine, Becoming Less Settled"
                case 4: forecast = "Fairly Fine, Showery Later"
                case 5: forecast = "Showery, Becoming More Unsettled"
                case 6: forecast = "Unsettled, Rain Later"
                case 7: forecast = "Rain at Times, Worse Later"
                case 8: forecast = "Rain at Times, Becoming Very Unsettled"
                case 9: forecast = "Very Unsettled, Rain"
                case _: forecast = "No forecast available"
            
                
    elif p0==pelozo and 960<=p0<=1033:
        z=144-(0.13*p0)
        match int(z):
                case 10: forecast = "Settled Fine"
                case 11: forecast = "Fine Weather"
                case 12: forecast = "Fine, Possibly Showers"
                case 13: forecast = "Fairly Fine, Showers Likely"
                case 14: forecast = "Showery, Bright Intervals"
                case 15: forecast = "Changeable, Some Rain"
                case 16: forecast = "Unsettled, Rain at Times"
                case 17: forecast = "Rain at Frequent Intervals"
                case 18: forecast = "Very Unsettled, Rain"
                case _: forecast = "No forecast available"
    elif p0>pelozo and 947<=p0<=1030:
        z=185-(0.16*p0)
        match int(z):
                case 20: forecast = "Settled Fine"
                case 21: forecast = "Fine Weather"
                case 22: forecast = "Becoming Fine"
                case 23: forecast = "Fairly Fine, Improving"
                case 24: forecast = "Fairly Fine, Possibly Showers Early"
                case 25: forecast = "Showery Early, Improving"
                case 26: forecast = "Changeable, Mending"
                case 27: forecast = "Rather Unsettled, Clearing Later"
                case 28: forecast = "Unsettled, Probably Improving"
                case 29: forecast = "Unsettled, Short Fine Intervals"
                case 30: forecast = "Very Unsettled, Finer at Times"
                case 31: forecast = "Stormy, Possibly Improving"
                case 32: forecast = "Stormy, Much Rain"
                case _: forecast = "No forecast available"
    pelozo=p0
    message="Temperature: "+ str(t) + "C " + "Pressure: "+ str(p) + "hPa " + "Humidity: " + str(h)+"% " + "Forecast: " + forecast
    print(message)
    sleep(1)