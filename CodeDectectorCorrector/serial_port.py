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

def ping_port(port, baudrate=9600, timeout=1):
    """
    Tente d'ouvrir un port série et d'envoyer une commande de ping.
    
    Args:
        port (str): Le nom du port série à tester.
        baudrate (int): Le débit en bauds pour la communication série.
        timeout (int): Le délai d'attente en secondes pour la lecture.
    
    Returns:
        bool: True si le ping a réussi, False sinon.
    """
    sp = SerialPort(port, baudrate, timeout)
    sp.open()
    if sp.ser and sp.ser.is_open:
        sp.write("PING\n")
        time.sleep(0.5)  # Attendre une réponse
        response = sp.readline()
        sp.close()
        if response == "PING":
            print(f"Ping réussi sur le port {port}.")
            return True
        else:
            print(f"Aucune réponse ou réponse incorrecte sur le port {port}.")
            return False
    else:
        print(f"Impossible d'ouvrir le port {port}.")
        return False

def transmeit_receive(port, data, baudrate=9600, timeout=1):
    """
    Envoie un message via le port série et attend une réponse.
    
    Args:
        port (str): Le nom du port série à utiliser.
        message (str): Le message à envoyer.
        baudrate (int): Le débit en bauds pour la communication série.
        timeout (int): Le délai d'attente en secondes pour la lecture.
    
    Returns:
        str: La réponse reçue du port série.
    """
    sp = SerialPort(port, baudrate, timeout)
    sp.open()
    response = None
    if sp.ser and sp.ser.is_open:
        sp.write(data + "\n")
        time.sleep(0.5)  # Attendre une réponse
        received = sp.readline()
        sp.close()
    else:
        print(f"Impossible d'ouvrir le port {port}.")
    return received