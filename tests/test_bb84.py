import unittest

from src.bb84 import (
    generer_bits,
    generer_bases,
    preparer_etats,
    mesurer,
    sift_key,
    calculer_qber,
    verifier_qber,
    estimer_qber,
    calculer_parite,
    decouper_blocs,
    trouver_blocs_differents,
    localiser_erreur,
    corriger_erreurs,
    cle_vers_texte,
    hacher_cle,
    empreinte_vers_bits,
    amplification_confidentialite
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

    def test_calculer_parite(self):
        self.assertEqual(calculer_parite([1, 0, 1, 0]), 0)
        self.assertEqual(calculer_parite([1, 0, 1, 1]), 1)


    def test_decouper_blocs(self):
        cle = [1, 0, 1, 1, 0, 0, 1, 0]

        blocs = decouper_blocs(cle, 4)

        self.assertEqual(
            blocs,
            [[1, 0, 1, 1], [0, 0, 1, 0]]
        )


    def test_decouper_blocs_conserve_dernier_bloc_incomplet(self):
        cle = [1, 0, 1, 1, 0, 0]

        blocs = decouper_blocs(cle, 4)

        self.assertEqual(
            blocs,
            [[1, 0, 1, 1], [0, 0]]
        )


    def test_trouver_blocs_differents(self):
        cle_alice = [1, 0, 1, 1, 0, 0, 1, 0]
        cle_bob = [1, 0, 0, 1, 0, 0, 1, 0]

        indices = trouver_blocs_differents(
            cle_alice,
            cle_bob,
            4
        )

        self.assertEqual(indices, [0])


    def test_localiser_erreur(self):
        bloc_alice = [1, 0, 1, 1]
        bloc_bob = [1, 0, 0, 1]

        position = localiser_erreur(
            bloc_alice,
            bloc_bob
        )

        self.assertEqual(position, 2)


    def test_corriger_erreurs(self):
        cle_alice = [1, 0, 1, 1, 0, 0, 1, 0]
        cle_bob = [1, 0, 0, 1, 0, 1, 1, 0]

        cle_bob_corrigee = corriger_erreurs(
            cle_alice,
            cle_bob,
            4
        )

        self.assertEqual(cle_bob_corrigee, cle_alice)

        # La fonction ne doit pas modifier la clé originale
        self.assertNotEqual(cle_bob, cle_alice)


    def test_corriger_erreur_dans_dernier_bloc_incomplet(self):
        cle_alice = [1, 0, 1, 1, 0, 0]
        cle_bob = [1, 0, 1, 1, 0, 1]

        cle_bob_corrigee = corriger_erreurs(
            cle_alice,
            cle_bob,
            4
        )

        self.assertEqual(cle_bob_corrigee, cle_alice)

    def test_cle_vers_texte(self):
        self.assertEqual(
            cle_vers_texte([1, 0, 1, 1]),
            "1011"
        )


    def test_hacher_cle_est_deterministe(self):
        cle = [1, 0, 1, 1]

        empreinte_1 = hacher_cle(cle)
        empreinte_2 = hacher_cle(cle.copy())

        self.assertEqual(empreinte_1, empreinte_2)

        # SHA-256 en hexadécimal contient 64 caractères
        self.assertEqual(len(empreinte_1), 64)


    def test_empreinte_vers_bits(self):
        bits = empreinte_vers_bits("a3")

        self.assertEqual(
            bits,
            [1, 0, 1, 0, 0, 0, 1, 1]
        )


    def test_amplification_confidentialite(self):
        cle_alice = [1, 0, 1, 1, 0, 1, 0, 0] * 20
        cle_bob = cle_alice.copy()

        cle_finale_alice = amplification_confidentialite(
            cle_alice
        )

        cle_finale_bob = amplification_confidentialite(
            cle_bob
        )

        self.assertEqual(
            cle_finale_alice,
            cle_finale_bob
        )

        # La clé initiale contient 160 bits,
        # donc la clé finale en contient 80
        self.assertEqual(len(cle_finale_alice), 80)

        self.assertTrue(
            all(bit in [0, 1] for bit in cle_finale_alice)
        )


    def test_amplification_limitee_a_256_bits(self):
        cle = [0, 1] * 600

        cle_finale = amplification_confidentialite(cle)

        self.assertEqual(len(cle_finale), 256)

if __name__ == "__main__":
    unittest.main()