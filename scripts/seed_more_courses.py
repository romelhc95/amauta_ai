from api.database import SessionLocal
from api.models import Institution, Course
from decimal import Decimal
import random

COURSES_DATA = [
    ("Data Science & AI", "data-science-ai", 15000, 5500, "Remoto", "8 meses"),
    ("Desarrollo Full Stack", "full-stack-dev", 12000, 4800, "Híbrido", "6 meses"),
    ("Ciberseguridad Avanzada", "ciberseguridad", 18000, 6500, "Remoto", "10 meses"),
    ("Marketing Digital", "marketing-digital", 8000, 3500, "Remoto", "4 meses"),
    ("UX/UI Design", "ux-ui-design", 9500, 4200, "Híbrido", "5 meses"),
    ("Product Management", "product-management", 14000, 7000, "Remoto", "6 meses"),
    ("Ingeniería de Datos", "data-engineering", 20000, 7500, "Presencial", "12 meses"),
    ("Cloud Computing (AWS)", "cloud-aws", 11000, 6000, "Remoto", "5 meses"),
    ("Blockchain Development", "blockchain-dev", 22000, 9000, "Remoto", "9 meses"),
    ("E-commerce Strategy", "ecommerce-strategy", 7000, 4000, "Híbrido", "3 meses")
]

def seed_more_courses():
    db = SessionLocal()
    try:
        institutions = db.query(Institution).all()
        if not institutions:
            print("No hay instituciones. Ejecuta primero seed_institutions.py")
            return

        for name, slug, price, salary, mode, duration in COURSES_DATA:
            inst = random.choice(institutions)
            existing = db.query(Course).filter(Course.slug == slug).first()
            if not existing:
                course = Course(
                    institution_id=inst.id,
                    name=name,
                    slug=slug,
                    price_pen=Decimal(str(price)),
                    expected_monthly_salary=Decimal(str(salary)),
                    mode=mode,
                    address=inst.address,
                    duration=duration,
                    url=f"{inst.website_url}/programas/{slug}"
                )
                db.add(course)
        
        db.commit()
        print(f"Éxito: Se han sembrado {len(COURSES_DATA)} cursos adicionales.")
    except Exception as e:
        db.rollback()
        print(f"Error sembrando cursos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_more_courses()
