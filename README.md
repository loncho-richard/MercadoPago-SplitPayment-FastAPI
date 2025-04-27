# Split Payments Marketplace

A FastAPI-based marketplace with Mercado Pago integration to handle split payments between sellers and marketplace fees.

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Setup](#-setup)
- [Testing Accounts](#-testing-accounts)
- [Configuration Guide](#-configuration-guide)
- [API Endpoints](#-api-endpoints)
- [Notes](#-notes)

## 🌟 Overview

This project enables:
- Sellers to connect their Mercado Pago accounts via OAuth2
- Buyers to pay via Mercado Pago Checkout Pro
- Automatic payment splitting between sellers and marketplace
- Sandbox testing environment support

## 🚀 Features

- Seller onboarding with Mercado Pago OAuth
- Payment processing with split fees (seller + marketplace)
- JWT authentication system
- Role-based access control (Buyer/Seller)
- Webhook payment notifications
- Sandbox/test mode implementation

## 🛠 Setup

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/split-payments-marketplace.git
   cd split-payments-marketplace
   ```

2. **Create virtual env**
   ```bash
   python3 -m venv env
   source ./env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**
   ```ini
   # Database
   DATABASE_URL=sqlite:///database.db
   
   # Authentication
   SECRET_KEY=your-super-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Application(You need an SSL certificate through a tunnel)
   DOMAIN=https://secure-domain
   
   # Mercado Pago
   MP_CLIENT_ID=your-marketplace-app-client-id
   MP_CLIENT_SECRET=your-marketplace-app-client-secret
   MP_MARKETPLACE_ACCESS_TOKEN=TEST-... # For fee collection
   ```

## 🔧 Testing Accounts

You need to create these accounts for testing:

| Role           | Access Token             |
|----------------|--------------------------|
| Marketplace    |`APP_USR-...` (from .env) |
| Seller         | Obtained via OAuth       |
| Buyer          | Pay                      |

## 🔄 Configuration Guide

### 1. Mercado Pago Setup
1. Create [Mercado Pago Developer Account](https://www.mercadopago.com.co/developers)
2. Create marketplace application
3. Get credentials:
   - `MP_CLIENT_ID`
   - `MP_CLIENT_SECRET`
   - `MP_MARKETPLACE_ACCESS_TOKEN` (Marketplace fee collection)

### 2. Testing Flow
1. **Seller Onboarding**
   ```http
   GET /api/v1/mercadopago/get-auth-url
   ```
   - Seller connects account
   - OAuth tokens stored in database

2. **Create Payment Checkout**
   ```http
   POST /api/v1/mercadopago/create-checkout
   {
     "items": [{
       "title": "Premium Item",
       "quantity": 1,
       "unit_price": 150.99
     }],
     "success_url": "http://localhost:3000/success",
     "failure_url": "http://localhost:3000/failure",
     "pending_url": "http://localhost:3000/pending"
   }
   ```

3. **Buyer Payment**
   - Use account balance
   - Simulate payment statuses:
     - Approved: Complete payment
     - Pending: `status=pending`
     - Rejected: `status=rejected`

## 📡 API Endpoints

| Endpoint                          | Method | Description                     | Auth     |
|-----------------------------------|--------|---------------------------------|----------|
| `/api/v1/mercadopago/get-auth-url` | GET    | Get OAuth URL                   | Seller   |
| `/api/v1/mercadopago/connect`      | GET    | Complete OAuth flow             | Public   |
| `/api/v1/mercadopago/create-checkout` | POST | Create payment checkout         | Seller   |
| `/api/v1/mercadopago/webhook`      | POST   | Payment notifications           | Public   |

## 📌 Notes

- **Sandbox Mode:** All transactions use test environment
- **Webhook Setup:** Configure in Mercado Pago dashboard:
  ```
  URL: https://yourdomain.com/api/v1/mercadopago/webhook
  Events: payment.created, payment.updated
  ```
- **Fee Structure:** Marketplace keeps 5% fee (adjustable in code)
- **Security:** Always:
  - Validate Mercado Pago signatures
  - Use HTTPS in production
  - Store secrets in `.env`