/*
Copyright 2022 @Yowkees
Copyright 2022 MURAOKA Taro (aka KoRoN, @kaoriya)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include QMK_KEYBOARD_H

#include "quantum.h"

// clang-format off
const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
  // keymap for default
  [0] = LAYOUT_universal(
    KC_Q     , KC_W     , KC_E     , KC_R     , KC_T     ,                            KC_Y     , KC_U     , KC_I     , KC_O     , KC_P     ,
    LALT_T(KC_A), LCTL_T(KC_S), LGUI_T(KC_D), LSFT_T(KC_F), KC_G     ,                            KC_H     , RSFT_T(KC_J), RGUI_T(KC_K), RCTL_T(KC_L), RALT_T(KC_MINS),
    KC_Z     , KC_X     , KC_C     , KC_V     , KC_B     ,                            KC_N     , KC_M     , KC_COMM  , KC_DOT   , KC_SLSH  ,
    KC_LNG2  , KC_LGUI  , KC_LALT  ,LSFT_T(KC_LNG2),LT(1,KC_SPC),LT(3,KC_LNG1),KC_BSPC,LT(2,KC_ENT),LSFT_T(KC_LNG2),KC_RALT,KC_RGUI, KC_LNG1
  ),
  // keymap for Nav layer (Miryoku NAV style)
  [1] = LAYOUT_universal(
    XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,                            G(KC_A)  , G(KC_V)  , G(KC_C)  , G(KC_X)  , G(KC_Z)  ,
    KC_LALT  , KC_LCTL  , KC_LGUI  , KC_LSFT  , XXXXXXX  ,                            CW_TOGG ,  KC_LEFT  , KC_DOWN  , KC_UP    , KC_RGHT  , 
    XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,                            KC_INS  ,  KC_HOME  , KC_PGDN  , KC_PGUP  , KC_END   ,
    XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,      KC_ENT   , KC_BSPC  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX
  ),
  // keymap for Mouse layer (Miryoku MOUSE style)
  [2] = LAYOUT_universal(
    XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,                            G(KC_A)  , G(KC_V)  , G(KC_C)  , G(KC_X)  , G(KC_Z)  ,
    KC_LALT  , KC_LCTL  , KC_LGUI  , KC_LSFT  , XXXXXXX  ,                            XXXXXXX  , KC_LSFT  , KC_LCTL  , KC_LALT  , KC_LGUI  ,
    XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,                            XXXXXXX  , KC_BTN1  , KC_BTN2  , XXXXXXX  , XXXXXXX  ,
    XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,      XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX
  ),
  // keymap for Fun layer (Miryoku FUN style)
  [3] = LAYOUT_universal(
    XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,                            KC_PSCR  , KC_F7    , KC_F8    , KC_F9  , KC_F12  ,
    KC_LALT  , KC_LCTL  , KC_LGUI  , KC_LSFT  , KC_SCRL  ,                            KC_SCRL   , KC_F4    , KC_F5    , KC_F6  , KC_F11  ,
    XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,                            KC_PAUS   , KC_F1    , KC_F2    , KC_F3  , KC_F10  ,
    XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,      XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX
  ),
  // keymap for Num layer (Miryoku NUM style)
  [4] = LAYOUT_universal(
    KC_LBRC  , KC_7     , KC_8     , KC_9     , KC_RBRC  ,                            XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,
    KC_SCLN  , KC_4     , KC_5     , KC_6     , KC_EQL   ,                            XXXXXXX  , KC_LSFT  , KC_LGUI  , KC_LCTL  , KC_LALT , 
    KC_GRV   , KC_1     , KC_2     , KC_3     , KC_BSLS  ,                            XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,
    XXXXXXX  , XXXXXXX  , XXXXXXX  , KC_DOT   , KC_0     , KC_MINS  ,      XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX
  ),
  // keymap for Sym layer (Miryoku SYM style)
  [5] = LAYOUT_universal(
    KC_LCBR  , KC_AMPR  , KC_ASTR  , KC_LPRN  , KC_RCBR  ,                            XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,
    KC_COLN  , KC_DLR   , KC_PERC  , KC_CIRC  , KC_PLUS  ,                            XXXXXXX  , KC_LSFT  , KC_LGUI  , KC_LCTL  , KC_LALT  ,
    KC_TILD  , KC_EXLM  , KC_AT    , KC_HASH  , KC_PIPE  ,                            XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  ,
    XXXXXXX  , XXXXXXX  , XXXXXXX  , KC_QUOT  , KC_RPRN  , KC_UNDS  ,      XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX  , XXXXXXX
  ),
};
// clang-format on

layer_state_t layer_state_set_user(layer_state_t state) {
    // Auto enable scroll mode when the highest layer is 3
    keyball_set_scroll_mode(get_highest_layer(state) == 3);
    return state;
}

#ifdef OLED_ENABLE

#    include "lib/oledkit/oledkit.h"

void oledkit_render_info_user(void) {
    keyball_oled_render_keyinfo();
    keyball_oled_render_ballinfo();
    keyball_oled_render_layerinfo();
}
#endif
