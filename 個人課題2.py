import flet as ft
import requests

def main(page: ft.Page):
    page.title = "都道府県天気予報アプリ"
    page.theme_mode = "light"

    # 気象庁APIエンドポイント
    area_url = "http://www.jma.go.jp/bosai/common/const/area.json"
    forecast_base_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/"

    region_display = ft.ListView(expand=True, spacing=10, padding=10)
    forecast_display = ft.Column(scroll="adaptive", expand=True)

    # 天気予報を取得する関数
    def fetch_forecast(region_code):
        try:
            forecast_url = f"{forecast_base_url}{region_code}.json"
            response = requests.get(forecast_url)
            if response.status_code != 200 or not response.text.strip():
                raise ValueError(f"地域コード {region_code} にデータがありません。")

            forecast_data = response.json()

            # 初始化天气显示
            forecast_display.controls.clear()
            forecast_display.controls.append(ft.Text(f"地域コード {region_code} の天気予報：", weight="bold"))

            # 检查并解析天气数据
            has_weather = False
            for time_series in forecast_data[0].get("timeSeries", []):
                times = time_series.get("timeDefines", [])
                areas = time_series.get("areas", [])

                for area in areas:
                    area_name = area["area"]["name"]
                    area_code = area["area"]["code"]
                    weathers = area.get("weathers", [])
                    
                    # 如果有天气数据，显示
                    if weathers:
                        has_weather = True
                        for time, weather in zip(times, weathers):
                            forecast_display.controls.append(
                                ft.ListTile(
                                    title=ft.Text(f"{area_name} - {time}"),
                                    subtitle=ft.Text(f"天気: {weather}"),
                                )
                            )

            # 如果没有任何天气数据，显示提示信息
            if not has_weather:
                forecast_display.controls.append(
                    ft.Text(f"地域コード {region_code} に有効な天気データがありません。", color="red")
                )
            page.update()
        except Exception as e:
            forecast_display.controls.clear()
            forecast_display.controls.append(ft.Text(f"エラー: {e}", color="red"))
            page.update()

    # 有效区域检查函数
    def validate_region(region_code):
        try:
            forecast_url = f"{forecast_base_url}{region_code}.json"
            response = requests.get(forecast_url)
            if response.status_code == 200 and response.text.strip():
                forecast_data = response.json()
                for time_series in forecast_data[0].get("timeSeries", []):
                    if len(time_series.get("areas", [])) > 0:
                        return True
        except Exception:
            pass
        return False

    # 创建区域列表
    try:
        area_data = requests.get(area_url).json()["class10s"]  # class10s: 都道府县级数据
        for region_code, region_info in area_data.items():
            if validate_region(region_code):  # 只显示有数据的地区
                region_display.controls.append(
                    ft.ListTile(
                        title=ft.Text(region_info["name"]),
                        on_click=lambda e, code=region_code: fetch_forecast(code),
                    )
                )
    except Exception as e:
        region_display.controls.append(
            ft.Text(f"地域データ取得に失敗しました: {e}", color="red")
        )

    # 切换视图
    def switch_view(e):
        if e.control.selected_index == 0:
            region_display.visible = True
            forecast_display.visible = False
        else:
            region_display.visible = False
            forecast_display.visible = True
        page.update()

    nav = ft.NavigationRail(
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.LIST, label="地域リスト"),
            ft.NavigationRailDestination(icon=ft.icons.WB_SUNNY, label="天気予報"),
        ],
        selected_index=0,
        on_change=switch_view,
    )

    page.add(
        ft.Row(
            [
                nav,
                ft.VerticalDivider(width=1),
                ft.Column([region_display, forecast_display], expand=True),
            ],
            expand=True,
        )
    )

    region_display.visible = True
    forecast_display.visible = False
    page.update()


if __name__ == "__main__":
    ft.app(target=main)









