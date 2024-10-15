# run.py
from app import create_app, db

# Create an instance of the app
app = create_app()

if __name__ == '__main__':
    # Create database tables within the application context
    with app.app_context():
        try:
            db.create_all()  # Create all tables
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")

    # Print app details for debugging
    print(f"App name: {app.name}")
    print(f"App routes: {app.url_map}")

    # Run the Flask app in debug mode
    app.run(debug=True)
