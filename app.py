import os
import pandas as pd
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
  # Lee tu archivo de Excel respetando el nombre exacto con espacios y mayúsculas
  df = pd.read_excel("INVENTARIO LA 48.xlsx")
  
  # Convierte el DataFrame de pandas a una tabla HTML bonita con Bootstrap
  tabla_html = df.to_html(classes="table table-striped table-bordered", index=False)

  # Plantilla web limpia y profesional
  template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Inventario La 48</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light p-4">
        <div class="container">
            <h2 class="mb-4 text-center text-dark font-weight-bold">Inventario La 48</h2>
            <div class="card shadow p-3 bg-white rounded">
                <div class="table-responsive">
                    {{ tabla_html | safe }}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
  return render_template_string(template, tabla_html=tabla_html)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
