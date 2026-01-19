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
        self.pushButtonTxMulti.clicked.connect(self.boutonTransmettreMulti)
        
        # Remplir le PortComboBox avec les ports disponibles
        self.PortComboBox.clear()
        if self.ports:
            for port in self.ports:
                self.PortComboBox.addItem(port['device'])
        else:
            self.PortComboBox.addItem("Aucun port disponible")
            self.pushButtonTx.setEnabled(False)

        #Connecte chaque bouton 
                # Connecte chaque bouton b0 à b17 à la méthode handle_bit_button (18 bits total)
        for i in range(18):
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
        
        try:
            # Convertir en hexadécimal (accepte avec ou sans préfixe 0x)
            motInfo8bits = int(motInfoHexa, 16) & 0xFF
            
            if motInfo8bits > 0xFF:
                self.labelTxInfo.setText("Le mot d'information doit être entre 0x00 et 0xFF.")
                return
        except ValueError:
            self.labelTxInfo.setText("Format invalide. Entrez une valeur hexadécimale (ex: FF ou 0xFF).")
            return
      
        self.motCode = cgn.generatecode(motInfo8bits)
#généré (23 bits : 8 info + 10 BCH)
        self.lineMotGene.setText(f"0x{self.motCode:08X}")

        # Afficher chaque bit sur les boutons b0 à b17
        for i in range(18):
            bit_value = (self.motCode >> i) & 1
            bouton = getattr(self, f"b{i}")
            bouton.setText(str(bit_value))
            bouton.setStyleSheet("")
            self.bit_states[i] = False  # Réinitialise l'état
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

        # Met à jour l'affichage des bits (18 bits)
        for i in range(18):
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
            num_errors, data_corrected = cgn.decodecode(int(received))
            self.lineCorrectedHexa.setText(f"0x{data_corrected:02X}")
            self.lineCorrectedBin.setText(f"{data_corrected:08b}")
            self.lineNbrError.setText(str(num_errors))

        else:
            print("Échec de la réception.")

    def boutonTransmettreMulti(self):
        """
        Encode un texte ASCII multi-octets, induit des erreurs aléatoires, 
        transmet sur liaison série et affiche les résultats
        """
        port_name = self.PortComboBox.currentText()
        if port_name == "Aucun port disponible":
            self.textRxMultiBrut.setText("Aucun port disponible pour la transmission.")
            return
        
        # Récupérer le texte à transmettre
        texte = self.textTxMulti.toPlainText()
        if not texte:
            self.textRxMultiBrut.setText("Aucun texte à transmettre.")
            return
        
        # Récupérer le nombre d'erreurs à induire par octet
        num_errors_per_byte = self.nberrorRx.value()
        
        print(f"\n=== Transmission Multi-Octets ===")
        print(f"Texte à transmettre: '{texte}'")
        print(f"Nombre d'octets: {len(texte)}")
        print(f"Erreurs par octet: {num_errors_per_byte}")
        
        # Encoder chaque caractère
        encoded_data = []
        corrupted_data = []
        
        for i, char in enumerate(texte):
            ascii_value = ord(char)
            print(f"\n--- Octet {i+1}: '{char}' (ASCII: 0x{ascii_value:02X}) ---")
            
            # Encoder avec BCH
            codeword = cgn.generatecode(ascii_value)
            encoded_data.append(codeword)
            
            # Induire des erreurs
            corrupted = cgn.induce_errors(codeword, num_errors_per_byte)
            corrupted_data.append(corrupted)
        
        # Préparer le message à transmettre (mots corrompus séparés par des espaces)
        message_to_send = ' '.join(str(word) for word in corrupted_data)
        
        print(f"\n=== Transmission ===")
        print(f"Message envoyé: {message_to_send}")
        
        # Transmettre sur liaison série
        received = sp.transmeit_receive(port_name, message_to_send)
        
        if received is not None:
            print(f"Données reçues: {received}")
            
            # Décoder les données reçues
            try:
                received_words = [int(word) for word in received.split()]
                decoded_text_brut = ""
                decoded_text_corrected = ""
                total_errors = 0
                
                print(f"\n=== Décodage ===")
                for i, word in enumerate(received_words):
                    # Extraire les 8 bits de données sans correction BCH (brut)
                    data_brut = (word >> 10) & 0xFF
                    char_brut = chr(data_brut)
                    decoded_text_brut += char_brut
                    
                    # Décoder avec correction BCH
                    num_errors, data_corrected = cgn.decodecode(word)
                    if data_corrected is not None:
                        decoded_char = chr(data_corrected)
                        decoded_text_corrected += decoded_char
                        total_errors += num_errors
                        print(f"Octet {i+1}: Brut='{char_brut}' -> Corrigé='{decoded_char}' ({num_errors} erreur(s))")
                
                # Afficher les résultats
                self.textRxMultiBrut.setText(decoded_text_brut)
                self.textRxMultiCorrected.setText(decoded_text_corrected)
                self.nbErreurRxMulti.setText(str(total_errors))
                self.nbOctetRxMulti.setText(str(len(received_words)))
                
                print(f"\n=== Résumé ===")
                print(f"Texte brut (avec erreurs): '{decoded_text_brut}'")
                print(f"Texte corrigé: '{decoded_text_corrected}'")
                print(f"Total erreurs corrigées: {total_errors}")
                
            except Exception as e:
                self.textRxMultiCorrected.setText(f"Erreur de décodage: {e}")
                print(f"Erreur lors du décodage: {e}")
        else:
            self.textRxMultiBrut.setText("Échec de la réception.")
            print("Échec de la réception.")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()


