import crc
from crc import Configuration

def generatecode(motBin):
    crc_poly = 0x80F  # Represente le polynome CRC-12
    width = 12  # Largeur du CRC

    num_bytes_for_message = (motBin.bit_length() + 7) // 8 if motBin.bit_length() > 0 else 1
    message_bytes_for_crc_calculation = motBin.to_bytes(num_bytes_for_message, byteorder='big')

    # CRC-12 configuration
    config = Configuration(
        width=width,
        polynomial=crc_poly,
        init_value=0x000,
        final_xor_value=0x000
    )

    # Initialize the CRC-12 calculator with the configuration
    crc_calculator = crc.Calculator(config)

    # Calcul du CRC-12
    calculated_crc = crc_calculator.checksum(message_bytes_for_crc_calculation)

    # Affichage du resultat CRC
    print(f"Mot d'information: {bin(motBin)}")
    print(f"CRC-12 calcule: {bin(calculated_crc)}")

    # Transmission du message avec le CRC
    codeGenerated = (motBin << width) | calculated_crc
    print(f"Message transmis (mot + CRC): {bin(codeGenerated)}")

    return codeGenerated

