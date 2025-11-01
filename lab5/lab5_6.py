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
            case(1):
                print("Settled Fine")
            case(2):
                print("Fine Weather")
            case(3):
                print("Fine, Becoming Less Settled")
            case(4):
                print("Fairly Fine, Showery Later")
            case(5):
                print("Showery, Becoming More Unsettled")
            case(6):
                 print("Unsettled, Rain later")
            case(7):
                 print("Rain at Times, Worse Later")
            case(8):
                 print("Rain at Times, Becoming Very Unsettled")
            case(9):
                 print("Very Unsettled, Rain")
            
                
    elif p0==pelozo and 960<=p0<=1033:
        z=144-(0.13*p0)
    elif p0>pelozo and 947<=p0<=1030:
        z=185-(0.16*p0)
    pelozo=p0
    message="Temperature: "+ str(t) + "C " + "Pressure: "+ str(p) + "hPa " + "Humidity: " + str(h)+"% "
    print(message)
    sleep(1)