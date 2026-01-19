from codeGenerator import generatecode, decodecode

print("=" * 70)
print("TEST du code BCH avec la bibliothèque galois")
print("=" * 70)

# Test 1: Encoder un message
print("\n--- TEST 1: Encodage ---")
mot = 0xA5  # 10100101 en binaire
message_transmis = generatecode(mot)

# Test 2: Décoder sans erreur
print("\n--- TEST 2: Décodage sans erreur ---")
num_errors, data_decoded = decodecode(message_transmis)
assert data_decoded == mot, f"Erreur: {data_decoded:02X} != {mot:02X}"

# Test 3: Introduire 1 erreur
print("\n--- TEST 3: Décodage avec 1 erreur (bit 5) ---")
message_1_erreur = message_transmis ^ (1 << 5)
num_errors, data_decoded = decodecode(message_1_erreur)
if num_errors >= 0:
    print(f"Comparaison: reçu={data_decoded:02X}, attendu={mot:02X}, match={data_decoded == mot}")

# Test 4: Introduire 2 erreurs
print("\n--- TEST 4: Décodage avec 2 erreurs (bits 3 et 12) ---")
message_2_erreurs = message_transmis ^ (1 << 3) ^ (1 << 12)
num_errors, data_decoded = decodecode(message_2_erreurs)
if num_errors >= 0:
    print(f"Comparaison: reçu={data_decoded:02X}, attendu={mot:02X}, match={data_decoded == mot}")

# Test 5: Tester tous les bits
print("\n--- TEST 5: Erreur sur chaque bit individuellement ---")
for bit_pos in range(18):
    message_erreur = message_transmis ^ (1 << bit_pos)
    num_err, _ = decodecode(message_erreur)
    status = "✓ détecté" if num_err > 0 else "✗ NON détecté"
    print(f"Bit {bit_pos:2d}: {status}")

print("\n" + "=" * 70)
print("Tests terminés!")
print("=" * 70)
