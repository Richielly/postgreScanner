import flet as ft
import configparser

import scannerDb
cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_center()
    page.title = "Banco de dados Scanner"
    page.update()
    progressBar = ft.ProgressBar(width=700, color=ft.colors.DEEP_ORANGE)

    def scanner_db(e):
        scan = scannerDb.ScannerDb()
        if not txt_palavra.value:
            txt_database.error_text = "Informe uma palavra."
            page.update()
        else:
            page.update()
            txt_header.value = 'Selects encontrados.'
            list_arquivos.controls.clear()
            for table in scan.count_rows_all_tables():
                if table[1] > 0:
                    if table[0]:
                        if scan.search_table_for_value(table[0], txt_palavra.value):
                            print(scan.search_table_for_value(table[0], txt_palavra.value))
                            list_arquivos.controls.append(ft.Text(f'select : ' + scan.search_table_for_value(table[0], txt_palavra.value),selectable=True,size=16, color=ft.colors.GREEN))
                            list_arquivos.update()
            list_arquivos.controls.append(ft.Text(f'Consulta finalizada.',size=16, color=ft.colors.BLUE_900))
            list_arquivos.update()
    ft.Divider(height=9, thickness=3),
    txt_host = ft.TextField(label="Host", text_size=12, value=cfg['DEFAULT']['Host'], width=100, height=35)
    txt_user = ft.TextField(label="User", text_size=12, value=cfg['DEFAULT']['User'], width=250, height=35)
    txt_password = ft.TextField(label="Password", text_size=12, value=cfg['DEFAULT']['password'], width=130, height=35, password=True, can_reveal_password=True)
    txt_database = ft.TextField(label="Nome do Banco", value=cfg['DEFAULT']['NomeBanco'], text_size=12, height=40)
    txt_port = ft.TextField(label="Porta", text_size=12, value=cfg['DEFAULT']['port'], width=100, height=30)
    txt_palavra = ft.TextField(label="Palavra", text_size=12, value='', width=700, height=50)
    txt_header = ft.Text('Selects possíveis')
    list_arquivos = ft.ListView(expand=1, spacing=2, padding=20, auto_scroll=True, disabled=False,)
    page.add(ft.Row([txt_host, txt_port, txt_user, txt_password]))
    page.add(txt_database)
    page.add(txt_palavra)
    page.add(ft.Row([ft.ElevatedButton("Pesquisar", on_click=scanner_db, icon=ft.icons.SEARCH)]))
    page.add(txt_header)
    page.add(list_arquivos)

if __name__ == "__main__":
    # ft.app(port=5555, target=main, view=ft.WEB_BROWSER)
    ft.app(port=5555, target=main)

#  pyinstaller --name scanner_postgres --onefile --icon=codigo-de-barras.ico --noconsole main.py
# flet pack --name scanner_postgres --icon=codigo-de-barras.ico main.py