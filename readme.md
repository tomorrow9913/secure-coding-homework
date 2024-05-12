# Secure Coding

Tiny Shopping Mall Website.

You should add some functions and complete the security requirements.

## requirements

if you don't have a miniconda(or anaconda), you can install it on this url.
https://docs.anaconda.com/free/miniconda/index.html

```
conda create -n secure_coding python=3.9
conda activate secure_coding
pip install -r requirements.txt
```

## usage

run the front and backend processes.

```
streamlit run streamlit_app.py
uvicorn fastapi_app:app --reload
```

if you want to test on external machine, you can utilize the ngrok to forwarding the url.
```
# optional
ngrok http 8501
```

## Structure
```
SECURE-CODING
│  fastapi_app.py
│  readme.md
│  requirements.txt
│  secure-coding-checklist.xlsx
│  shopping_mall.db
│  streamlit_app.py
│  시큐어코딩.pdf
│
├─core
│  │  database.py
│  │  models.py
│  └─ oauthConfig.py
│
├─crud
│  │  Auth.py
│  │  Order.py
│  │  Pay.py
│  │  Products.py
│  └─ Users.py
│
├─routes
│  │  Auth.py
│  │  Order.py
│  │  Pay.py
│  │  Products.py
│  │  Users.py
│  └─ __init__.py
│
├─schema
│  │  Auth.py
│  │  Product.py
│  └─  User.py
│
└─utils
   │  oauth.py
   └─ passHash.py
```
- `core`: database connection, models and oauth configuration
- `crud`: CRUD operations for each table
- `routes`: API routes
- `schema`: Pydantic models for request and response
- `utils`: utility functions