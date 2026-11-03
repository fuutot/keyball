# Keyball39 personal firmware

自分専用の Keyball39 キーマップ `myKeymap` を設定し、GitHub Actions でビルドするためのリポジトリです。
QMK 本体はビルド時に **0.22.14** を取得します。

## 設定を変更する

通常は次の3ファイルを編集します。

| ファイル | 設定内容 |
| --- | --- |
| [keymap.c](qmk_firmware/keyboards/keyball/keyball39/keymaps/myKeymap/keymap.c) | キー配列、6レイヤー、スクロールモードの切り替え |
| [config.h](qmk_firmware/keyboards/keyball/keyball39/keymaps/myKeymap/config.h) | タップ時の遅延、オートマウスなど |
| [rules.mk](qmk_firmware/keyboards/keyball/keyball39/keymaps/myKeymap/rules.mk) | OLED・VIA・RGBなどの有効／無効 |

現在は OLED・VIA が有効、RGB が無効です。既存の配列・動作をそのまま使用します。
Keyball 固有の設定は [ライブラリの説明](qmk_firmware/keyboards/keyball/lib/keyball/README.md) と
[独自キーコード一覧](qmk_firmware/keyboards/keyball/lib/keyball/keycodes.md) を参照してください。

## GitHub Actions でビルドする

1. 設定の変更をコミットして push するか、プルリクエストを作成します。ファームウェアまたはビルド用ワークフローに変更があれば、自動でビルドします。
2. リポジトリの **Actions → Build Keyball39** から該当する実行を開きます。
3. 成功した実行の **Artifacts → keyball39-myKeymap-firmware** をダウンロードして展開します。
4. `keyball_keyball39_myKeymap.hex` を QMK Toolbox などで左右両方の Pro Micro（ATmega32U4 / Caterina）に書き込みます。各側を USB 接続し、リセットしてブートローダーに入れてから書き込みます。

手動実行は **Actions → Build Keyball39 → Run workflow** で対象ブランチを選択します。
ワークフローを初めて追加するブランチでは、PR の自動ビルドを利用できます。手動実行ボタンはワークフローがデフォルトブランチに入ってから使えます。

### キーマップのカンニングシート

ビルド時に `keymap.c` と `info.json` から全レイヤーの配列図を自動生成します。
同じ実行の **Artifacts → keyball39-myKeymap-cheatsheet** をダウンロードし、展開した `index.html` をブラウザーで開いてください。
タップと長押しの機能を表示し、ブラウザーから印刷もできます。画像として使える `keyball39-myKeymap.svg` も含みます。

配列図は `LAYOUT_universal` の全42位置を表示するため、トラックボール搭載側の物理キーがない位置も含みます。
VIA / Remap で EEPROM に保存した配列は反映されません。

ローカルでは Python 3 のみで生成できます（追加パッケージ不要）。

```sh
python3 scripts/generate_keymap_cheatsheet.py
```

生成先は `tmp/keymap-cheatsheet/` です。生成スクリプトを変更した場合も Actions が実行されます。

VIA / Remap のキーマップが EEPROM に保存されている場合、ファームウェアを書き換えても保存済みの配列が優先されます。
`keymap.c` の変更を反映したい場合は、必要な設定をバックアップしてから EEPROM をリセットしてください。
VIA の定義ファイルは [via.json](qmk_firmware/keyboards/keyball/keyball39/via.json) です。

## ローカルでビルドする場合

QMK CLI と AVR 向けのビルド環境を用意したうえで、このリポジトリのルートで実行します。

```sh
git clone --depth 1 --branch 0.22.14 --recurse-submodules --shallow-submodules \
  https://github.com/qmk/qmk_firmware.git __qmk__
python3 -m pip install -r __qmk__/requirements.txt
qmk setup --home "$PWD/__qmk__" --yes
ln -s "$PWD/qmk_firmware/keyboards/keyball" __qmk__/keyboards/keyball
qmk compile -j 4 -kb keyball/keyball39 -km myKeymap
```

生成先は `__qmk__/keyball_keyball39_myKeymap.hex` です。

## 含まれるもの

Keyball39 のキーボード定義、`myKeymap`、トラックボール用 PMW3360 ドライバー、Keyball / OLED ライブラリとフォント、VIA 定義を含みます。
他機種、サンプルキーマップ、基板設計データ、組立資料、全機種向けビルド・リリース処理は含みません。
削除した資料は Git の履歴と [上流リポジトリ](https://github.com/Yowkees/keyball) で確認できます。

元の Keyball ファームウェアは Yowkees / 白銀ラボおよび各コントリビューターによるものです。
著作権表記と [LICENSE](LICENSE) を保持しています。
