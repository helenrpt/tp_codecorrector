from PyQt5 import QtWidgets, uic
import codeGenerator as cgn
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('guideux.ui', self)
        self.show()
        self.motCode = 0
        self.pushButtonGenerer.clicked.connect(self.boutonGenerer)
        self.bit_states = {}

        #Connecte chaque bouton 
                # Connecte chaque bouton b0 à b30 à la méthode handle_bit_button (31 bits total)
        for i in range(31):
            bouton = getattr(self, f"b{i}")
            bouton.clicked.connect(lambda checked, idx=i: self.handle_bit_button(idx))
            self.bit_states[i] = False  

    def boutonGenerer(self):
        motInfoHexa = self.lineMotInfo.text()
        
        motInfo8bits = int(motInfoHexa, 16) & 0xFF
        
        self.motCode = cgn.generatecode(motInfo8bits)
#généré (31 bits : 16 info + 15 BCH)
        self.lineMotGene.setText(f"0x{self.motCode:08X}")
        
        # Afficher chaque bit sur les boutons b0 à b30
        for i in range(31):
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

        # Met à jour l'affichage des bits (31 bits)
        for i in range(31):
            bit_value = (self.motCode >> i) & 1
            getattr(self, f"b{i}").setText(str(bit_value))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


