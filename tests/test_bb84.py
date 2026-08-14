import unittest

from src.bb84 import (
    generer_bits,
    generer_bases,
    preparer_etats,
    mesurer,
    sift_key,
    calculer_qber,
    verifier_qber,
    estimer_qber
)


class TestBB84(unittest.TestCase):

    def test_generer_bits(self):
        bits = generer_bits(10)

        self.assertEqual(len(bits), 10)

        for bit in bits:
            self.assertIn(bit, [0, 1])


    def test_generer_bases(self):
        bases = generer_bases(10)

        self.assertEqual(len(bases), 10)

        for base in bases:
            self.assertIn(base, ["Z", "X"])


    def test_preparer_etats(self):
        bits = [0, 1, 0, 1]
        bases = ["Z", "Z", "X", "X"]

        etats = preparer_etats(bits, bases)

        self.assertEqual(
            etats,
            ["H", "V", "+", "-"]
        )


    def test_mesurer_meme_base(self):
        etats = ["H", "V", "+", "-"]
        bases_bob = ["Z", "Z", "X", "X"]

        bits_bob = mesurer(etats, bases_bob)

        self.assertEqual(
            bits_bob,
            [0, 1, 0, 1]
        )


    def test_sift_key(self):
        bits = [1, 0, 1, 0]
        bases_alice = ["Z", "X", "Z", "X"]
        bases_bob = ["Z", "Z", "Z", "X"]

        cle = sift_key(
            bits,
            bases_alice,
            bases_bob
        )

        self.assertEqual(
            cle,
            [1, 1, 0]
        )

    # test the entire V1 protocol at once
    def test_bb84_sans_eve(self):
        n = 100

        bits_alice = generer_bits(n)
        bases_alice = generer_bases(n)

        etats = preparer_etats(
            bits_alice,
            bases_alice
        )

        bases_bob = generer_bases(n)

        bits_bob = mesurer(
            etats,
            bases_bob
        )

        cle_alice = sift_key(
            bits_alice,
            bases_alice,
            bases_bob
        )

        cle_bob = sift_key(
            bits_bob,
            bases_alice,
            bases_bob
        )

        self.assertEqual(cle_alice, cle_bob)


    def test_calculer_qber(self):
        cle_alice = [0, 1, 1, 0]
        cle_bob = [0, 0, 1, 1]

        qber = calculer_qber(cle_alice, cle_bob)

        self.assertEqual(qber, 0.5)

    def test_verifier_qber(self):
        self.assertTrue(verifier_qber(0.05))
        self.assertTrue(verifier_qber(0.11))
        self.assertFalse(verifier_qber(0.20))

    def test_estimer_qber_identical_keys(self):
        cle_alice = [0, 1, 0, 1, 1, 0, 1, 0, 1, 0]
        cle_bob = cle_alice.copy()

        qber, alice_restante, bob_restante = estimer_qber(
            cle_alice,
            cle_bob,
            proportion=0.2)

        self.assertEqual(qber, 0)
        self.assertEqual(len(alice_restante), 8)
        self.assertEqual(alice_restante, bob_restante)


if __name__ == "__main__":
    unittest.main()