import os
import openpyxl
from flask import Flask, render_template_string

app = Flask(__name__)


@app.route("/")
def index():
  archivo = "INVENTARIO LA 48.xlsx"
  wb = openpyxl.load_workbook(archivo, data_only=True)
  sheet = wb.active

  # Generamos una tabla HTML que mapea cada celda y su contenido exacto
  html_rows = []
  max_row = sheet.max_row
  max_col = sheet.max_column

  for r in range(1, max_row + 1):
    row_cells = []
    has_data = False
    for c in range(1, max_col + 1):
      cell = sheet.cell(row=r, column=c)
      val = cell.value

      if val is not None:
        has_data = True

      # Formato de celda (si es booleano, ponemos casilla; si no, el texto)
      if isinstance(val, bool):
        checked = "checked" if val else ""
        content = f'<input type="checkbox" {checked} disabled style="transform: scale(0.9);">'
      elif val is not None:
        content = str(val)
      else:
        content = ""

      # Estilos básicos heredados de la celda
      style = ""
      if cell.font and cell.font.bold:
        style += "font-weight: bold;"
      if cell.alignment and cell.alignment.horizontal:
        style += f"text-align: {cell.alignment.horizontal};"

      row_cells.append(f"<td style='{style}'>{content}</td>")

    if has_data:
      html_rows.append(f"<tr>{''.join(row_cells)}</tr>")

  tabla_html = f"<table class='excel-native-table'>{''.join(html_rows)}</table>"

  template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inventario La 48</title>
        <style>
            body { 
                background-color: #f5f5f5; 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
            }
            .excel-viewer {
                background: white;
                padding: 15px;
                border-radius: 4px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                max-width: 100%;
                overflow-x: auto;
            }
            table.excel-native-table {
                border-collapse: collapse;
                width: auto;
                font-size: 13px;
                background-color: #ffffff;
            }
            table.excel-native-table td {
                border: 1px solid #d4d4d4;
                padding: 6px 10px;
                white-space: nowrap;
                color: #000;
            }
            table.excel-native-table tr:hover {
                background-color: #f1f3f5;
            }
        </style>
    </head>
    <body>
        <div class="excel-viewer">
            <div style="overflow-x: auto;">
                {{ tabla_html | safe }}
            </div>
        </div>
    </body>
    </html>
    """
  return render_template_string(template, tabla_html=tabla_html)


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
