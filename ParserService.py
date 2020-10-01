import socket
import sys
import signal
import time
import json

class Quotation:
    def __init__(self, path):
        self.set_path(path)

    def set_path(self, path):
        self.__path = path

    def load_csv(self, file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            next(file)  # jump first line
            coins = []
            for line in file:
                data = {}
                separator = line.split(",")
                data["id"] = int(separator[0])
                data["value1"] = float(separator[2])
                data["value2"] = float(separator[3])
                data["name"] = separator[1]
                coins.append(data)
            return json.dumps(coins)

class Main:
    SLEEP_TIME = 5
    UDP_IP = "localhost"
    UDP_PORT = 10000

    def __init__(self, name):
        self.set_file_name(name)

    def set_file_name(self, name):
        self.__path = name

    def get_file_name(self):
        return self.__path

    def open_CSV(self):
        with open(self.get_file_name(), 'r', encoding='utf-8') as file:
            return file.read()

    def signal_handler(self, sig, frame):
        print(' -> SIGINT signal')
        exit(0)

    def main(self):

        signal.signal(signal.SIGINT, self.signal_handler)
        quotation = Quotation(self.get_file_name())

        while True:
            try:
                string_json = quotation.load_csv(self.open_CSV())
                print(string_json)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(bytearray(string_json, 'utf-8'), (self.UDP_IP, self.UDP_PORT))
                time.sleep(self.SLEEP_TIME)
            finally:
                sock.close()
                print('Program finished..\n')

# main application
app = Main('Config.txt')
app.main()
