import requests
import flet as ft
from io import BytesIO
import matplotlib
matplotlib.use("Agg")  # 设置 Matplotlib 后端为非交互式
import matplotlib.pyplot as plt
import base64
import sqlite3
from datetime import datetime

# 数据库初始化
def init_db():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    # 创建天气数据表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_code TEXT,
            area_name TEXT,
            date_time TEXT,
            weather TEXT,
            temperature TEXT,
            precipitation TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 保存天气数据到数据库
def save_weather_to_db(area_code, area_name, weather_data):
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    for series in weather_data[0].get("timeSeries", []):
        for area in series.get("areas", []):
            name = area["area"]["name"]
            weathers = ", ".join(area.get("weathers", []))
            temperatures = ", ".join(area.get("temps", []))
            precipitation = ", ".join(area.get("pops", []))
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                '''INSERT INTO weather_data (area_code, area_name, date_time, weather, temperature, precipitation) 
                VALUES (?, ?, ?, ?, ?, ?)''',
                (area_code, name, date_time, weathers, temperatures, precipitation)
            )
    conn.commit()
    conn.close()

# 从数据库中读取天气数据
def fetch_weather_from_db(area_code):
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT date_time, weather, temperature, precipitation FROM weather_data WHERE area_code = ?''', (area_code,))
    data = cursor.fetchall()
    conn.close()
    return data

# 获取地域列表
def fetch_areas():
    url = "http://www.jma.go.jp/bosai/common/const/area.json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("offices", {})

# 获取天气数据
def fetch_weather(area_code):
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# 创建图表并返回图像数据
def create_chart(weather_data, area_name):
    time_defines = []
    pops = []

    # 提取降水概率数据
    for series in weather_data[0].get("timeSeries", []):
        for area in series.get("areas", []):
            if "pops" in area:
                time_defines = series["timeDefines"]
                pops = area["pops"]
                break

    if not pops or not time_defines:
        return None

    # 绘制图表
    fig, ax = plt.subplots()
    ax.plot(time_defines, pops, marker='o', label="Precipitation Probability")
    ax.set_title(f"Precipitation Probability for {area_name}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Probability (%)")
    ax.set_xticks(time_defines)
    ax.set_xticklabels(time_defines, rotation=45)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    # 保存图像到内存
    img_data = BytesIO()
    plt.savefig(img_data, format="png")
    img_data.seek(0)
    plt.close(fig)  # 关闭图表，释放内存
    return img_data

# Flet 主程序
def main(page: ft.Page):
    page.title = "Weather Forecast Application"
    page.scroll = ft.ScrollMode.AUTO

    # 初始化数据库
    init_db()

    # 初始状态
    areas = fetch_areas()
    dropdown_items = [ft.dropdown.Option(key=code, text=info["name"]) for code, info in areas.items()]
    selected_area = ft.Text(value="Select an area to see the weather", size=18)
    weather_display = ft.Column()
    chart_container = ft.Container()

    # 地域选择下拉菜单
    def on_select_area(e):
        area_code = e.control.value
        area_name = areas[area_code]["name"]
        selected_area.value = f"Weather Data for {area_name}"

        # 获取天气数据
        weather_data = fetch_weather(area_code)

        # 保存到数据库
        save_weather_to_db(area_code, area_name, weather_data)

        # 显示天气信息
        weather_display.controls = []
        for record in fetch_weather_from_db(area_code):
            date_time, weather, temperature, precipitation = record
            weather_display.controls.append(ft.Text(f"Date: {date_time}"))
            weather_display.controls.append(ft.Text(f"Weather: {weather}"))
            weather_display.controls.append(ft.Text(f"Temperature: {temperature}"))
            weather_display.controls.append(ft.Text(f"Precipitation: {precipitation}"))
            weather_display.controls.append(ft.Divider())

        # 创建并显示可视化图表
        chart_img = create_chart(weather_data, area_name)
        if chart_img:
            chart_container.content = ft.Image(src=f"data:image/png;base64,{base64.b64encode(chart_img.getvalue()).decode('utf-8')}")
        else:
            chart_container.content = ft.Text("No data available for visualization.")

        page.update()

    dropdown = ft.Dropdown(options=dropdown_items, on_change=on_select_area)

    # 页面布局
    page.add(
        ft.Text("Weather Forecast App", size=24, weight="bold"),
        ft.Divider(),
        dropdown,
        selected_area,
        weather_display,
        ft.Divider(),
        chart_container
    )

# 运行 Flet 应用
if __name__ == "__main__":
    ft.app(target=main)















