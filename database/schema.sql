-- Schema pour la base de données Supply Chain
CREATE DATABASE supply_chain_db;

-- Table des entrepôts
CREATE TABLE warehouses (
    warehouse_id SERIAL PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    location VARCHAR(200),
    capacity_m3 DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des SKUs (produits)
CREATE TABLE skus (
    sku_id SERIAL PRIMARY KEY,
    sku_code VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    unit_cost DECIMAL(10,2),
    weight_kg DECIMAL(8,3),
    dimensions_cm VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des stocks
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    warehouse_id INTEGER REFERENCES warehouses(warehouse_id),
    sku_id INTEGER REFERENCES skus(sku_id),
    quantity_available INTEGER NOT NULL DEFAULT 0,
    quantity_reserved INTEGER NOT NULL DEFAULT 0,
    safety_stock INTEGER NOT NULL DEFAULT 0,
    reorder_point INTEGER NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(warehouse_id, sku_id)
);

-- Table des commandes
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id VARCHAR(50),
    order_date DATE NOT NULL,
    required_date DATE,
    status VARCHAR(20) DEFAULT 'PENDING',
    priority VARCHAR(10) DEFAULT 'NORMAL',
    total_value DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des lignes de commande
CREATE TABLE order_lines (
    order_line_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    sku_id INTEGER REFERENCES skus(sku_id),
    quantity_ordered INTEGER NOT NULL,
    quantity_shipped INTEGER DEFAULT 0,
    unit_price DECIMAL(10,2),
    line_total DECIMAL(12,2)
);

-- Table des expéditions
CREATE TABLE shipments (
    shipment_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    warehouse_id INTEGER REFERENCES warehouses(warehouse_id),
    carrier VARCHAR(100),
    tracking_number VARCHAR(100),
    ship_date DATE,
    estimated_delivery DATE,
    actual_delivery DATE,
    status VARCHAR(20) DEFAULT 'PREPARING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des mouvements de stock
CREATE TABLE stock_movements (
    movement_id SERIAL PRIMARY KEY,
    warehouse_id INTEGER REFERENCES warehouses(warehouse_id),
    sku_id INTEGER REFERENCES skus(sku_id),
    movement_type VARCHAR(20) NOT NULL, -- IN, OUT, ADJUSTMENT
    quantity INTEGER NOT NULL,
    reference_type VARCHAR(20), -- ORDER, RECEIPT, ADJUSTMENT
    reference_id INTEGER,
    movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

-- Table des fournisseurs
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(50),
    address TEXT,
    country VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    lead_time_days INTEGER DEFAULT 7,
    reliability_score DECIMAL(3,2) DEFAULT 1.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des clients
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(50),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des commandes fournisseurs
CREATE TABLE purchase_orders (
    po_id SERIAL PRIMARY KEY,
    po_number VARCHAR(50) UNIQUE NOT NULL,
    supplier_id INTEGER REFERENCES suppliers(supplier_id),
    warehouse_id INTEGER REFERENCES warehouses(warehouse_id),
    po_date DATE NOT NULL,
    expected_date DATE,
    received_date DATE,
    status VARCHAR(20) DEFAULT 'PENDING',
    total_value DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des lignes de commande fournisseur
CREATE TABLE po_lines (
    po_line_id SERIAL PRIMARY KEY,
    po_id INTEGER REFERENCES purchase_orders(po_id),
    sku_id INTEGER REFERENCES skus(sku_id),
    quantity_ordered INTEGER NOT NULL,
    quantity_received INTEGER DEFAULT 0,
    unit_cost DECIMAL(10,2),
    line_total DECIMAL(12,2)
);

-- Index pour optimiser les performances
CREATE INDEX idx_inventory_warehouse_sku ON inventory(warehouse_id, sku_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_shipments_status ON shipments(status);
CREATE INDEX idx_stock_movements_date ON stock_movements(movement_date);
CREATE INDEX idx_stock_movements_sku ON stock_movements(sku_id);

-- Vues pour les KPIs
CREATE VIEW v_stock_status AS
SELECT 
    w.warehouse_name,
    s.sku_code,
    s.product_name,
    i.quantity_available,
    i.safety_stock,
    i.reorder_point,
    CASE 
        WHEN i.quantity_available <= i.safety_stock THEN 'CRITICAL'
        WHEN i.quantity_available <= i.reorder_point THEN 'LOW'
        ELSE 'OK'
    END as stock_status
FROM inventory i
JOIN warehouses w ON i.warehouse_id = w.warehouse_id
JOIN skus s ON i.sku_id = s.sku_id;

CREATE VIEW v_order_fulfillment AS
SELECT 
    o.order_number,
    o.order_date,
    o.required_date,
    o.status,
    COUNT(ol.order_line_id) as total_lines,
    SUM(CASE WHEN ol.quantity_shipped >= ol.quantity_ordered THEN 1 ELSE 0 END) as fulfilled_lines,
    ROUND(
        SUM(CASE WHEN ol.quantity_shipped >= ol.quantity_ordered THEN 1 ELSE 0 END) * 100.0 / COUNT(ol.order_line_id), 
        2
    ) as fulfillment_rate
FROM orders o
LEFT JOIN order_lines ol ON o.order_id = ol.order_id
GROUP BY o.order_id, o.order_number, o.order_date, o.required_date, o.status;
