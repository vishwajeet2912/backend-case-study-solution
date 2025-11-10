#**Logic:**
#- For each product in each warehouse, if quantity < threshold → alert  
#- Include supplier info  
#- Compute `days_until_stockout
 


from flask import request, jsonify
from models import db, Product, Inventory

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    required = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Check SKU uniqueness
    if Product.query.filter_by(sku=data['sku']).first():
        return jsonify({"error": "SKU must be unique"}), 409

    try:
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=float(data['price'])
        )
        db.session.add(product)
        db.session.flush()

        # Prevent duplicate inventory row
        if Inventory.query.filter_by(product_id=product.id, warehouse_id=data['warehouse_id']).first():
            db.session.rollback()
            return jsonify({"error": "Inventory already exists for this product in this warehouse"}), 409

        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data['warehouse_id'],
            quantity=data['initial_quantity']
        )
        db.session.add(inventory)
        db.session.commit()

        return jsonify({"message": "Product created", "product_id": product.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
