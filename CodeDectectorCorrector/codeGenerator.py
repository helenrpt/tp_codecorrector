import galois
import numpy as np

# Création du code BCH avec la bibliothèque galois
# BCH(n=31, k=21, t=2) peut corriger 2 erreurs
# n = 31 (longueur du mot de code)
# k = 21 (longueur du message)
# Pour notre cas: 8 bits de données -> on aura 10 bits de parité (18 bits total)

# Créer le code BCH (31, 21) qui peut corriger 2 erreurs
bch = galois.BCH(31, 21)

print(f"Code BCH créé: n={bch.n}, k={bch.k}, r={bch.n - bch.k}, t={bch.t}")

def generatecode(motBin):
    """
    Génère un code BCH pour un mot de 8 bits
    
    Args:
        motBin: Entier sur 8 bits (0-255)
    
    Returns:
        Message encodé (données + parité)
    """
    # Force le mot d'information sur exactement 8 bits
    motBin = motBin & 0xFF
    
    # Convertir en array binaire de 8 bits
    # On doit étendre à k bits (21) pour BCH(31,21)
    # On remplit avec des zéros à gauche
    message_bits = []
    for i in range(7, -1, -1):
        message_bits.append((motBin >> i) & 1)
    
    # Padding avec des zéros pour atteindre k=21 bits
    message_padded = [0] * (bch.k - 8) + message_bits
    message_array = galois.GF2(message_padded)

    print(f"message_array (padded to 21 bits): {message_array}")
    # Encoder le message
    codeword = bch.encode(message_array)

    print(f"Mot de code BCH complet (31 bits): {codeword}")

    # Raccourcir le mot de code (supprimer les 13 bits initiaux)
    shortened_codeword = codeword[13:]

    print(f"Mot BCH raccourci (18 bits): {shortened_codeword}")
    
    # Convertir le mot de code en entier
    codeGenerated = 0
    for bit in shortened_codeword:
        codeGenerated = (codeGenerated << 1) | int(bit)
    
    # Affichage
    print(f"Mot d'information (8 bits): {format(motBin, '08b')} = 0x{motBin:02X}")
    print(f"Message transmis (mot + BCH): 0b{codeGenerated:018b} ({codeGenerated.bit_length()} bits utilisés, 18 bits total)")
    print(f"Structure: [8 bits info][10 bits BCH] - Peut corriger 2 erreurs")
    
    return codeGenerated


def decodecode(messageRecu):
    """
    Décode un mot BCH raccourci (18,8) et corrige jusqu'à 2 erreurs
    """

    print(f"\nDécodage du message reçu:")
    print(f"Mot BCH reçu (18 bits): 0b{messageRecu:018b}")

    # Convertir l'entier en tableau de bits (18 bits)
    received_bits = []
    for i in range(17, -1, -1):
        received_bits.append((messageRecu >> i) & 1)

    # Réinsérer les 13 bits raccourcis (zéros)
    full_codeword = [0]*13 + received_bits
    full_codeword = galois.GF2(full_codeword)

    try:
        # Décodage BCH
        decoded_message, num_errors = bch.decode(full_codeword, errors=True)

        # Extraire les 8 bits utiles (ignorer le padding)
        data_corrected = 0
        for i in range(bch.k - 8, bch.k):
            data_corrected = (data_corrected << 1) | int(decoded_message[i])

        print(f"✓ {num_errors} erreur(s) détectée(s) et corrigée(s)")
        print(f"Données corrigées: 0b{data_corrected:08b} = 0x{data_corrected:02X}")

        return num_errors, data_corrected

    except Exception as e:
        print(f"✗ Trop d'erreurs pour être corrigées")
        return -1, None


def induce_errors(codeword, num_errors):
    """
    Induit un nombre spécifique d'erreurs aléatoires dans un mot de code de 18 bits
    
    Args:
        codeword: Entier de 18 bits
        num_errors: Nombre d'erreurs à induire (0-18)
    
    Returns:
        Entier de 18 bits avec erreurs induites
    """
    import random
    
    if num_errors <= 0 or num_errors > 18:
        return codeword
    
    # Générer des positions d'erreurs aléatoires uniques
    error_positions = random.sample(range(18), num_errors)
    
    # Inverser les bits aux positions choisies
    corrupted = codeword
    for pos in error_positions:
        corrupted ^= (1 << pos)
    
    print(f"  Erreurs induites aux positions: {sorted(error_positions, reverse=True)}")
    print(f"  Mot original: 0b{codeword:018b}")
    print(f"  Mot corrompu: 0b{corrupted:018b}")
    
    return corrupted


