from enum import StrEnum


# ==========================================
#        ORDER STATUS ENUM DEFINITION
# ==========================================

class OrderStatus(StrEnum):
    PREPARING = "preparing"
    READY = "ready"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


# =========================================
#  PROPERTY LOCATION LABEL ENUM DEFINITION
# =========================================

class PropertyLocationLabel(StrEnum):
    HOME = "home"
    WORK = "work"
    GYM = "gym"
