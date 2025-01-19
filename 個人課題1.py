import flet as ft
import math

def main(page: ft.Page):
    page.title = "科学計算機"

    # 入力表示ボックス
    txt_display = ft.TextField(
        value="0",  # 初期値は 0
        text_align=ft.TextAlign.RIGHT,  # 右揃え
        read_only=True,  # 読み取り専用に設定
    )

    # ボタンのクリックイベントを処理
    def button_click(e):
        value = e.control.text

        if value == "C":  # クリア機能
            txt_display.value = "0"
        elif value == "⌫":  # 削除キー機能
            if len(txt_display.value) > 1:
                txt_display.value = txt_display.value[:-1]
            else:
                txt_display.value = "0"
        elif value == "=":  # 数式の計算
            try:
                txt_display.value = str(eval(txt_display.value))
            except Exception:
                txt_display.value = "Error"
        else:
            # 現在の値が "0" の場合は置き換え、それ以外は追加
            if txt_display.value == "0":
                txt_display.value = value
            else:
                txt_display.value += value

        page.update()

    # 科学計算ボタンのクリックイベントを処理
    def scientific_button_click(e):
        func = e.control.data
        try:
            value = float(txt_display.value)
            if func == "sin":
                txt_display.value = str(math.sin(math.radians(value)))  # サイン（角度をラジアンに変換）
            elif func == "cos":
                txt_display.value = str(math.cos(math.radians(value)))  # コサイン（角度をラジアンに変換）
            elif func == "sqrt":
                txt_display.value = str(math.sqrt(value))  # 平方根
            elif func == "log":
                txt_display.value = str(math.log(value))  # 自然対数
            elif func == "power":
                txt_display.value = str(value ** 2)  # 2乗
        except Exception:
            txt_display.value = "Error"
        page.update()

    # 通常計算ボタンのレイアウト
    basic_buttons = [
        "7", "8", "9", "/", "C",
        "4", "5", "6", "*", "⌫",
        "1", "2", "3", "-", "(",
        "0", ".", "=", "+", ")"
    ]

    # 科学計算ボタンのレイアウト
    scientific_buttons = [
        {"text": "sin", "func": "sin"},
        {"text": "cos", "func": "cos"},
        {"text": "√", "func": "sqrt"},
        {"text": "log", "func": "log"},
        {"text": "x²", "func": "power"},
    ]

    # 通常計算ボタンを動的に生成
    grid = ft.GridView(expand=True, max_extent=100)
    for btn in basic_buttons:
        grid.controls.append(
            ft.ElevatedButton(
                text=btn,
                on_click=button_click,
            )
        )

    # 科学計算ボタンを動的に生成
    sci_grid = ft.Row(wrap=True)
    for btn in scientific_buttons:
        sci_grid.controls.append(
            ft.ElevatedButton(
                text=btn["text"],
                data=btn["func"],
                on_click=scientific_button_click,
            )
        )

    # ページにコンポーネントを追加
    page.add(
        ft.Column(
            expand=True,
            controls=[
                txt_display,
                grid,
                ft.Text("科学計算機能", size=20, weight=ft.FontWeight.BOLD),  # 科学計算のタイトル
                sci_grid,
            ]
        )
    )

# アプリを起動
ft.app(target=main)
