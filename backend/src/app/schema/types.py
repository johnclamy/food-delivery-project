# backend/src/app/schema/types.py
from __future__ import annotations
from typing import Annotated
from decimal import Decimal
from pydantic import BeforeValidator, Field


# =========================================
#       STANDALONE VALIDATION FUNCTIONS                              
# =========================================

def _clean_text(v: str | None) -> str | None:
    """Strips whitespace and title-cases standard text fields."""
    if v is None:
        return None
    if not isinstance(v, str):
        raise ValueError("Must be a string")
    
    cleaned = v.strip()
    if not cleaned:
        raise ValueError("Cannot be empty or just whitespace")
    
    return cleaned.title()


def _clean_postal_code(v: str | None) -> str | None:
    """Strips spaces and uppercases postal codes."""
    if v is None:
        return None
    if not isinstance(v, str):
        raise ValueError("Postal code must be a string")
    
    cleaned = v.strip().replace(" ", "").upper()
    if len(cleaned) < 3:
        raise ValueError("Postal code is too short")
    
    return cleaned


def _normalize_phone(v: str | None) -> str | None:
    """Strips non-digits (except '+') and validates minimum length."""
    if v is None:
        return None
    if not isinstance(v, str):
        raise ValueError("Phone number must be a string")
    
    cleaned = "".join(ch for ch in v if ch.isdigit() or ch == "+")
    if len(cleaned) < 7:
        raise ValueError("Phone number is too short (minimum 7 digits)")
    
    return cleaned


def _validate_currency(v: str | None) -> str | None:
    """Ensures currency is a valid 3-letter uppercase ISO 4217 code."""
    if v is None:
        return None
    if not isinstance(v, str):
        raise ValueError("Currency must be a string")
    
    cleaned = v.strip().upper()
    if len(cleaned) != 3:
        raise ValueError("Currency must be a 3-letter ISO 4217 code (e.g., GBP, USD)")
    return cleaned


def _validate_reference(v: str | None) -> str | None:
    """Strips whitespace and enforces max length for external reference codes."""
    if v is None:
        return None
    if not isinstance(v, str):
        raise ValueError("Reference must be a string")
    
    cleaned = v.strip()
    if not cleaned:
        return None # Allow empty string to become None
    if len(cleaned) > 64:
        raise ValueError("Reference cannot exceed 64 characters")
    
    return cleaned


# =========================================
#       EXPORTABLE PYDANTIC TYPES                              
# =========================================
# By exporting these, other schema files can just import the type 
# directly, keeping the schema classes incredibly clean.

# Text & Contact

CleanText = Annotated[str, BeforeValidator(_clean_text)]
OptionalCleanText = Annotated[str | None, BeforeValidator(_clean_text)]

PhoneNumber = Annotated[str, BeforeValidator(_normalize_phone)]
OptionalPhoneNumber = Annotated[str | None, BeforeValidator(_normalize_phone)]


# Location

CleanPostalCode = Annotated[str, BeforeValidator(_clean_postal_code)]
OptionalCleanPostalCode = Annotated[str | None, BeforeValidator(_clean_postal_code)]


# Financial & Order Specific

PositiveDecimal = Annotated[Decimal, Field(gt=0)]
CurrencyCode = Annotated[str, BeforeValidator(_validate_currency)]
ReferenceCode = Annotated[str, BeforeValidator(_validate_reference)]
OptionalReferenceCode = Annotated[str | None, BeforeValidator(_validate_reference)]
