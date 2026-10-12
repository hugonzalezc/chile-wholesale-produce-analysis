# Datos externos: IPC general (INE)

**Fuente:** Instituto Nacional de Estadísticas (INE), Índice de Precios al Consumidor, general, mensual.
**Descarga:** [10-10-2026].
**Periodo:** enero de 2020 a diciembre de 2025 (72 meses).

## Archivos

| Archivo | Contenido |
| --- | --- |
| `ipc_ine_raw.csv` | Armado a mano. Meses hasta diciembre de 2023 en base 2018=100, desde enero de 2024 en base 2023=100. **No usar directamente**: tiene un salto de 24% por el cambio de base |
| `ipc_ine.csv` | Serie empalmada a base 2023=100, generada con `src/ipc.py` |

## Empalme

Los meses hasta diciembre de 2023 se multiplican por el factor de enlace del INE
(FE = diciembre 2023 en base 2023 ÷ diciembre 2023 en base 2018), según el manual metodológico del IPC base 2023.
El valor de diciembre de 2023 en la serie referencial (R = 101,04) no se obtuvo
directamente del INE: se dedujo de siete cifras oficiales publicadas (variaciones
mensuales, acumuladas y a doce meses de enero, febrero, septiembre y diciembre de 2024), cuya intersección es 101,02–101,05. FE = 0,75347. El error es menor a ±0,02%.

Comprobación: inflación de diciembre a diciembre de 2023, 2024 y 2025 de 3,94%, 4,53% y 3,45%
(oficiales: 3,9%, 4,5% y 3,5%).