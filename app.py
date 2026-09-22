import os
import openpyxl
from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():
  archivo = "INVENTARIO LA 48.xlsx"
  wb = openpyxl.load_workbook(archivo, data_only=True)
  sheet = wb.active

  # Convertimos la hoja completa a una estructura de datos para la tabla web
  data = list(sheet.values)

  template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inventario La 48 - Vista Excel</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { 
                background-color: #f3f3f3; 
                font-family: 'Calibri', Arial, sans-serif; 
                margin: 0;
                padding: 10px;
            }
            .excel-window {
                background: white;
                border: 1px solid #ccc;
                box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                border-radius: 4px;
                max-width: 100%;
                margin: auto;
                overflow: hidden;
            }
            .excel-header-bar {
                background-color: #107c41;
                color: white;
                padding: 10px 15px;
                font-size: 16px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .excel-container {
                max-height: 80vh;
                overflow: auto;
                background-color: #fff;
            }
            table.excel-grid {
                border-collapse: collapse;
                width: 100%;
                table-layout: fixed;
            }
            table.excel-grid th, table.excel-grid td {
                border: 1px solid #d4d4d4;
                padding: 5px 8px;
                font-size: 12px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
            /* Fila y columna de índices estilo Excel (A, B, C... 1, 2, 3...) */
            table.excel-grid th {
                background-color: #f2f2f2;
                color: #333;
                text-align: center;
                font-weight: normal;
                position: sticky;
                top: 0;
                z-index: 10;
            }
            table.excel-grid td:first-child, table.excel-grid th:first-child {
                background-color: #f2f2f2;
                width: 40px;
                text-align: center;
                color: #555;
                position: sticky;
                left: 0;
                z-index: 5;
            }
            table.excel-grid tr:hover {
                background-color: #f9fbfd;
            }
        </style>
    </head>
    <body>
        <div class="excel-window">
            <div class="excel-header-bar">
                <span>🟢 INVENTARIO LA 48 (Solo Vista)</span>
                <span style="font-size: 12px; font-weight: normal;">Modo Seguro</span>
            </div>
            <div class="excel-container">
                <table class="excel-grid">
                    <thead>
                        <tr>
                            <th>#</th>
                            {% for col in range(1, data[0]|length + 1) %}
                                <th>{{ col }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for row_idx in range(data|length) %}
                        <tr>
                            <td>{{ row_idx + 1 }}</td>
                            {% for cell in data[row_idx] %}
                            <td>
                                {% if cell is boolean %}
                                    <input type="checkbox" {% if cell %}checked{% endif %} disabled style="transform: scale(0.9);">
                                {% elif cell is not none %}
                                    {{ cell }}
                                {% endif %}
                            </td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
  return render_template_string(template, data=data)


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
