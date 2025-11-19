import network
import socket
import utime
from all_to_test import move_arm       # For two values with 2 decimal places
from all_to_testa import runall_to_test2  # For 3 decimal places + four identical digits
from all_to_testb import runall_to_test3  # For 1 decimal place + four identical digits

class SocketServer:
    def __init__(self):
        self.received_data = None

    def connect_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        try:
            wlan.active(False)
            wlan.active(True)
            wlan.connect('123', '00000000')  # Replace with actual SSID and password
            print("Connecting to WiFi...")
            for i in range(20):
                print("Waiting for connection: {} seconds".format(i + 1))
                utime.sleep(1)
                if wlan.isconnected():
                    break
            if wlan.isconnected():
                print("WiFi connected, config:", wlan.ifconfig())
            else:
                print("WiFi connection failed")
        except Exception as e:
            print("WiFi error:", e)
        return wlan

    def start_socket_server(self):
        wlan = self.connect_wifi()
        host_ip = wlan.ifconfig()[0]
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.bind((host_ip, 1000))  # Set IP and port
        tcp_server.listen(1)  # Accept one connection at a time
        print("TCP server running, waiting for connection...")

        while True:
            client, addr = tcp_server.accept()
            print("Connection from", addr)
            while True:
                msg = client.recv(128).decode().strip()
                if msg:
                    print("Received message:", msg)
                    self.received_data = msg
                    client.send("Server received the message".encode())
                    self.process_received_data()
                else:
                    print("Client disconnected")
                    break
            client.close()

    def process_received_data(self):
        tokens = self.received_data.split()
        if len(tokens) != 2:
            print("Data format error: please provide exactly two values.")
            return

        try:
            # Get decimal places from first token
            if '.' in tokens[0]:
                fraction = tokens[0].split('.')[1]
                decimal_places = len(fraction)
            else:
                fraction = ""
                decimal_places = 0

            # Check second token for four identical digits
            second_val = tokens[1]
            is_four_identical = (len(second_val) == 4 and second_val[0] == second_val[1] == second_val[2] == second_val[3])

            # Case 1: Two values with 2 decimal places
            if decimal_places == 2:
                val1 = float(tokens[0])
                val2 = float(tokens[1])
                print("Calling move_arm with value1 = {:.2f}, value2 = {:.2f}".format(val1, val2))
                move_arm(val1, val2)

            # Case 2: First value with 3 decimal places and second is four identical digits
            elif decimal_places == 3 and is_four_identical:
                angle = float(tokens[0])
                num = int(tokens[1])
                mapping = {1111: "c", 2222: "t", 3333: "s1", 4444: "s2", 5555: "f"}
                if num in mapping:
                    symbol = mapping[num]
                    print("Calling runall_to_test2 with angle = {:.3f} and symbol = '{}'".format(angle, symbol))
                    runall_to_test2(angle, symbol, run_time=2500)
                else:
                    print("Received number {} does not match mapping.".format(num))

            # Case 3: First value with 1 decimal place and second is four identical digits
            elif decimal_places == 1 and is_four_identical:
                angle = float(tokens[0])
                num = int(tokens[1])
                mapping = {1111: "c", 2222: "t", 3333: "s1", 4444: "s2", 5555: "f"}
                if num in mapping:
                    symbol = mapping[num]
                    print("Calling runall_to_test3 with angle = {:.1f} and symbol = '{}'".format(angle, symbol))
                    runall_to_test3(angle, symbol, run_time=2500)
                else:
                    print("Received number {} does not match mapping.".format(num))

            else:
                print("Invalid data format: check decimal places and second value format.")

        except Exception as e:
            print("Error processing received data:", e)

def main():
    server = SocketServer()
    server.start_socket_server()

if __name__ == '__main__':
    main()



