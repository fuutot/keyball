import json
import unittest
import xml.etree.ElementTree as ET

from generate_keymap_cheatsheet import KEYBOARD, KEYMAP, label, parse_layers, render_svg


class CheatSheetTests(unittest.TestCase):
    def test_current_keymap_has_all_layers_and_positions(self):
        positions = json.loads((KEYBOARD / "info.json").read_text())["layouts"]["LAYOUT_no_ball"]["layout"]
        layers = parse_layers(KEYMAP.read_text(), len(positions))
        self.assertEqual([number for number, _ in layers], list(range(6)))
        self.assertEqual(layers[0][1][33], "LT(1,KC_TAB)")
        self.assertEqual(layers[5][1][0], "KC_LCBR")
        root = ET.fromstring(render_svg(layers, positions))
        groups = root.findall("{http://www.w3.org/2000/svg}g")
        self.assertEqual(len(groups), 6 * 42)
        self.assertEqual(groups[33].find("{http://www.w3.org/2000/svg}title").text, "LT(1,KC_TAB)")

    def test_nested_keycodes_and_comments(self):
        source = "keymaps[][1][2] = { /* ignored */ [0] = LAYOUT_universal(LT(1,KC_TAB), G(S(KC_A))), };"
        self.assertEqual(parse_layers(source, 2), [(0, ["LT(1,KC_TAB)", "G(S(KC_A))"])])

    def test_invalid_layout_fails_instead_of_dropping_keys(self):
        for body in ("[0] = LAYOUT_universal(KC_A)",
                     "[0] = LAYOUT_other(KC_A,KC_B)",
                     "[BASE] = LAYOUT_universal(KC_A,KC_B)",
                     "[0] = LAYOUT_universal(KC_A,KC_B"):
            with self.subTest(body=body), self.assertRaises(ValueError):
                parse_layers("keymaps[][1][2] = {" + body + "};", 2)

    def test_tap_hold_and_symbols(self):
        self.assertEqual(label("LT(2, KC_SPC)"), ("Space", "Hold: Layer 2"))
        self.assertEqual(label("LSFT_T(KC_F)"), ("F", "Hold: L Shift"))
        self.assertEqual(label("G(KC_C)"), ("GUI+C", ""))
        self.assertEqual(label("KC_AMPR"), ("&", ""))
        self.assertEqual(label("CUSTOM_KEY"), ("CUSTOM_KEY", ""))
        svg = render_svg([(0, ["KC_AMPR"])], [{"x": 0, "y": 0}])
        self.assertIn("&amp;", svg)
        ET.fromstring(svg)


if __name__ == "__main__":
    unittest.main()
