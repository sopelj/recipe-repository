from decimal import Decimal

from pint import UnitRegistry

unit_registry: UnitRegistry[Decimal] = UnitRegistry(non_int_type=Decimal, auto_reduce_dimensions=True)
unit_registry.formatter.default_format = "P"
