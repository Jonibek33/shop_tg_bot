import json
import os
from typing import Dict, List, Any
from pathlib import Path

class DatabaseHelper:
    def __init__(self, db_file: str = "database/data.json"):
        self.db_file = db_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict[str, Any]:
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default data structure
        default_data = {
            "menu": {
                "кроссовки": [
                    {"id": 1, "name": "Nike", "price": 30.00, "description": "Натуральная кожа, резиновая подошва", "image": r"C:\Users\Shacsim_systems©\Desktop\кросс_найк.jpg"},
                    {"id": 2, "name": "Puma", "price": 27.00, "description": "Синтетическая кожа, легкая подошва", "image": r"C:\Users\Shacsim_systems©\Desktop\кросс_пума.jpg"},
                    {"id": 3, "name": "Adidas", "price": 35.00, "description": "Текстиль, амортизирующая подошва", "image": r"C:\Users\Shacsim_systems©\Desktop\кросс_адидас.jpg"}
                ],
                "футболки": [
                    {"id": 4, "name": "Nike", "price": 10.00, "description": "Из хлопка, дышащий материал", "image": r"C:\Users\Shacsim_systems©\Desktop\фут_найк.jpg"},
                    {"id": 5, "name": "Puma", "price": 11.00, "description": "Синтетика, легкий и прочный", "image": r"C:\Users\Shacsim_systems©\Desktop\фут_пума.jpg"},
                    {"id": 6, "name": "Adidas", "price": 9.00, "description": "Текстиль, удобный крой", "image": r"C:\Users\Shacsim_systems©\Desktop\фут_адидас.jpg"}
                ],
                "свитпэнты": [
                    {"id": 7, "name": "Nike", "price": 15.00, "description": "Из хлопка, мягкий и теплый", "image": r"C:\Users\Shacsim_systems©\Desktop\штаны_найк.jpg"},
                    {"id": 8, "name": "Puma", "price": 20.00, "description": "Синтетика, стильный дизайн", "image": r"C:\Users\Shacsim_systems©\Desktop\штаны_пума.jpg"},
                    {"id": 9, "name": "Adidas", "price": 30.00, "description": "Текстиль, спортивный стиль", "image": r"C:\Users\Shacsim_systems©\Desktop\штаны_адидас.jpg"}
                ]
            },
            "orders": {},
            "settings": {
                "delivery_fee": 2.50,
                "min_order": 15.00
            }
        }
        
        # Save default data
        self.save_data_dict(default_data)
        return default_data
    
    def save_data(self):
        self.save_data_dict(self.data)
    
    def save_data_dict(self, data: Dict[str, Any]):
        # Create directory if it doesn't exist
        Path(self.db_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_menu_category(self, category: str) -> List[Dict]:
        return self.data.get("menu", {}).get(category, [])
    
    def get_item_by_id(self, item_id: int) -> Dict:
        for category in self.data.get("menu", {}).values():
            for item in category:
                if item["id"] == item_id:
                    return item
        return {}
    
    def add_to_cart(self, user_id: int, item_id: int, quantity: int = 1):
        user_str = str(user_id)
        if user_str not in self.data["orders"]:
            self.data["orders"][user_str] = {"items": {}, "total": 0}
        
        if str(item_id) in self.data["orders"][user_str]["items"]:
            self.data["orders"][user_str]["items"][str(item_id)] += quantity
        else:
            self.data["orders"][user_str]["items"][str(item_id)] = quantity
        
        self.update_cart_total(user_id)
        self.save_data()
    
    def update_cart_total(self, user_id: int):
        user_str = str(user_id)
        total = 0
        if user_str in self.data["orders"]:
            for item_id, quantity in self.data["orders"][user_str]["items"].items():
                item = self.get_item_by_id(int(item_id))
                if item:
                    total += item["price"] * quantity
        
        self.data["orders"][user_str]["total"] = total
    
    def get_cart(self, user_id: int) -> Dict:
        return self.data["orders"].get(str(user_id), {"items": {}, "total": 0})
    
    def clear_cart(self, user_id: int):
        user_str = str(user_id)
        if user_str in self.data["orders"]:
            self.data["orders"][user_str] = {"items": {}, "total": 0}
            self.save_data()

# Global database instance
db = DatabaseHelper()