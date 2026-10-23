# Paquete de reproducción

El recorrido principal está en [notebooks/README.md](notebooks/README.md). Desde este directorio:

```bash
uv sync --locked --group dev
uv run --no-sync jupyter lab notebooks
```

Para ejecutar los cinco cuadernos en kernels nuevos:

```bash
uv run --no-sync python notebooks/verify_notebooks.py
```

Los notebooks explican las fuentes, llaman a los scripts de análisis y muestran las salidas recién recalculadas. La [guía de reproducción](../REPRODUCIBILIDAD.md) distingue el reanálisis offline de la nueva inferencia y detalla la alternativa por consola.

Los PDF de entrega están en [documentos/](../documentos/). Las fuentes QMD se conservan aquí junto a sus recursos; los comandos de reproducción no las modifican ni las renderizan.
