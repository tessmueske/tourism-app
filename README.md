## magwa: Helping Solve the Tourism Crisis in the Canary Islands 
magwa is a traditional word from the canary islands that means disappointment, grief, or sadness.

## About the Project
I started building this project in the autumn of 2024 after learning about the tourism crisis in the Canary Islands. I want to visit special places like this one without contributing to the growing economic and ecological challenges. [Learn more on the application's About page.]

## Tech Stack
- **Frontend**: React with JavaScript, Formik for form validation, React Context for global state management.
- **Backend**: Python with Flask and SQL, using Flask-Session for account verification and Bcrypt for password hashing.
- **Integrations**: Formspree for contact forms, Flask-Mail for account verification emails.
- **Routing**: ReSTful conventions with full CRUD functionality.

## Features
- Users can:
  - Create, edit, and delete accounts.
  - Create, edit, and delete posts.
  - Comment on and delete others' posts.
  - View profiles and filter posts by hashtags.

## How to Install on Your Machine
**Installation & Local Setup**

This project has two parts:

* **Backend** (Flask/Python) in the `/server` folder
* **Frontend** (React/JavaScript) in the `/client` folder

Follow these steps to run the app locally:

---

**1. Clone the repository**

```bash
git clone https://github.com/tessmueske/tourism-app.git
cd tourism-app
```

---

**2. Backend Setup**

1. **Go to the server folder**

   ```bash
   cd server
   ```

2. **Install Pipenv** (if not already installed)

   ```bash
   pip install --user pipenv
   ```

3. **Install dependencies**

   ```bash
   pipenv install
   pipenv install Flask Flask-Session Flask-Cors Flask-Bcrypt Flask-SQLAlchemy python-dotenv psycopg2-binary Flask-Mail
   ```

4. **Create a `.env` file** in `/server` with your environment variables:

   ```env
   FLASK_DEBUG=1
   SECRET_KEY=dev-secret-key

   MAIL_SERVER=localhost
   MAIL_PORT=1025
   MAIL_USERNAME=
   MAIL_PASSWORD=
   MAIL_USE_TLS=false
   MAIL_USE_SSL=false

   DATABASE_URL=sqlite:///app.db
   FRONTEND_URL=http://localhost:3000
   ```

5. **Run the backend**

   ```bash
   pipenv run python app.py
   ```

   The server will start on [http://127.0.0.1:5555](http://127.0.0.1:5555).

---

**3. Frontend Setup**

1. **Open a new terminal** and navigate to the client folder:

   ```bash
   cd client
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Run the frontend**

   ```bash
   npm start
   ```

   The React app will start on [http://localhost:3000](http://localhost:3000) and connect to the backend.

---

### **4. Development Notes**

* The backend runs on port **5555** by default; the frontend runs on **3000**.
* Make sure both are running for full functionality.
* The backend `.env` file is for **local development only** — do not commit secrets.


## Future Considerations
- **Community Calendar**: A shared event planning tool.  
- **Trip Planner**: An itinerary builder for sustainable travel.  
- **Friendship Capabilities**: Connect users with similar travel interests.  
- **In-app Messaging**: Allow users to communicate directly.  
- **Filtered Views**: View posts by travelers, local experts, or advertisers.

## Sources
- [Euronews: Canary Islands tourism crisis](https://www.euronews.com/my-europe/2024/10/20/thousands-protest-against-over-tourism-in-canary-islands)
- [The Guardian: Unsustainable tourism protests](https://www.theguardian.com/world/2024/apr/20/thousands-protest-canary-islands-unsustainable-tourism)
- [Spanish National Institute of Statistics (INE)](https://www.ine.es/dyngs/Prensa/es/ECV2023.htm)
- [Canarias Se Agota](https://canariaseagota.com/)


