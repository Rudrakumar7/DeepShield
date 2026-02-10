from app import app, db

print("Imported app and db")

with app.app_context():
    print("Creating tables...")
    try:
        db.create_all()
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        import traceback
        traceback.print_exc()
