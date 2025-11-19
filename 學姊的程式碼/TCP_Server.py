# ESP32 TCP 伺服器程式 (MicroPython)
import network
import socket
import gc
import utime
from machine import Pin
import machine

led = Pin(14, Pin.OUT)  # 控制 LED 燈的 GPIO

# Wi-Fi 設定
SSID = "123"           # 你的 Wi-Fi 名稱
PASSWORD = "00000000"  # 你的 Wi-Fi 密碼
PORT = 2000            # 伺服器監聽的 Port

def go_wifi():
    try:
        wifi.active(False)
        wifi.active(True)
        wifi.connect(SSID, PASSWORD)
        print("Start connecting to Wi-Fi...")
        for i in range(20):
            print("Attempting to connect: {}s".format(i))
            utime.sleep(1)
            if wifi.isconnected():
                break
        if wifi.isconnected():
            print("Wi-Fi connection successful!")
            print("Network Config:", wifi.ifconfig())
        else:
            print("Wi-Fi connection failed!")
    except Exception as e:
        print("Wi-Fi Error:", e)

gc.collect()
wifi = network.WLAN(network.STA_IF)
go_wifi()

if not wifi.isconnected():
    print("Wi-Fi connection failed, restarting...")
    utime.sleep(2)
    machine.reset()

hostip = wifi.ifconfig()[0]
print("ESP32 Server IP Address:", hostip)

# 模擬執行 all_to_test 指令的函式
def exec_all_to_test(dx, dy):
    print(">>> Executing all_to_test with dx = {:.3f}, dy = {:.3f}".format(dx, dy))
    # 模擬動作：例如點亮 LED 表示正在運行
    led.value(1)
    utime.sleep(2)
    led.value(0)
    return "complete"

def exec_all_to_test2(slope, block):
    print(">>> Executing all_to_test2 with slope = {:.2f}, block = {}".format(slope, block))
    utime.sleep(2)
    return "complete"

def exec_all_to_test3(slope, block):
    print(">>> Executing all_to_test3 with slope = {:.2f}, block = {}".format(slope, block))
    utime.sleep(2)
    return "complete"

# 建立 TCP 伺服器
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_server.bind(("0.0.0.0", PORT))
tcp_server.listen(1)
rev_num = 0

print("ESP32 TCP Server is listening on port", PORT)

while True:
    try:
        print("Waiting for incoming connections...")
        tcp_conn, client_addr = tcp_server.accept()
        print("Client connected successfully from:", client_addr)

        while True:
            msg = tcp_conn.recv(128)
            if len(msg) > 0:
                msg = msg.decode().strip()
                print("Received command:", msg)
                response = ""
                # 處理 led= 指令 (保持原有邏輯)
                if msg.startswith("led="):
                    if msg[4] == '1':
                        led.value(1)
                        print("LED turned ON")
                    else:
                        led.value(0)
                        print("LED turned OFF")
                    response = "Message received: led command"
                # 處理 exec_all_to_test 指令
                elif msg.startswith("exec_all_to_test"):
                    # 指令格式例如: "exec_all_to_test dx=12.345 dy=-6.789"
                    try:
                        parts = msg.split()
                        dx = None
                        dy = None
                        for part in parts:
                            if part.startswith("dx="):
                                dx = float(part[3:])
                            elif part.startswith("dy="):
                                dy = float(part[3:])
                        if dx is not None and dy is not None:
                            result = exec_all_to_test(dx, dy)
                            response = result
                        else:
                            response = "Missing dx or dy parameter"
                    except Exception as e:
                        response = "Error parsing exec_all_to_test: " + str(e)

                # 處理 exec_all_to_test2 指令
                elif msg.startswith("exec_all_to_test2"):
                    # 指令格式例如: "exec_all_to_test2 slope=30.0 block=red"
                    try:
                        parts = msg.split()
                        slope = None
                        block = None
                        for part in parts:
                            if part.startswith("slope="):
                                slope = float(part[6:])
                            elif part.startswith("block="):
                                block = part[6:]
                        if slope is not None and block is not None:
                            result = exec_all_to_test2(slope, block)
                            response = result
                        else:
                            response = "Missing slope or block parameter"
                    except Exception as e:
                        response = "Error parsing exec_all_to_test2: " + str(e)
                # 處理 exec_all_to_test3 指令
                elif msg.startswith("exec_all_to_test3"):
                    # 指令格式例如: "exec_all_to_test3 slope=30.0 block=red"
                    try:
                        parts = msg.split()
                        slope = None
                        block = None
                        for part in parts:
                            if part.startswith("slope="):
                                slope = float(part[6:])
                            elif part.startswith("block="):
                                block = part[6:]
                        if slope is not None and block is not None:
                            result = exec_all_to_test3(slope, block)
                            response = result
                        else:
                            response = "Missing slope or block parameter"
                    except Exception as e:
                        response = "Error parsing exec_all_to_test3: " + str(e)
                else:
                    response = "Unrecognized command"
                    print("Unrecognized command:", msg)
                
                rev_num += 1
                tcp_conn.send(response.encode())
            else:
                print("Client socket disconnected")
                break
    except Exception as e:
        print("Error:", e)
    finally:
        tcp_conn.close()


