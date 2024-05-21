import mpu6050
import requests
import time
from time import sleep

# mpu6050 사용
mpu = mpu6050.mpu6050(0x68)

MOBIUS_HOST = "203.253.128.177"
MOBIUS_PORT = 7579
MOBIUS_ACCEL_PATH = "/Mobius/LOD/ACCEL"
MOBIUS_GYRO_PATH = "/Mobius/LOD/GYRO"

def upload_to_mobius(payload, path):
    headers = {
        "Accept": "application/json",
        "X-M2M-RI": "12345",
        "X-M2M-Origin": "SKJZkzO42fL",
        "Content-Type": "application/vnd.onem2m-res+json; ty=4"
    }
    url = f"http://{MOBIUS_HOST}:{MOBIUS_PORT}{path}"
    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code, response.text)

def read_sensor_data():
    # 가속도 값 읽어오기
    accelerometer_data = mpu.get_accel_data()

    # 자이로 값 읽어오기
    gyroscope_data = mpu.get_gyro_data()

    return accelerometer_data, gyroscope_data

while True:
    time.sleep(0.007)

    # 센서값 읽어오는 코드
    accelerometer_data, gyroscope_data = read_sensor_data()

    # Accelerometer값
    accel_payload = {
        "m2m:cin": {
            "con": {
                "accel": {
                    'x': accelerometer_data['x'],
                    'y': accelerometer_data['y'],
                    'z': accelerometer_data['z']
                }
            }
        }
    }

    # Gyro값
    gyro_payload = {
        "m2m:cin": {
            "con": {
                "gyro": {
                    'x': gyroscope_data['x'],
                    'y': gyroscope_data['y'],
                    'z': gyroscope_data['z']
                }
            }
        }
    }

    # Accel값 업로드
    upload_to_mobius(accel_payload, MOBIUS_ACCEL_PATH)

    # Gyro값 업로드
    upload_to_mobius(gyro_payload, MOBIUS_GYRO_PATH)

    # 센서값 출력
    print("Accelerometer:", accelerometer_data)
    print("Gyroscope:", gyroscope_data)
