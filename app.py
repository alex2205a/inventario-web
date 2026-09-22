import os
import openpyxl
from flask import Flask, render_template_string

app = Flask(__name__)


@app.route("/")
def index():
  archivo = "INVENTARIO LA 48.xlsx"
  wb = openpyxl.load_workbook(archivo, data_only=True)
  sheet = wb.active

  # Construimos una tabla HTML que replica exactamente las filas y columnas de tu Excel
  html_rows = []
  for r in range(1, sheet.max_row + 1):
    row_cells = []
    has_content = False
    for c in range(1, sheet.max_column + 1):
      cell = sheet.cell(row=r, column=c)
      val = cell.value

      # Si la celda es un booleano (True/False), lo convertimos en un checkbox visual de Excel
      if isinstance(val, bool):
        checked = "checked" if val else ""
        cell_content = (
            f'<input type="checkbox" {checked} disabled class="form-check-input">'
        )
        has_content = True
      elif val is not None:
        cell_content = str(val)
        has_content = True
      else:
        cell_content = ""
        # Verificamos si tiene color de fondo o bordes en el Excel original

      # Determinamos si es una celda de encabezado o título
      tag = "td"
      if r in [2, 6, 8, 9, 27, 30, 31, 32, 41, 42]:
        if val is not None and str(val).strip() != "":
          tag = "th"

      row_cells.append(f"<{tag}>{cell_content}</{tag}>")

    if has_content:
      html_rows.append(f"<tr>{''.join(row_cells)}</tr>")

  tabla_html = f"<table class='excel-table'>{''.join(html_rows)}</table>"

  template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inventario La 48</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { 
                background-color: #f0f2f5; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                padding: 20px;
            }
            .excel-container { 
                max-width: 100%; 
                margin: auto; 
                background: white; 
                padding: 20px; 
                border-radius: 8px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
                overflow-x: auto;
            }
            h2 { color: #1a1a1a; font-weight: bold; margin-bottom: 20px; text-align: center; }
            
            /* Estilo idéntico a una hoja de Excel */
            .excel-table {
                border-collapse: collapse;
                width: 100%;
                font-size: 13px;
                white-space: nowrap;
            }
            .excel-table td, .excel-table th {
                border: 1px solid #d4d4d4;
                padding: 6px 10px;
                vertical-align: middle;
            }
            .excel-table th {
                background-color: #eaedf0;
                color: #333;
                font-weight: bold;
                text-align: center;
            }
            .excel-table tr:hover {
                background-color: #f8f9fa;
            }
        </style>
    </head>
    <body>
        <div class="excel-container">
            <h2>Inventario La 48</h2>
            <div class="table-responsive">
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
