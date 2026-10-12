import contextlib
import io
import unittest

from utilities import hex_to_binary, binary_to_hex
from key_generator import key_generation, ke_des_generation
from des import des_process, k_des_process, expansion_kd
from function_F import function_F


def bits_to_hex(bits):
    return "".join(binary_to_hex(bits))


class DESKEDESTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plaintext = "0123456789ABCDEF"
        cls.key = "133457799BBCDFF1"
        cls.plaintext2 = "A1B2C3D4E5F60718"
        cls.key2 = "0F1E2D3C4B5A6978"

        cls.bits = hex_to_binary(cls.plaintext)
        cls.key_bits = hex_to_binary(cls.key)
        cls.bits2 = hex_to_binary(cls.plaintext2)
        cls.key_bits2 = hex_to_binary(cls.key2)
        # expansion_kd expects a bit list, while hex_to_binary returns a string.
        cls.left_bits = list(cls.bits[:32])

        with contextlib.redirect_stdout(io.StringIO()):
            cls.keys = key_generation(cls.key_bits)
            cls.ke_keys, cls.pc1_kd, cls.pc2_kd = ke_des_generation(cls.key_bits)
            cls.cipher_bits = des_process(cls.bits, cls.keys)
            cls.ke_cipher_bits = k_des_process(
                cls.bits, cls.ke_keys, cls.pc1_kd, cls.pc2_kd
            )

    # 1. DES known-vector test
    def test_des_known_vector(self):
        self.assertEqual(bits_to_hex(self.cipher_bits), "85E813540F0AB405")

    # 2. DES roundtrip
    def test_des_roundtrip(self):
        with contextlib.redirect_stdout(io.StringIO()):
            recovered = des_process(self.cipher_bits, list(reversed(self.keys)))
        self.assertEqual(bits_to_hex(recovered), self.plaintext)

    # 3. KE-DES published subkeys
    def test_ke_des_k1(self):
        self.assertEqual(
            "".join(self.ke_keys[0]),
            "011011101010110000011010010000110001100110111101",
        )

    def test_ke_des_k2(self):
        self.assertEqual(
            "".join(self.ke_keys[1]),
            "100100010101001111100101101111001110011001000010",
        )

    # 4. KE-DES roundtrip
    def test_ke_des_roundtrip(self):
        with contextlib.redirect_stdout(io.StringIO()):
            recovered = k_des_process(
                self.ke_cipher_bits,
                list(reversed(self.ke_keys)),
                self.pc1_kd,
                list(reversed(self.pc2_kd)),
            )
        self.assertEqual(bits_to_hex(recovered), self.plaintext)

    # 5. Structural tests
    def test_des_generates_16_keys(self):
        self.assertEqual(len(self.keys), 16)

    def test_des_round_keys_are_48_bits(self):
        self.assertTrue(all(len(key) == 48 for key in self.keys))

    def test_pc1_kd_selection_is_8_bits(self):
        self.assertEqual(len(self.pc1_kd), 8)

    def test_ke_des_has_16_pc2_selections(self):
        self.assertEqual(len(self.pc2_kd), 16)

    def test_pc2_kd_selections_are_8_bits(self):
        self.assertTrue(all(len(sel) == 8 for sel in self.pc2_kd))

    def test_kd_expansion_is_48_bits(self):
        expanded = expansion_kd(self.left_bits, self.pc1_kd, self.pc2_kd[0])
        self.assertEqual(len(expanded), 48)

    def test_function_f_output_is_32_bits(self):
        expanded = expansion_kd(self.left_bits, self.pc1_kd, self.pc2_kd[0])
        with contextlib.redirect_stdout(io.StringIO()):
            output = function_F(expanded, self.keys[0])
        self.assertEqual(len(output), 32)

    # 6. Second arbitrary vector roundtrips
    def test_des_second_roundtrip(self):
        with contextlib.redirect_stdout(io.StringIO()):
            keys = key_generation(self.key_bits2)
            cipher = des_process(self.bits2, keys)
            recovered = des_process(cipher, list(reversed(keys)))
        self.assertEqual(bits_to_hex(recovered), self.plaintext2)

    def test_ke_des_second_roundtrip(self):
        with contextlib.redirect_stdout(io.StringIO()):
            keys, pc1, pc2 = ke_des_generation(self.key_bits2)
            cipher = k_des_process(self.bits2, keys, pc1, pc2)
            recovered = k_des_process(
                cipher, list(reversed(keys)), pc1, list(reversed(pc2))
            )
        self.assertEqual(bits_to_hex(recovered), self.plaintext2)


if __name__ == "__main__":
    unittest.main()
