import bchlib

# Création du codec BCH pour corriger 2 erreurs
# t=2 : peut corriger 2 erreurs
# prim_poly=37 : polynôme primitif pour GF(2^5)
# ECC = 10 bits pour corriger 2 erreurs
bch = bchlib.BCH(t=2, prim_poly=37)

def generatecode(motBin):
    # Force le mot d'information sur exactement 8 bits
    motBin = motBin & 0xFF  # Masque pour garder seulement les 8 bits de poids faible
    
    # Convertir le mot de 8 bits en bytes (1 octet)
    data = motBin.to_bytes(1, byteorder='big')
    
    # Calculer le BCH (code correcteur d'erreur)
    ecc = bch.encode(data)
    
    # Convertir ECC en entier
    ecc_int = int.from_bytes(ecc, byteorder='big')
    
    # Affichage du resultat BCH avec mot de 8 bits
    print(f"Mot d'information (8 bits): {format(motBin, '08b')} = 0x{motBin:02X}")
    print(f"BCH-{bch.ecc_bits} calculé (parité): {format(ecc_int, f'0{bch.ecc_bits}b')} = 0x{ecc_int:04X}")
    
    # Transmission du message : [8 bits info | 10 bits BCH] = 18 bits total
    codeGenerated = (motBin << bch.ecc_bits) | ecc_int
    
    # Affichage avec 18 bits (8 info + 10 parité)
    print(f"Message transmis (mot + BCH): 0b{codeGenerated:018b} ({codeGenerated.bit_length()} bits utilisés, 18 bits total)")
    print(f"Structure: [8 bits info][{bch.ecc_bits} bits BCH] - Peut corriger 2 erreurs")

    return codeGenerated

