#Setting Up MercadoPago Payment API

This guide will walk you through the steps needed to integrate MercadoPago’s payment API into your application.
Prerequisites

  - MercadoPago Account: You must have a MercadoPago account. Sign up here.
  - MercadoPago Developer Account: Enable the developer mode in your MercadoPago account to access API credentials.
  - API Credentials: Obtain your Access Token and Public Key for API authentication.

Step 1: Create a MercadoPago Account

  - Sign up for an account at MercadoPago.
  - Log in and go to the Developer Panel to get your API credentials.

Step 2: Get API Credentials

  - In your MercadoPago dashboard, go to Credentials under Your Business > Settings > Credentials.
  - You will get two credentials:
      - Public Key: Used for frontend integrations (to generate tokens for payments).
      - Access Token: Used for backend integrations to process payments.

You will use these keys to interact with the MercadoPago API.

Step 3: Set up env vars

Set up the public key in the .env file in the next variable name:
  - MP_ACCESS_TOKEN