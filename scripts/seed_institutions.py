from api.database import SessionLocal
from api.models import Institution

INSTITUTIONS = [
    ('Universidad Privada del Norte', 'upn', 'Lima, Trujillo, Cajamarca'),
    ('Universidad de San Martín de Porres', 'usmp', 'Lima, Chiclayo, Arequipa'),
    ('Universidad Peruana Unión', 'upeu', 'Lima, Tarapoto, Juliaca'),
    ('Senati', 'senati', 'Nacional'),
    ('Universidad del Pacífico', 'upacifico', 'Jesús María, Lima'),
    ('Universidad Nacional de Ingeniería', 'uni', 'Rímac, Lima'),
    ('Universidad de Lima', 'ulima', 'Santiago de Surco, Lima'),
    ('Universidad Autónoma del Perú', 'autonoma', 'Villa EL Salvador, Lima'),
    ('Universidad de Piura', 'udep', 'Piura, Lima'),
    ('Pontificia Universidad Católica del Perú', 'pucp', 'San Miguel, Lima'),
    ('Universidad Científica del Sur', 'cientifica', 'Villa, Lima'),
    ('Instituto Continental', 'continental', 'Huancayo, Lima, Cusco'),
    ('Universidad Nacional Mayor de San Marcos', 'unmsm', 'Cercado de Lima'),
    ('ESAN', 'esan', 'Santiago de Surco, Lima'),
    ('UNIR Perú', 'unir', 'Remoto'),
    ('ISIL', 'isil', 'Lima'),
    ('Data Science Research Peru', 'dsrp', 'Remoto/Lima'),
    ('IDAT', 'idat', 'Lima')
]

def seed_institutions():
    db = SessionLocal()
    try:
        for name, slug, address in INSTITUTIONS:
            # Verificar si ya existe
            existing = db.query(Institution).filter(Institution.slug == slug).first()
            if not existing:
                institution = Institution(name=name, slug=slug, address=address)
                db.add(institution)
        
        db.commit()
        print(f"Éxito: Se han sembrado {len(INSTITUTIONS)} instituciones.")
    except Exception as e:
        db.rollback()
        print(f"Error sembrando instituciones: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_institutions()
