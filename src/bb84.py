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



def mesurer(etats, bases_bob):
    bits_bob = []

    for i in range(len(etats)):

        # Bob measures in the same base as Alice's --> correct result 100%
        if etats[i] in ["H","V"] and bases_bob[i] == "Z":
            if etats[i] == "H" : 
                bits_bob.append(0)
            else : 
                bits_bob.append(1)
        elif etats[i] in ["+","-"] and bases_bob[i] == "X":
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