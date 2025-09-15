-- Mise à jour du schéma pour ajouter la table customers manquante

-- Vérifier si la table customers existe déjà
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'customers') THEN
        -- Créer la table customers
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
        
        RAISE NOTICE 'Table customers créée avec succès';
    ELSE
        RAISE NOTICE 'Table customers existe déjà';
    END IF;
END $$;

-- Vérifier et mettre à jour la table suppliers si nécessaire
DO $$
BEGIN
    -- Ajouter les colonnes manquantes à suppliers si elles n'existent pas
    IF NOT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'suppliers' AND column_name = 'contact_person') THEN
        ALTER TABLE suppliers ADD COLUMN contact_person VARCHAR(100);
        RAISE NOTICE 'Colonne contact_person ajoutée à suppliers';
    END IF;
    
    IF NOT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'suppliers' AND column_name = 'phone') THEN
        ALTER TABLE suppliers ADD COLUMN phone VARCHAR(50);
        RAISE NOTICE 'Colonne phone ajoutée à suppliers';
    END IF;
    
    IF NOT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'suppliers' AND column_name = 'address') THEN
        ALTER TABLE suppliers ADD COLUMN address TEXT;
        RAISE NOTICE 'Colonne address ajoutée à suppliers';
    END IF;
    
    IF NOT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'suppliers' AND column_name = 'country') THEN
        ALTER TABLE suppliers ADD COLUMN country VARCHAR(100);
        RAISE NOTICE 'Colonne country ajoutée à suppliers';
    END IF;
    
    IF NOT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'suppliers' AND column_name = 'is_active') THEN
        ALTER TABLE suppliers ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
        RAISE NOTICE 'Colonne is_active ajoutée à suppliers';
    END IF;
    
    -- Renommer contact_email en email si elle existe
    IF EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'suppliers' AND column_name = 'contact_email') THEN
        ALTER TABLE suppliers RENAME COLUMN contact_email TO email;
        RAISE NOTICE 'Colonne contact_email renommée en email dans suppliers';
    END IF;
END $$;
