import psutil
import subprocess
import re
import sounddevice as sd
import numpy as np

class SensorValue:
    def get_value(self):
        """Get sensor value."""
        raise NotImplementedError("Subclasses must implement get_value method")

class OsxCpuTempSensor(SensorValue):
    def get_value(self):
        try:
            result = subprocess.run(['osx-cpu-temp'], capture_output=True, text=True)
            output = result.stdout.strip()

            temperature_matches = re.findall(r'\d+\.\d+', output)

            if temperature_matches:
                temperature = float(temperature_matches[0])
                return temperature
            else:
                print("Error retrieving temperature.")
                return None
        except Exception as e:
            print(f"Error retrieving temperature: {e}")
            return None

class BatteryLevelSensor(SensorValue):
    def get_value(self):
        try:
            battery = psutil.sensors_battery()
            if battery:
                battery_level = battery.percent
                return battery_level
            else:
                print("Battery information not available.")
                return None
        except Exception as e:
            print(f"Error retrieving battery level: {e}")
            return None

class MicrophoneNoiseSensor(SensorValue):
    def get_value(self):
        try:
            audio_data = sd.rec(int(2 * 44100), samplerate=44100, channels=1, dtype='int16') 
            sd.wait()
            rms = np.sqrt(np.mean(audio_data ** 2))
            rms_rounded = round(rms, 2)
            return rms_rounded
        except Exception as e:
            print(f"Error retrieving microphone noise level: {e}")
            return None

class CpuUsageSensor(SensorValue):
    def get_value(self):
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_usage_with_units = f"{cpu_usage}"
            return cpu_usage_with_units
        except Exception as e:
            print(f"Error retrieving CPU usage: {e}")
            return None

class Sensor:
    def __init__(self, sensor_value):
        self.sensor_value = sensor_value

    def get_value(self):
        return self.sensor_value.get_value()

if __name__ == '__main__':
    osx_cpu_temp_sensor = OsxCpuTempSensor()
    sensor_osx_cpu_temp = Sensor(osx_cpu_temp_sensor)
    result_osx_cpu_temp = sensor_osx_cpu_temp.get_value()
    print(f"OSX CPU Temperature: {result_osx_cpu_temp} °C")

    battery_level_sensor = BatteryLevelSensor()
    sensor_battery_level = Sensor(battery_level_sensor)
    result_battery_level = sensor_battery_level.get_value()
    print(f"Battery Level: {result_battery_level} %")

    cpu_usage_sensor = CpuUsageSensor()
    sensor_cpu_usage = Sensor(cpu_usage_sensor)
    result_cpu_usage = sensor_cpu_usage.get_value()
    print(f"CPU Usage: {result_cpu_usage} %")

    microphone_noise_sensor = MicrophoneNoiseSensor()
    sensor_microphone_noise = Sensor(microphone_noise_sensor)
    result_microphone_noise = sensor_microphone_noise.get_value()
    print(f"Microphone Noise Level: {result_microphone_noise} dB")
