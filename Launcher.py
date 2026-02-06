import flet as ft
import json
import subprocess
import os
import sys

# PyInstaller対応：リソースパスの取得
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

CONFIG_FILE = "tools.json"
MANUAL_FILE = "Manual.html"

def main(page: ft.Page):
    page.title = "Tunnel Inspection Tool Launcher"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 1000
    page.window_height = 700
    page.bgcolor = ft.Colors.GREY_100

    # マニュアルを開く関数
    def open_manual(_):
        manual_path = get_resource_path(MANUAL_FILE)
        if os.name == 'nt':
            if os.path.exists(manual_path):
                os.startfile(manual_path)
            else:
                 page.snack_bar = ft.SnackBar(ft.Text(f"エラー: マニュアルが見つかりません\n{manual_path}"), bgcolor=ft.Colors.RED_400)
                 page.snack_bar.open = True
                 page.update()
        else:
            # 他のOS向けのフォールバック（必要なら実装）
            pass

    # ヘッダー
    header = ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text("トンネル点検調書作成支援ツール ランチャー", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Text("Tunnel Inspection Support Tools", size=16, color=ft.Colors.BLUE_GREY_500),
            ], expand=True),
            # マニュアルボタン
            ft.ElevatedButton(
                "使い方マニュアル",
                icon="help_outline",
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREEN_600,
                on_click=open_manual,
                height=50
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(bottom=20)
    )

    # ツール実行関数
    def run_tool(tool_config):
        command = tool_config.get("command")
        name = tool_config.get("name")
        print(f"Trying to launch: {name}") # Debug print
        
        if not command:
            page.snack_bar = ft.SnackBar(ft.Text(f"エラー: {name} のコマンドが設定されていません"), bgcolor=ft.Colors.RED_400)
            page.snack_bar.open = True
            page.update()
            return

        command_path = os.path.abspath(command)
        cwd = os.path.dirname(command_path)
        print(f"Command path: {command_path}")

        if not os.path.exists(command_path):
            page.snack_bar = ft.SnackBar(ft.Text(f"エラー: ファイルが見つかりません\n{command_path}"), bgcolor=ft.Colors.RED_400)
            page.snack_bar.open = True
            page.update()
            return

        try:
            # 環境変数の準備 (現在のPythonがあるフォルダをPATHの先頭に追加)
            current_python_dir = os.path.dirname(sys.executable)
            env = os.environ.copy()
            env["PATH"] = current_python_dir + os.pathsep + env["PATH"]

            if os.name == 'nt':
                # start "タイトル" /D "作業フォルダ" "コマンドパス"
                cmd = f'start "{name}" /D "{cwd}" "{command_path}"'
                print(f"Executing: {cmd}")
                subprocess.run(cmd, shell=True, env=env)
            else:
                print(f"Popen calling: {command_path}")
                subprocess.Popen(command_path, shell=True, cwd=cwd, env=env)
            
            page.snack_bar = ft.SnackBar(ft.Text(f"「{name}」を起動しました"), bgcolor=ft.Colors.GREEN_600)
            page.snack_bar.open = True
            page.update()
            
        except Exception as e:
            print(f"Exception: {e}")
            page.snack_bar = ft.SnackBar(ft.Text(f"起動エラー: {str(e)}"), bgcolor=ft.Colors.RED_400)
            page.snack_bar.open = True
            page.update()

    # ツールカード生成
    def create_tool_card(tool):
        # 最小構成のデザイン（安定版）
        return ft.Container(
            width=300,
            height=180,
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            padding=20,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_200),
            content=ft.Column([
                ft.Text(
                    tool.get("name", "Unknown"), 
                    weight=ft.FontWeight.BOLD,
                    size=16,
                    color=ft.Colors.BLACK,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                
                ft.Text(
                    tool.get("description", ""), 
                    size=12,
                    color=ft.Colors.GREY_600,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS
                ),
                
                ft.Container(
                    content=ft.ElevatedButton(
                        "起動",
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_600,
                        on_click=lambda _: run_tool(tool),
                        width=260
                    ),
                    alignment=ft.Alignment(0, 0)
                )
            ], 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    # 設定読み込みとレイアウト
    tools_layout = ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )

    try:
        config_path = get_resource_path(CONFIG_FILE)
        with open(config_path, "r", encoding="utf-8") as f:
            tools_data = json.load(f)
            
        for tool in tools_data:
            tools_layout.controls.append(create_tool_card(tool))
            
    except FileNotFoundError:
        tools_layout.controls.append(ft.Text(f"設定ファイル ({CONFIG_FILE}) が見つかりませんでした。", color=ft.Colors.RED))
    except json.JSONDecodeError:
        tools_layout.controls.append(ft.Text(f"設定ファイル ({CONFIG_FILE}) の形式が正しくありません。", color=ft.Colors.RED))

    scroll_container = ft.Column(
        controls=[tools_layout],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    page.add(
        header,
        scroll_container
    )

if __name__ == "__main__":
    ft.app(target=main)
