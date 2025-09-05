# Project Title: Multi-Factor Authentication System
A secure web authentication system that uses a multi-factor verification and JWT tokens.
With token expiration and re-authentication on session expire, the project delivers both data security and a user-friendly experience.


## Features
- Built the **frontend interfaces using HTML, CSS, and JavaScript with camera input** for facial authentication and dynamic validation prompts.
- Utilized **Django REST Framework to serialize and manage user data for API endpoints**, which facilitated a structured and efficient way to handle registration and authentication requests.
- The system handles user authentication with secure password storage, **hashing password** using Django's built-in _'make_password'_ and _'check_password'_ which rely on **SHA256 algorithm**. 
- Creating a secured **biometric authentication** system using DeepFace comparing a live camera feed to a stored image in the database.
- Implemented **JWT tokenization with expiry-based re-authentication**, which ensures reliable protection against unauthorized access.

## Technology Stack
- `Frontend` HTML, CSS, JavaScript
- `Backend` Python, Django framework, MySQL, JWT (JSON Web Tokens), DeepFace and PIL (Pillow)
- `API` REST framework.

## Dependencies Installation
```
pip install django djangorestframework mysqlclient django-simple-jwt deepface Pillow
```

## Database Configuration
Make sure you have a MySQL database set up.
Update the database settings in settings.py with your credentials.

## Run Migrations
```
python manage.py makemigrations
python manage.py migrate
```
## Run the Server
```
python manage.py runserver
```

The application will be accessible at http://127.0.0.1:8000/

## Future Enhancements
- **Add Email Verification:** Implement a system to send a verification email during the sign-up process to ensure the user's email address is valid.
- **Password Strengthening:** Strengthen the password by looking for non-recurring password.
- **Another factor for authentication:** This project was intended to replace OTP based authentication. One can still go for email or sms based authentication.

## Documentation References:
- Django: (https://docs.djangoproject.com/en/stable/)
- Django REST Framework (DRF): (https://www.django-rest-framework.org/)
- DeepFace: (https://github.com/serengil/deepface)
- JWT (JSON Web Tokens): (https://jwt.io/introduction/)
- Pillow (PIL): (https://pillow.readthedocs.io/en/stable/)

# Authors
`Sameena Tabassum`: _(https://github.com/Sameenatabassum)_ - Contributed on JWT tokenization with expiry-based re-authentication and API Integration.

`Sanjana`: _(https://github.com/sanjana3281)_ - Developed the frontend interface and enhanced the user experience and integration.

`Sudhiksha H`: _(https://github.com/SudhikshaH)_ - Contributed for password and biometric authentication.


