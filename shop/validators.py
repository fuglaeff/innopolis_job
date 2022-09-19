from django.core.exceptions import ValidationError


def discount_and_tax_validator(value):
    if not 0 < value <= 100:
        raise ValidationError(
            'Value of discount/tax must be g then 0 and l then 1'
        )
