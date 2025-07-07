from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from fastapi import status
from decimal import Decimal
from app.models.models import Product, User
from app.models.models import Order, OrderItem, OrderStatus
from app.schemas.order import OrderOut, OrderItemOut, OrderCreateWithItems, OrderUpdate

async def get_order_by_id(order_id: int, db: Session) -> OrderOut:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return OrderOut.model_validate(order)

async def get_all_orders(db: Session) -> list[OrderOut]:
    orders = db.query(Order).all()
    return [OrderOut.model_validate(order) for order in orders]

async def get_orders_by_status(status: OrderStatus, db: Session) -> list[OrderOut]:
    orders = db.query(Order).filter(Order.status == status).all()
    return [OrderOut.model_validate(order) for order in orders]

async def get_orders_by_user(user_id: int, db: Session) -> list[OrderOut]:
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return [OrderOut.model_validate(order) for order in orders]

async def create_order(order_data: OrderCreateWithItems, db: Session) -> OrderOut:
    # 0. Validar la existencia del usuario
    user = db.query(User).filter(User.id == order_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {order_data.user_id} not found."
        )

    new_order_items = []
    total_amount = Decimal('0.00')

    # 1. Verificar y procesar cada ítem del carrito
    for item_data in order_data.items:
        # 1.1. Verificar existencia del producto
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item_data.product_id} not found or not active."
            )

        if item_data.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Quantity for product ID {item_data.product_id} must be positive."
            )

        #1.2. Calcular subtotal e IVA por ítem 
        item_subtotal = item_data.quantity * product.price
        item_iva_amount = item_subtotal * product.iva

        # 1.3. Crear instancia de OrderItem y acumular al total
        order_item = OrderItem(
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            price_at_time_of_order=product.price,
            iva_at_time_of_order=product.iva
        )
        new_order_items.append(order_item)
        total_amount += item_subtotal + item_iva_amount

    # 2. Crear la instancia de Order principal
    new_order = Order(
        user_id=order_data.user_id,
        total_amount=total_amount,
        status=OrderStatus.PENDING
    )

    # 3. Asociar OrderItems a la Order y agregarlos a la sesión
    new_order.order_items = new_order_items
    db.add(new_order)
    db.flush()

    # 4. Guardar la orden y sus ítems en la base de datos (con manejo de errores)
    try:
        db.commit()
        db.refresh(new_order)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing order due to data inconsistency: {e.orig.args[1] if e.orig else e}."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error creating order: {e}")

    # 5. Retornar la orden creada
    return OrderOut.model_validate(new_order)

async def update_order(order_id: int, order_data: OrderUpdate, db: Session) -> OrderOut:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    for key, value in order_data.model_dump(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return OrderOut.model_validate(order)

async def get_order_item_by_id(order_item_id: int, db: Session) -> OrderItemOut:
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    if not order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
    return OrderItemOut.model_validate(order_item)

async def get_order_items_by_order(order_id: int, db: Session) -> list[OrderItemOut]:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    return [OrderItemOut.model_validate(item) for item in order_items]
