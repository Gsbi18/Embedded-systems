from sense_hat import SenseHat
import matplotlib.pyplot as plt
import time

def plot(filename):
    temp_list = []
    humi_list = []
    try:

        file = open(filename, 'r')
        lines = file.readlines()

        for line in lines:
            values = line.split(',')
            temp_list.append(float(values[0]))
            humi_list.append(float(values[1]))
    finally:
        file.close()

    plt.plot(range(1, len(temp_list) + 1), temp_list, 'r-')
    plt.plot(range(1, len(humi_list) + 1), humi_list, 'b--')
    plt.title('Weather')
    plt.xlabel('Measurements')
    plt.ylabel('Value')
    plt.show()

def main():
    sense = SenseHat()
    start_time = time.time()
    stop_time = time.time()
    filename = 'weather.txt'
    file = open(filename, 'a')
    print('Data acquisition is starting…')
    while stop_time - start_time < 5:
        file.write(str(sense.get_temperature()) +',' +str(sense.get_humidity()))
        file.write('\n')
        stop_time = time.time()
    print('Stop data acquisition!')
    file.close()
    plot(filename)


if __name__ == '__main__':
    main()