import os
import openpyxl
from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():
  archivo = "INVENTARIO LA 48.xlsx"
  df = pd.read_excel(archivo, sheet_name=0, header=None)

  # Limpiamos el DataFrame para quitar columnas o filas completamente vacías sobrantes
  df = df.dropna(how="all").dropna(axis=1, how="all")

  # Convertimos el DataFrame a HTML con clases de Bootstrap
  html_table = df.to_html(
      header=False,
      index=False,
      classes=(
          "table table-hover table-bordered align-middle m-0"
          " excel-custom-table"
      ),
      escape=False,
  )

  template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inventario General - La 48</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root {
                --primary-color: #0f172a;
                --accent-color: #10b981;
                --bg-color: #f8fafc;
            }
            body {
                background-color: var(--bg-color);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #334155;
            }
            .navbar-brand-custom {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: white;
                padding: 1.2rem 2rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            .card-dashboard {
                background: white;
                border: none;
                border-radius: 12px;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05);
                overflow: hidden;
            }
            .table-container {
                max-height: 75vh;
                overflow: auto;
            }
            /* Estilo profesional para la tabla de Excel */
            table.excel-custom-table {
                font-size: 0.85rem;
                white-space: nowrap;
            }
            table.excel-custom-table th, table.excel-custom-table td {
                padding: 0.65rem 0.9rem;
                border-color: #e2e8f0 !important;
            }
            /* Destacar filas de cabecera o títulos dentro del excel */
            table.excel-custom-table tr:nth-child(1) td {
                font-weight: 700;
                font-size: 1.1rem;
                color: #0f172a;
                background-color: #f1f5f9;
                text-align: center;
                border-bottom: 2px solid #cbd5e1;
            }
            table.excel-custom-table tr:nth-child(5) td, 
            table.excel-custom-table tr:nth-child(7) td {
                font-weight: 600;
                background-color: #f8fafc;
                color: #475569;
            }
            .badge-secure {
                background-color: rgba(16, 185, 129, 0.1);
                color: #059669;
                font-weight: 600;
                padding: 0.5rem 1rem;
                border-radius: 50rem;
                font-size: 0.75rem;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }
            /* Scrollbar personalizado moderno */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #f1f5f9;
            }
            ::-webkit-scrollbar-thumb {
                background: #cbd5e1;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #94a3b8;
            }
        </style>
    </head>
    <body>

        <!-- Barra Superior Corporativa -->
        <div class="navbar-brand-custom d-flex justify-content-between align-items-center mb-4">
            <div class="d-flex align-items-center gap-3">
                <i class="fa-solid fa-boxes-stacked fa-xl text-success"></i>
                <div>
                    <h4 class="m-0 fw-bold tracking-wide">INVENTARIO LA 48</h4>
                    <small class="text-slate-400" style="color: #94a3b8;">Sistema de Control y Monitoreo Interno</small>
                </div>
            </div>
            <div>
                <span class="badge-secure">
                    <i class="fa-solid fa-shield-halved me-1"></i> Modo Seguro / Solo Lectura
                </span>
            </div>
        </div>

        <!-- Contenedor Principal -->
        <div class="container-fluid px-4">
            <div class="card card-dashboard mb-4">
                <div class="card-body p-0">
                    <div class="table-responsive table-container">
                        {{ html_table | safe }}
                    </div>
                </div>
            </div>
            <footer class="text-center text-muted py-3 small">
                <span>La 48 &copy; 2026 &bull; Todos los derechos reservados</span>
            </footer>
        </div>

    </body>
    </html>
    """
  return render_template_string(template, html_table=html_table)


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
