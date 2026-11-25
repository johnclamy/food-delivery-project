import enum


# ==========================================
#        ORDER STATUS ENUM DEFINITION            
# ==========================================

class OrderStatus(str, enum.Enum):
    PREPARING = "preparing"
    READY = "ready"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


# =========================================
#  PROPERTY LOCATION LABEL ENUM DEFINITION            
# =========================================

class PropertyLocationLabel(str, enum.Enum):
    HOME = 'Home'
    WORK = 'Work'
    GYM = 'Gym'
