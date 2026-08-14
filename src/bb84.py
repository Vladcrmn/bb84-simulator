import random

def generer_bits(n):
    bits = []

    for _ in range(n):
        bits.append(random.randint(0,1))

    return bits


# base Z : states  |H> et |V>
# -> bit 0 = |H>
# -> bit 1 = |V>
# base X : states  |+> et |->
# -> bit 0 = |+>
# -> bit 1 = |->
def generer_bases(n):
    bases = []
    for _ in range(n) : 
        bases.append(random.choice(["Z","X"]))
    return bases

# Correspondance bit <-> état
def preparer_etats(bits, bases):
    etats = []

    for i in range(len(bits)):
        if bases[i] == "Z" and bits[i] == 0 : 
            etats.append("H")
        elif bases[i] == "Z" and bits[i] == 1 : 
            etats.append("V")
        elif bases[i] == "X" and bits[i] == 0 : 
            etats.append("+")
        elif bases[i] == "X" and bits[i] == 1 : 
            etats.append("-")

    return etats

#----------------------------------
# Alice knows now :               |
# Generate the bit sequence       |
# Generate the bases              |
# Prepare the photon states       |
#                                 |
# Now Bob                         |
#----------------------------------



def mesurer(etats, bases_mesure):
    bits_bob = []

    for i in range(len(etats)):

        # Bob measures in the same base as Alice's --> correct result 100%
        if etats[i] in ["H","V"] and bases_mesure[i] == "Z":
            if etats[i] == "H" : 
                bits_bob.append(0)
            else : 
                bits_bob.append(1)
        elif etats[i] in ["+","-"] and bases_mesure[i] == "X":
                    if etats[i] == "+" : 
                        bits_bob.append(0)
                    else : 
                        bits_bob.append(1)

        # Bob measures in a different base than Alice --> random result with probability 1/2
        else : 
            bits_bob.append(random.randint(0,1))

    return bits_bob

# Alice and Bob will only compare their bases, not their bits.
def sift_key(bits, bases_alice, bases_bob):
    cle = []

    for i in range(len(bits)):
        if bases_alice[i] == bases_bob[i] : 
            cle.append(bits[i])

    return cle


# Calculate the Quantum Bit Error Rate between Alice's and Bob's keys
def calculer_qber(cle_alice, cle_bob):

    if len(cle_alice) == 0: 
            return 0
    
    err = 0
    for i in range(len(cle_alice)) :
        if cle_alice[i] != cle_bob[i] : 
            err +=1

    return err/len(cle_alice)

# Alice and Bob reveal publicly only a certain percentage of the key
def estimer_qber(cle_alice, cle_bob, proportion=0.2):
    if len(cle_alice) == 0:
        return 0, [], []

    n_test = max(1, int(len(cle_alice) * proportion)) 

    # Take a random sample of the key
    indices_test = random.sample(range(len(cle_alice)), n_test)
    cle_bob_test = []
    cle_alice_test = []

    for x in indices_test :
        cle_bob_test.append(cle_bob[x])
        cle_alice_test.append(cle_alice[x])

    # Calculate the QBER based on the sample key
    qber = calculer_qber(cle_alice_test,cle_bob_test)

    cle_alice_restante = []

    for i in range(len(cle_alice)):
        if i not in indices_test:
            cle_alice_restante.append(cle_alice[i]) 

    cle_bob_restante = []
    
    for i in range(len(cle_bob)):
            if i not in indices_test:
                cle_bob_restante.append(cle_bob[i])
        

    return qber,cle_alice_restante,cle_bob_restante

# Approximate asymptotic BB84 security threshold
# for ideal conditions with one-way post-processing
def verifier_qber(qber, seuil=0.11):
    return qber <= seuil

# BB84 Protocol
def simuler_bb84(n, eve_active=False, verbose=True): 
    # Generate Alice's bit sequence
    bits_alice = generer_bits(n)

    # Generate Alice's bases sequence
    bases_alice = generer_bases(n)

    # Bit <-> state mapping
    etats = preparer_etats(bits_alice,bases_alice)

    if eve_active : 
        # Eve chooses random measurement bases
        bases_eve = generer_bases(n)

        # Eve intercepts and measures Alice's photons
        bits_eve = mesurer(etats,bases_eve)

        # Eve prepares new photons according to her measurements
        etats_envoye = preparer_etats(bits_eve,bases_eve)
    else : 
        etats_envoye = etats


    # Generate Bob's bases sequence
    bases_bob = generer_bases(n)

    # Bob measures the data sent by Alice
    # In one case : Alice -> Bob
    # Other case : Alice -> Eve -> Bob
    bits_bob = mesurer(etats_envoye,bases_bob)

    # The key shared via sifting
    cle_alice_sifted = sift_key(bits_alice, bases_alice, bases_bob)
    cle_bob_sifted = sift_key(bits_bob, bases_alice, bases_bob)
    qber, cle_alice, cle_bob = estimer_qber(cle_alice_sifted,cle_bob_sifted,proportion=0.2)



    if verbose : 
        print("Alice's bits : ",bits_alice)
        print("Alice's bases : ",bases_alice)
        print("Alice's states : ",etats)
        print("Bob's bases : ",bases_bob)
        print("Bob's bits : ",bits_bob)
        print("Alice sifted key :", cle_alice_sifted)
        print("Bob sifted key   :", cle_bob_sifted)
        print("Alice remaining key :", cle_alice)
        print("Bob remaining key   :", cle_bob)

    print(f"Estimated QBER : {qber * 100:.2f}%")
    
    if verifier_qber(qber):
            print("Continue protocol : QBER acceptable")
    else:
        print("Abort protocol : QBER too high")


    
    



    