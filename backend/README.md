# Documentación específica del backend

Requisitos mínimos:
- Python 3.10+

Setup rápido (recomendado):

1. Crear y activar un entorno virtual:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Ejecutar la suite de pruebas:

```bash
python -m pytest -q
```

Notas y recomendaciones:
- Si el entorno es administrado por el sistema (error PEP 668), usa el entorno virtual local como se indica arriba.
- El proyecto usa SQLite por defecto; para producción se recomienda Postgres u otra base de datos con mejor concurrencia.
- El workflow de CI está en `.github/workflows/ci.yml` y ejecuta los tests en GitHub Actions.

Soporte y troubleshooting:
- Si falta `email-validator`, instálalo con `python -m pip install email-validator`.
- Para cambiar la versión de Python usada en CI, edita la matriz `python-version` en el archivo del workflow.


