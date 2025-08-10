from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database.db_helper import db
from keyboards.main_keyboard import get_main_keyboard, get_back_keyboard

# Create router instance
router = Router()

@router.callback_query(F.data == "menu")
async def show_menu_categories(callback: CallbackQuery):
    """Show menu categories"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👟 Кроссовки", callback_data="катигория_кроссовки"),
            InlineKeyboardButton(text="👕 Футболки", callback_data="катигория_футболки")
        ],
        [
            InlineKeyboardButton(text="👖 Свитпэнты", callback_data="катигория_свитпэнты"),
            InlineKeyboardButton(text="🛒 Корзина", callback_data="cart")
        ],
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back")
        ]
    ])
    
    await callback.message.edit_text(
        "🏪 <b>Выберите категорию:</b>",
        reply_markup=keyboard
    )
    await callback.answer()

@router.callback_query(F.data.startswith("катигория_"))
async def show_category_items(callback: CallbackQuery):
    """Show items in selected category"""
    category = callback.data.split("_")[1]
    items = db.get_menu_category(category)
    
    if not items:
        await callback.answer("Эта категория пуста!", show_alert=True)
        return
    
    keyboard_buttons = []
    text = f"🏪 <b>{category.title()}</b>\n\n"
    
    for item in items:

        # with open(f"images/{item['image']}", "rb") as img:
        #     await callback.message.answer_photo(
        #         photo=img,
        #         caption=f"<b>{item['name']}</b> - ${item['price']:.2f}\n<i>{item['description']}</i>",
        #         parse_mode="HTML"
        #     )

        text += f"<b>{item['name']}</b> - ${item['price']:.2f}\n"
        text += f"<i>{item['description']}</i>\n\n"
        
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"➕ Добавить {item['name']}", 
                callback_data=f"add_{item['id']}"
            )
        ])
    
    keyboard_buttons.append([
        InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="menu")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("add_"))
async def add_to_cart(callback: CallbackQuery):
    """Add item to cart"""
    item_id = int(callback.data.split("_")[1])
    item = db.get_item_by_id(item_id)
    
    if not item:
        await callback.answer("Товар не найден!", show_alert=True)
        return
    
    db.add_to_cart(callback.from_user.id, item_id)
    
    await callback.answer(f"✅ {item['name']} добавлено в корзину!", show_alert=True)

@router.callback_query(F.data == "cart")
async def show_cart(callback: CallbackQuery):
    """Show user's cart"""
    cart = db.get_cart(callback.from_user.id)
    
    if not cart["items"]:
        await callback.message.edit_text(
            "🛒 <b>Ваша корзина пуста</b>\n\n"
            "Добавить некоторые пункты из меню!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🏪 Просмотреть меню", callback_data="menu")],
                [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
            ])
        )
        await callback.answer()
        return
    
    text = "🛒 <b>Ваша корзина:</b>\n\n"
    total = 0
    
    for item_id, quantity in cart["items"].items():
        item = db.get_item_by_id(int(item_id))
        if item:
            item_total = item["price"] * quantity
            total += item_total
            text += f"<b>{item['name']}</b>\n"
            text += f"${item['price']:.2f} x {quantity} = ${item_total:.2f}\n\n"
    
    delivery_fee = db.data.get("settings", {}).get("delivery_fee", 2.50)
    text += f"<b>Итого:</b> ${total:.2f}\n"
    text += f"<b>Доставка:</b> ${delivery_fee:.2f}\n"
    text += f"<b>Общий:</b> ${total + delivery_fee:.2f}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Проверить", callback_data="checkout"),
            InlineKeyboardButton(text="🗑️ Очистить корзину", callback_data="clear_cart")
        ],
        [
            InlineKeyboardButton(text="🏪 Добавить больше элементов", callback_data="menu"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back")
        ]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "clear_cart")
async def clear_cart(callback: CallbackQuery):
    """Clear user's cart"""
    db.clear_cart(callback.from_user.id)
    await callback.answer("🗑️ Корзина очищена!", show_alert=True)
    await show_cart(callback)

@router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery):
    """Process checkout"""
    cart = db.get_cart(callback.from_user.id)
    
    if not cart["items"]:
        await callback.answer("Ваша корзина пуста!", show_alert=True)
        return
    
    # Here you would integrate with payment systems
    # For now, we'll just show order confirmation
    
    order_text = "🎉 <b>Заказ подтвержден!</b>\n\n"
    order_text += "📞 Мы позвоним вам в ближайшее время, чтобы подтвердить детали доставки.\n"
    order_text += "⏱️ Расчетное время доставки: 30-45 минут.\n\n"
    order_text += "<b>Сводка заказа:</b>\n"
    
    for item_id, quantity in cart["items"].items():
        item = db.get_item_by_id(int(item_id))
        if item:
            order_text += f"• {item['name']} x{quantity}\n"
    
    delivery_fee = db.data.get("settings", {}).get("delivery_fee", 2.50)
    order_text += f"\n<b>Общий: ${cart['total'] + delivery_fee:.2f}</b>"
    
    # Clear the cart after order
    db.clear_cart(callback.from_user.id)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back")]
    ])
    
    await callback.message.edit_text(order_text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "contact")
async def show_contact(callback: CallbackQuery):
    """Show contact information"""
    contact_text = """
📞 <b>Контактная информация</b>

📱 Телефон: +1 (555) 123-4567
📧 Email: info@styleshop.com
🌐 Website: www.styleshop.com

<b>Подписывайтесь на нас:</b>
📘 Facebook: @styleshop
📷 Instagram: @styleshop
🐦 Twitter: @styleshop
    """
    
    await callback.message.edit_text(
        contact_text,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "location")
async def show_location(callback: CallbackQuery):
    """Show restaurant location"""
    await callback.message.edit_text(
        "📍 <b>Наше местоположение</b>\n\n"
        "123 Главная улица\n"
        "Центр города, Штат 12345\n\n"
        "Мы находимся в самом центре города!",
        reply_markup=get_back_keyboard()
    )
    # Send actual location
    await callback.message.answer_location(
        latitude=40.7128,  # Replace with actual coordinates
        longitude=-74.0060
    )
    await callback.answer()

@router.callback_query(F.data == "hours")
async def show_hours(callback: CallbackQuery):
    """Show opening hours"""
    hours_text = """
⏰ <b>Время работы</b>

<b>Понедельник - Четверг:</b> 11:00 AM - 10:00 PM
<b>Пятница - Суббота:</b> 11:00 AM - 11:00 PM
<b>Воскресенье:</b> 12:00 PM - 9:00 PM

<b>Мазазин закрывается за 30 минут до закрытия.</b>
    """
    
    await callback.message.edit_text(
        hours_text,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    """Go back to main menu"""
    await callback.message.edit_text(
        f"👋 Добро пожаловать, {callback.from_user.full_name}!\n\n"
        f"Что бы вы хотели сделать?",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()