import mpu6050
import requests
import time
from time import sleep

#mpu사용
mpu6050 = mpu6050.mpu6050(0x68)

SSID = ""
PASSWORD = ""
MOBIUS_HOST = "203.253.128.177"
MOBIUS_PORT = 7579
MOBIUS_PATH = "/Mobius/LOD/MPU"

def upload_to_mobius(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z):
    payload = {
        "m2m:cin": {
            "con": f"{gyro_x}, {gyro_y}, {gyro_z}, {accel_x}, {accel_y}, {accel_z}"
        }
    }
    headers = {
        "Accept": "application/json",
        "X-M2M-RI": "12345",
        "X-M2M-Origin": "SKJZkzO42fL",
        "Content-Type": "application/vnd.onem2m-res+json; ty=4"
    }
    url = f"http://{MOBIUS_HOST}:{MOBIUS_PORT}{MOBIUS_PATH}"
    response = requests.post(url, headers=headers, json=payload)

def read_sensor_data():
    # 가속도 값 읽어오기
    accelerometer_data = mpu6050.get_accel_data()

    # 자이로 값 읽어오기
    gyroscope_data = mpu6050.get_gyro_data()
    return accelerometer_data, gyroscope_data

while True:
    time.sleep(0.007)
    # 센서값 읽어오는 코드
    accelerometer_data, gyroscope_data = read_sensor_data()
    #라이브러리에서 불러온 'x', 'y', 'z'의 값만 저장
    accel_x = accelerometer_data['x']
    accel_y = accelerometer_data['y']
    accel_z = accelerometer_data['z']

    gyro_x = gyroscope_data['x']
    gyro_y = gyroscope_data['y']
    gyro_z = gyroscope_data['z']
    #업로드
    upload_to_mobius(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z)
    #센서값 출력
    print(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z)
