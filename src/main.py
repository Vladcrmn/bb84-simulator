from bb84 import (
    generer_bits,
    generer_bases,
    preparer_etats,
    mesurer,
    sift_key
)

def main():
    n = 10

    # Generate Alice's bit sequence
    bits_alice = generer_bits(n)

    # Generate Alice's bases sequence
    bases_alice = generer_bases(n)

    # Bit <-> state mapping
    etats = preparer_etats(bits_alice,bases_alice)

    # Generate Bob's bases sequence
    bases_bob = generer_bases(n)

    # Bob measures the data sent by Alice
    bits_bob = mesurer(etats,bases_bob)

    # The key shared via sifting
    cle_alice = sift_key(bits_alice, bases_alice, bases_bob)
    cle_bob = sift_key(bits_bob, bases_alice, bases_bob)

    print("Alice's bits : ",bits_alice)
    print("Alice's bases : ",bases_alice)
    print("Alice's states : ",etats)
    print("Bob's bases : ",bases_bob)
    print("Bob's bits : ",bits_bob)
    print("Alice's key : ",cle_alice)
    print("Bob's key : ",cle_bob)
    print("Keys match : ", cle_alice == cle_bob)



if __name__ == "__main__":
    main()