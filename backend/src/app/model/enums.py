import enum


# ==========================================
#        ORDER STATUS ENUM DEFINITION            
# ==========================================

class OrderStatus(str, enum.Enum):
    PREPARING = 'Preparing'
    PICKED_UP = 'Picked up'
    IN_TRANSIT = 'In transit'
    ARRIVED = 'Arrived'
    DELIVERED = 'Delivered'
