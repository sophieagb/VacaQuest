# VacaQuest
VacaQuest is an AI-driven platform that recommends personalized vacation destinations based on user preferences. It utilizes advanced algorithms to suggest ideal travel spots, ensuring every user finds the perfect getaway effortlessly.

## Pages and Navigation
Login & Registration Pages: Simple and secure user authentication.
Index Page: Includes sections for Easy Visa Destinations, Most Popular, and Bookings.
Sidebar Navigation: Access Dashboard, My Tickets, Favorites, Messages, Transactions, Settings, and Logout.

## Getting Started

#### Prerequisites
Python 3.8+
MySQL
Flask
Figma (for design reference)
Installation

### MySQL Setup

1. **Install MySQL**: Download and install MySQL from the [official website](https://dev.mysql.com/downloads/installer/).

2. **Create a Database and User**:

   Open the MySQL command line:

   ```sh
   mysql -u root -p
   CREATE DATABASE travel_app;
   CREATE USER 'travel_admin'@'localhost' IDENTIFIED BY 'travel-pass123';
   GRANT ALL PRIVILEGES ON travel_app.* TO 'travel_admin'@'localhost';
   FLUSH PRIVILEGES;

   Then create a .env file and paste the following:
   
    OPENAI_API_KEY='your-openai-api-key'
  
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'travel_admin'
    MYSQL_PASSWORD = 'travel-pass123'
    MYSQL_DB = 'travel_app'

#### Clone the repository:
git clone https://github.com/yourusername/vacaquest.git


#### Navigate to the project directory:
cd vacaquest


#### Create and activate a virtual environment:
python3 -m venv venv
Then
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


#### Install dependencies:
pip install -r requirements.txt


#### Running the Application
Set the FLASK_APP environment variable:
##### export FLASK_APP=app.backend:create_app   
##### ensure you have your OpenAI API key set in your .env file: OPENAI_API_KEY='your-openai-api-key'
##### On Windows use `set FLASK_APP=app.backend:create_app`


#### Run the development server:
flask run

#### Open your browser and visit:
http://localhost:5000

## License
This project is licensed under the MIT License - see the LICENSE file for details.





    


