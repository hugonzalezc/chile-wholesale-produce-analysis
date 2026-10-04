import re
import numpy as np

_NUM = r"(\d+(?:,\d+)?)"


def _f(s):
    return float(s.replace(",", "."))


def parsear_unidad(etiqueta):
    """Clasifica una etiqueta de unidad y devuelve (tipo, kilos por unidad de precio).

    tipos: kilo, kilos_envase, unidades, kilo_vol_unidades,
           unidades_vol_unidades, rango, otro
    """
    e = etiqueta.lower().strip()

    if "volumen en unidades" in e:
        if e.startswith("$/kilo"):
            return "kilo_vol_unidades", 1.0
        return "unidades_vol_unidades", np.nan

    if e.startswith("$/kilo") or e.startswith("$/kg"):
        return "kilo", 1.0

    if re.search(_NUM + r"\s*a\s*" + _NUM + r"\s*(kilos?|gramos)", e):
        return "rango", np.nan

    if "gramos" in e:
        return "otro", np.nan

    m = re.search(_NUM + r"\s*(?:kilos?|kgs?\b)", e)
    if m:
        return "kilos_envase", _f(m.group(1))

    if re.search(r"unidad|atado|mata|paquete|cien|docena|trenza|media", e):
        return "unidades", np.nan

    return "otro", np.nan