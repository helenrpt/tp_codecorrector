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
        #self.pushButtonGenerer.setStyleSheet("background-color: red;")

                # Connecte chaque bouton b0 à b19 à la méthode handle_bit_button
        for i in range(20):
            bouton = getattr(self, f"b{i}")
            bouton.clicked.connect(lambda checked, idx=i: self.handle_bit_button(idx))
            self.bit_states[i] = False  # Par défaut, aucun bouton n'est rouge

    def boutonGenerer(self):
        motInfoHexa = self.lineMotInfo.text();
        
        self.motCode = cgn.generatecode(int(motInfoHexa, 20))

        self.lineMotGene.setText(hex(self.motCode))
        
        # Afficher chaque bit sur les boutons b0 à b19
        for i in range(20):
            bit_value = (self.motCode >> i) & 1
            bouton = getattr(self, f"b{i}")
            bouton.setText(str(bit_value))
            bouton.setStyleSheet("")
            self.bit_states[i] = False  # Réinitialise l'état

    def handle_bit_button(self, idx):
        bouton = getattr(self, f"b{idx}")
        if self.bit_states[idx]:
            # Si déjà rouge, on remet par défaut et on réinverse le bit
            self.motCode ^= (1 << idx)
            bouton.setStyleSheet("")
            self.bit_states[idx] = False
        else:
            # Sinon, on inverse le bit et on met en rouge
            self.motCode ^= (1 << idx)
            bouton.setStyleSheet("background-color: red;")
            self.bit_states[idx] = True

        print(f"Code genere apres inversion du bit {idx}: {bin(self.motCode)}")

        # Met à jour l'affichage des bits
        for i in range(20):
            bit_value = (self.motCode >> i) & 1
            getattr(self, f"b{i}").setText(str(bit_value))
        #self.lineMotGene.setText(hex(self.motCode))



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


