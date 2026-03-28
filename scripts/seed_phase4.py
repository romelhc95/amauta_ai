from api.database import SessionLocal
from api.models import Course
from decimal import Decimal

def seed_phase4():
    db = SessionLocal()
    courses = db.query(Course).all()
    
    for course in courses:
        if "Maestría" in course.name:
            course.price_pen = Decimal("25000.00")
            course.expected_monthly_salary = Decimal("8500.00")
            course.duration = "24 meses"
        elif "Ingeniería" in course.name:
            course.price_pen = Decimal("60000.00")
            course.expected_monthly_salary = Decimal("4500.00")
            course.duration = "10 ciclos"
        elif "Programa especializado" in course.name:
            course.price_pen = Decimal("3500.00")
            course.expected_monthly_salary = Decimal("5000.00")
            course.duration = "6 meses"
        else:
            course.price_pen = Decimal("5000.00")
            course.expected_monthly_salary = Decimal("3000.00")
            course.duration = "Variable"
    
    db.commit()
    db.close()
    print("Fase 4: Datos de ROI sembrados con éxito.")

if __name__ == "__main__":
    seed_phase4()
