from __future__ import annotations

from decimal import Decimal

from django import forms

from ..units import utils


class FractionField(forms.Field):
    def to_python(self, value: str | None) -> Decimal | None:
        """Take decimal or fraction and return a decimal if valid."""
        if not value:
            return None

        if "/" in value:
            try:
                amount = utils.parse_numeric_string(value)
                return utils.soft_round(amount) if amount else None
            except ValueError as e:
                raise forms.ValidationError(self.error_messages["invalid"], code="invalid") from e
        try:
            return utils.soft_round(Decimal(str(value)))
        except ValueError as e:
            raise forms.ValidationError(self.error_messages["invalid"], code="invalid") from e
