# backend/src/app/schema/types.py
from __future__ import annotations
from typing import Annotated
from pydantic import BeforeValidator


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


# =========================================
#       EXPORTABLE PYDANTIC TYPES                              
# =========================================
# By exporting these, other schema files can just import the type 
# directly, keeping the schema classes incredibly clean.

# Text Types
CleanText = Annotated[str, BeforeValidator(_clean_text)]
OptionalCleanText = Annotated[str | None, BeforeValidator(_clean_text)]

# Location Types
CleanPostalCode = Annotated[str, BeforeValidator(_clean_postal_code)]
OptionalCleanPostalCode = Annotated[str | None, BeforeValidator(_clean_postal_code)]

# Contact Types
PhoneNumber = Annotated[str, BeforeValidator(_normalize_phone)]
OptionalPhoneNumber = Annotated[str | None, BeforeValidator(_normalize_phone)]