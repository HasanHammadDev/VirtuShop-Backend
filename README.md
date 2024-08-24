# VirtuShop Backend

This project aims to create a backend infrastructure for a virtual reality e-commerce platform. Key functionalities include user authentication, shopping cart operations, and review management. The backend is built using Python Flask and MySQL. RESTful APIs will be implemented to handle requests from the frontend VR application.

Please refer to the [VitruShop] repository for the frontend code, which is located here:

https://github.com/HasanHammadDev/VirtuShop
## Screenshots
### JWT Decorator Function (Passes through the current user)
  ![JWT](https://i.ibb.co/YdnCcff/jwt.jpg)
  
## Installation

How to install
```bash 
  git clone https://github.com/HasanHammadDev/VirtuShop-Backend.git
  cd VirtuShop-Backend
  python -m venv venv
  source venv/scripts/activate
  pip install -r requirements.txt
  python app.py
```
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file in the root of your VirtuShop-Backend folder.

`DATABASE_URI`=your_db_uri
`JWT_SECRET_KEY`=your_jwt_secret_key
`GOOGLE_CLIENT_ID`=your_google_client_id
## Contributing

Contributions are always welcome!
