from dbtools import Dao
class ProductDao(Dao):
    def update(self, product_id: int, **fields):
        updates = [f"{key} = ?" for key in fields.keys()]
        params = list(fields.values()) + [product_id]
        stmt = f"UPDATE products SET {', '.join(updates)} WHERE id = ?"
        self._conn.execute(stmt, params)
