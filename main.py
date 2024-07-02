from app import app
from app.models import create_tables

if __name__ == "__main__":
    with app.app_context():
        create_tables()
    app.run(debug=True)
