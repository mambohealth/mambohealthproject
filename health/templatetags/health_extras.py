
from django import template
register = template.Library()
from health.normal_ranges import NORMAL_RANGES

@register.filter
def record_out_of_range(record):
    try:
        v = float(record.data)
        min_v = float(record.normal_min) if record.normal_min else None
        max_v = float(record.normal_max) if record.normal_max else None
        if min_v is not None and v < min_v:
            return True
        if max_v is not None and v > max_v:
            return True
        return False
    except Exception:
        return False

@register.filter
def get_unit(key):
    return NORMAL_RANGES.get(key, {}).get("unit", "")

@register.filter
def get_normal_min(key):
    return NORMAL_RANGES.get(key, {}).get("min", "")

@register.filter
def get_normal_max(key):
    return NORMAL_RANGES.get(key, {}).get("max", "")

@register.filter
def is_out_of_range(value, key):
    try:
        v = float(value)
        min_v = NORMAL_RANGES.get(key, {}).get("min")
        max_v = NORMAL_RANGES.get(key, {}).get("max")
        if min_v is not None and v < min_v:
            return True
        if max_v is not None and v > max_v:
            return True
        return False
    except Exception:
        return False
