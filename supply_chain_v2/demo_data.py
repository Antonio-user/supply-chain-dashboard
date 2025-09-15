"""Script pour insérer des données de démonstration"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import db

def insert_demo_data():
    """Insère des données de démonstration pour tous les modules"""
    
    print("🚀 Insertion des données de démonstration...")
    
    # Connexion à la base
    if not db.connect():
        print("❌ Impossible de se connecter à la base")
        return False
    
    try:
        # 1. Clients de démonstration
        clients_data = [
            ("TechCorp Solutions", "Marie Dubois", "marie@techcorp.fr", "01.23.45.67.89", "15 Avenue des Champs", "Paris", "France"),
            ("Global Industries", "Pierre Martin", "pierre@global.com", "01.98.76.54.32", "42 Rue de la Paix", "Lyon", "France"),
            ("Innovation Ltd", "Sophie Bernard", "sophie@innovation.uk", "+44.20.1234.5678", "10 Oxford Street", "London", "UK"),
            ("Digital Dynamics", "Alex Johnson", "alex@digital.com", "+1.555.123.4567", "123 Tech Avenue", "San Francisco", "USA"),
            ("Euro Logistics", "Hans Mueller", "hans@euro.de", "+49.30.1234567", "Unter den Linden 1", "Berlin", "Germany")
        ]
        
        for client in clients_data:
            query = """
                INSERT INTO customers (customer_name, contact_person, email, phone, address, city, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(query, client)
        
        print("✅ Clients insérés")
        
        # 2. Entrepôts de démonstration
        warehouses_data = [
            ("Entrepôt Central Paris", "Paris, Île-de-France", 5000.0),
            ("Hub Logistique Lyon", "Lyon, Auvergne-Rhône-Alpes", 3500.0),
            ("Centre de Distribution Marseille", "Marseille, PACA", 2800.0),
            ("Plateforme Nord Lille", "Lille, Hauts-de-France", 4200.0),
            ("Dépôt Régional Bordeaux", "Bordeaux, Nouvelle-Aquitaine", 2200.0)
        ]
        
        for warehouse in warehouses_data:
            query = """
                INSERT INTO warehouses (warehouse_name, location, capacity_m3)
                VALUES (%s, %s, %s)
            """
            db.execute_query(query, warehouse)
        
        print("✅ Entrepôts insérés")
        
        # 3. Fournisseurs de démonstration
        suppliers_data = [
            ("TechSupply International", "Jean-Claude Vannier", "jc@techsupply.fr", "01.44.55.66.77", "Zone Industrielle Nord", "France", True),
            ("Global Components Ltd", "Sarah Wilson", "sarah@globalcomp.com", "+44.161.234.5678", "Manchester Business Park", "UK", True),
            ("Euro Electronics GmbH", "Klaus Weber", "klaus@euroelec.de", "+49.89.1234567", "Münchener Strasse 45", "Germany", True),
            ("Asian Manufacturing Co", "Li Wei", "li@asianmfg.cn", "+86.21.1234.5678", "Shanghai Industrial Zone", "China", True),
            ("American Parts Corp", "Mike Thompson", "mike@amparts.com", "+1.312.555.0123", "Chicago Industrial District", "USA", False)
        ]
        
        for supplier in suppliers_data:
            query = """
                INSERT INTO suppliers (supplier_name, contact_person, email, phone, address, country, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(query, supplier)
        
        print("✅ Fournisseurs insérés")
        
        # 4. Produits de démonstration
        products_data = [
            ("LAPTOP-001", "Ordinateur Portable Pro", "Électronique", 850.00),
            ("MOUSE-002", "Souris Ergonomique", "Électronique", 45.00),
            ("CHAIR-003", "Chaise de Bureau", "Mobilier", 320.00),
            ("DESK-004", "Bureau Ajustable", "Mobilier", 580.00),
            ("PHONE-005", "Téléphone IP", "Électronique", 120.00),
            ("TABLET-006", "Tablette Tactile", "Électronique", 450.00),
            ("PRINTER-007", "Imprimante Laser", "Électronique", 280.00),
            ("CABLE-008", "Câble HDMI 2m", "Électronique", 25.00),
            ("MONITOR-009", "Écran 24 pouces", "Électronique", 220.00),
            ("KEYBOARD-010", "Clavier Mécanique", "Électronique", 95.00)
        ]
        
        for product in products_data:
            query = """
                INSERT INTO skus (sku_code, product_name, category, unit_cost)
                VALUES (%s, %s, %s, %s)
            """
            db.execute_query(query, product)
        
        print("✅ Produits insérés")
        
        # 5. Commandes de démonstration
        orders_data = [
            (1, '2024-09-01', 'PENDING', 2850.00),
            (2, '2024-09-02', 'CONFIRMED', 1250.00),
            (3, '2024-09-03', 'SHIPPED', 3400.00),
            (4, '2024-09-04', 'DELIVERED', 890.00),
            (1, '2024-08-30', 'DELIVERED', 1650.00)
        ]
        
        for order in orders_data:
            query = """
                INSERT INTO orders (customer_id, order_date, status, total_amount)
                VALUES (%s, %s, %s, %s)
            """
            db.execute_query(query, order)
        
        print("✅ Commandes insérées")
        
        # 6. Inventaire de démonstration
        inventory_data = [
            (1, 1, 50, 10),  # LAPTOP-001 dans Entrepôt 1
            (2, 1, 200, 20), # MOUSE-002 dans Entrepôt 1
            (3, 2, 30, 5),   # CHAIR-003 dans Entrepôt 2
            (4, 2, 15, 3),   # DESK-004 dans Entrepôt 2
            (5, 3, 80, 15),  # PHONE-005 dans Entrepôt 3
            (6, 1, 35, 8),   # TABLET-006 dans Entrepôt 1
            (7, 4, 25, 5),   # PRINTER-007 dans Entrepôt 4
            (8, 5, 150, 30), # CABLE-008 dans Entrepôt 5
            (9, 1, 40, 8),   # MONITOR-009 dans Entrepôt 1
            (10, 2, 60, 12)  # KEYBOARD-010 dans Entrepôt 2
        ]
        
        for inv in inventory_data:
            query = """
                INSERT INTO inventory (sku_id, warehouse_id, quantity_available, safety_stock)
                VALUES (%s, %s, %s, %s)
            """
            db.execute_query(query, inv)
        
        print("✅ Inventaire inséré")
        
        print("🎉 Toutes les données de démonstration ont été insérées avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion: {e}")
        return False
    
    finally:
        db.close()

if __name__ == "__main__":
    insert_demo_data()
