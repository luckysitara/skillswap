
markdown
# Skillswap API

Welcome to the Skillswap API! This project is designed to help users connect, share skills, and collaborate with others. It features user authentication, messaging, skill management, notifications, and reviews.

## Features

- **User Authentication**: Sign up, log in, and manage user profiles.
- **Password Reset**: Allows users to reset their passwords.
- **Messaging**: Send and receive messages between users.
- **Skill Management**: Create and manage skills associated with users.
- **Notifications**: Users can receive notifications for messages and updates.
- **Reviews**: Users can leave reviews for each other after collaborations.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Flask
- SQLite
- cURL (for testing)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/skillapi.git
   cd skillapi/backend
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:

   Make sure to set your email credentials in the `config.py` file. Then run the following commands in the Flask shell:

   ```bash
   from app import db
   db.create_all()
   ```

5. **Run the Flask application**:

   ```bash
   flask run
   ```

   Your API should now be running on `http://127.0.0.1:5000`.

## API Testing with cURL

Here are some `curl` commands to test the various functionalities of the Skillswap API.

### 1. User Authentication

#### Sign Up

```bash
curl -X POST http://127.0.0.1:5000/auth/signup \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "email": "testuser@example.com", "password": "yourpassword"}'
```

#### Login

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
-H "Content-Type: application/json" \
-d '{"email": "testuser@example.com", "password": "yourpassword"}'
```

### 2. User Profile Management

#### Get User Profile

```bash
curl -X GET http://127.0.0.1:5000/auth/1
```

#### Update User Profile

```bash
curl -X PUT http://127.0.0.1:5000/auth/1 \
-H "Content-Type: application/json" \
-d '{"username": "updateduser", "email": "updateduser@example.com", "password": "newpassword"}'
```

### 3. Password Reset (Optional)

#### Reset Password

```bash
curl -X POST http://127.0.0.1:5000/auth/password/reset \
-H "Content-Type: application/json" \
-d '{"email": "testuser@example.com"}'
```

### 4. Messaging Functionality

#### Send Message

```bash
curl -X POST http://127.0.0.1:5000/messages/ \
-H "Content-Type: application/json" \
-d '{"sender_id": 1, "receiver_id": 2, "content": "Hello there!"}'
```

#### Get Messages

```bash
curl -X GET http://127.0.0.1:5000/messages/1
```

### 5. Skill Management

#### Create Skill

```bash
curl -X POST http://127.0.0.1:5000/skills/ \
-H "Content-Type: application/json" \
-d '{"name": "Python Programming", "user_id": 1}'
```

#### Get User Skills

```bash
curl -X GET http://127.0.0.1:5000/skills/1
```

### 6. Notification Management

#### Create Notification

```bash
curl -X POST http://127.0.0.1:5000/notifications/ \
-H "Content-Type: application/json" \
-d '{"user_id": 1, "message": "You have a new message!"}'
```

#### Get Notifications

```bash
curl -X GET http://127.0.0.1:5000/notifications/1
```

### 7. Review Management

#### Leave Review

```bash
curl -X POST http://127.0.0.1:5000/reviews/ \
-H "Content-Type: application/json" \
-d '{"reviewer_id": 1, "reviewee_id": 2, "content": "Great collaboration!"}'
```

#### Get Reviews for User

```bash
curl -X GET http://127.0.0.1:5000/reviews/2
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

---
