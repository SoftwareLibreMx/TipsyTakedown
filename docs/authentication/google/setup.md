# Setting Up Google Authentication API Using People API

This guide will walk you through how to set up Google Authentication and retrieve user profile information using the People API.
Prerequisites

  - Google Cloud Account: Make sure you have a Google account and access to Google Cloud Console.
  - Google Cloud Project: You must create or have an existing project in the Google Cloud Console.
  - OAuth 2.0 Client Credentials: Set up OAuth 2.0 credentials for authenticating users.
  - People API Enabled: Enable the People API in your project.

Step 1: Create a Google Cloud Project

  - Go to the Google Cloud Console.
  - Create a new project or select an existing one.
  - Once your project is created, note the Project ID.

Step 2: Enable the People API

  - In the Google Cloud Console, go to APIs & Services > Library.
  - Search for the People API and click on it.
  - Click Enable to activate the People API for your project.

Step 3: Set Up OAuth 2.0 Credentials

  - In the Google Cloud Console, go to APIs & Services > Credentials.
  - Click on Create Credentials and select OAuth 2.0 Client ID.
  - Configure your consent screen:
      - Select External for production apps, or Internal for G Suite users.
      - Fill in the required details (e.g., app name, support email).
  - Set up the OAuth consent screen:
      - Add scopes (like the People API scope: https://www.googleapis.com/auth/userinfo.profile).
      - Add authorized domains (for example, localhost for testing or your production domain).
  - Create OAuth client credentials:
      - Choose Web Application as the application type.
      - Provide an authorized Redirect URI (e.g., http://localhost:8000/callback for local testing).
      - Save your Client ID and Client Secret.

Step 4: Save json and set the envs

  - Save the downloaded file with the next name and path : www/client_secret.json

  - Set the envs with the info of the file in the .env file on root:
    - GOOGLE_OAUTH_CLIENT_ID
    - GOOGLE_OAUTH_CLIENT_SECRET
    - GOOGLE_OAUTH_REDIRECT_URI