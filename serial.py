#port serie
import serial
import serial.tools.list_ports
import time

class SerialPort:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def open(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Opened serial port {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"Closed serial port {self.port}.")

    def write(self, data):
        if self.ser and self.ser.is_open:
            self.ser.write(data.encode())
            print(f"Wrote to serial port: {data}")
        else:
            print("Serial port is not open.")

    def read(self, size=1):
        if self.ser and self.ser.is_open:
            data = self.ser.read(size).decode()
            print(f"Read from serial port: {data}")
            return data
        else:
            print("Serial port is not open.")
            return None

    def readline(self):
        if self.ser and self.ser.is_open:
            data = self.ser.readline().decode().strip()
            print(f"Read line from serial port: {data}")
            return data
        else:
            print("Serial port is not open.")
            return None

def list_available_ports():
    """
    Détecte et retourne la liste de tous les ports série disponibles.
    
    Returns:
        list: Liste des ports série disponibles avec leurs informations
    """
    ports = serial.tools.list_ports.comports()
    available_ports = []
    
    for port in ports:
        port_info = {
            'device': port.device,          # Ex: 'COM3' ou '/dev/ttyUSB0'
            'name': port.name,              # Nom court
            'description': port.description, # Description complète
            'hwid': port.hwid               # Hardware ID
        }
        available_ports.append(port_info)
    
    return available_ports

def print_available_ports():
    """
    Affiche tous les ports série disponibles de manière formatée.
    """
    ports = list_available_ports()
    
    if not ports:
        print("Aucun port série disponible.")
        return
    
    print(f"Ports série disponibles ({len(ports)}):")
    for i, port in enumerate(ports, 1):
        print(f"  {i}. {port['device']}")
        print(f"     Description: {port['description']}")
        print(f"     HWID: {port['hwid']}")
        print()

# Test de la fonction
if __name__ == "__main__":
    print_available_ports()