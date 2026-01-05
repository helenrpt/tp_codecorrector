from PyQt5 import QtWidgets, uic
import codeGenerator as cgn
import serial_port as sp
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('guideux.ui', self)
        self.show()
        self.motCode = 0
        
        self.bit_states = {}
        self.ports = sp.list_available_ports()

        self.pushButtonGenerer.clicked.connect(self.boutonGenerer)
        self.pushButtonPing.clicked.connect(self.boutonPinger)
        self.pushButtonTx.clicked.connect(self.boutonTransmettre)
        
        # Remplir le PortComboBox avec les ports disponibles
        self.PortComboBox.clear()
        if self.ports:
            for port in self.ports:
                self.PortComboBox.addItem(port['device'])
        else:
            self.PortComboBox.addItem("Aucun port disponible")

        #Connecte chaque bouton 
                # Connecte chaque bouton b0 à b30 à la méthode handle_bit_button (31 bits total)
        for i in range(23):
            bouton = getattr(self, f"b{i}")
            bouton.clicked.connect(lambda checked, idx=i: self.handle_bit_button(idx))
            self.bit_states[i] = False  


    def boutonPinger(self):
        port_name = self.PortComboBox.currentText()
        if port_name == "Aucun port disponible":
            self.labelPingResult.setText("Aucun port disponible pour le ping.")
            return
        
        success = sp.ping_port(port_name)
        if success:
            self.labelPingResult.setText(f"Ping réussi sur le port {port_name}.")
        else:
            self.labelPingResult.setText(f"Échec du ping sur le port {port_name}.")


    def boutonGenerer(self):
        motInfoHexa = self.lineMotInfo.text()
        
        motInfo8bits = int(motInfoHexa, 16) & 0xFF
        
        self.motCode = cgn.generatecode(motInfo8bits)
#généré (23 bits : 8 info + 10 BCH)
        self.lineMotGene.setText(f"0x{self.motCode:08X}")
        
        # Afficher chaque bit sur les boutons b0 à b22
        for i in range(23):
            bit_value = (self.motCode >> i) & 1
            bouton = getattr(self, f"b{i}")
            bouton.setText(str(bit_value))
            bouton.setStyleSheet("")
            self.bit_states[i] = False  # Réinitialise l'étatalue))
            bouton.setStyleSheet("")
            self.bit_states[i] = False 

    def handle_bit_button(self, idx):
        bouton = getattr(self, f"b{idx}")
        if self.bit_states[idx]:
            self.motCode ^= (1 << idx)
            bouton.setStyleSheet("")
            self.bit_states[idx] = False
        else:
            self.motCode ^= (1 << idx)
            bouton.setStyleSheet("background-color: red;")
            self.bit_states[idx] = True

        print(f"Code genere apres inversion du bit {idx}: {bin(self.motCode)}")

        # Met à jour l'affichage des bits (23 bits)
        for i in range(23):
            bit_value = (self.motCode >> i) & 1
            getattr(self, f"b{i}").setText(str(bit_value))

    def boutonTransmettre(self):
        port_name = self.PortComboBox.currentText()
        if port_name == "Aucun port disponible":
            self.labelTransmissionResult.setText("Aucun port disponible pour la transmission.")
            return


        received = sp.transmeit_receive(port_name, str(self.motCode))
        if received is not None:
            print(f"Réception réussie: 0x{int(received):08X}")
            self.lineRxHexa.setText(f"0x{int(received):08X}")
            self.lineRxBin.setText(f"{int(received):023b}")

        else:
            print("Échec de la réception.")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


