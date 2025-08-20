# BioVerse - Flask Implementation

## Overview

BioVerse is an AI-powered alien creator application that generates scientifically accurate alien species based on planetary characteristics. This implementation uses a Flask backend to handle all API logic server-side with retry mechanisms, minimizing JavaScript usage and resolving CORS issues.

## Project Structure

```
BioVerse/
├── app.py              # Flask application (main server)
├── bioverse_app.py    # BioVerse application logic (Python)
├── requirements.txt   # Python dependencies
├── .env               # Environment configuration
├── templates/         # HTML templates
│   └── index.html    # Main application page
└── static/           # Static assets
    ├── styles.css    # Application styling
    └── script.js     # Minimal frontend UI logic only
```

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   # On Linux/Mac
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in `.env`:
   ```env
   # LLM Configuration
   LLM_BASE_URL=https://samuraiapi.in/v1
   LLM_API_KEY=your-api-key-here
   LLM_MODEL=groq/moonshotai/kimi-k2-instruct

   # Image Generation Configuration
   IMAGE_BASE_URL=https://api.together.xyz/v1
   IMAGE_API_KEY=your-image-api-key-here
   IMAGE_MODEL=black-forest-labs/FLUX.1-schnell-Free

   # Server Configuration
   PORT=8000
   HOST=localhost
   ```

5. Run the Flask application:
   ```bash
   python app.py
   ```

6. Access the application in your browser at `http://localhost:8000`

## Flask Endpoints

- `GET /` - Serve the main application page
- `POST /api/create-alien` - Create alien species based on planet name (handles all API calls server-side)
- `GET /api/health` - Health check endpoint

## Architecture

This implementation follows a server-side architecture to minimize client-side JavaScript:

1. **Frontend**: Minimal JavaScript for UI interactions only
2. **Backend**: Python Flask server handles all API logic
3. **Data Processing**: All LLM and image API calls are made server-side
4. **Template Rendering**: Results are rendered using Flask templates

## CORS Issue Resolution

The original application experienced CORS errors when making direct API requests from the browser to `https://samuraiapi.in/v1/chat/completions`. This Flask implementation resolves the issue by:

1. **Server-side proxy**: All API requests are routed through the Flask server, eliminating cross-origin restrictions
2. **Same-origin requests**: The frontend makes requests to the same origin (`localhost:8000`), bypassing browser CORS policies
3. **Centralized configuration**: API keys and endpoints are managed server-side, improving security

## How It Works

1. User enters a planet name in the input field
2. Frontend sends request to Flask endpoint `/api/create-alien` with planet name
3. Flask server processes the request using BioVerseApp class:
   - Analyzes planet characteristics using LLM API with retry mechanism
   - Generates alien species based on planet data with retry mechanism
   - Creates alien image using image generation API with retry mechanism
4. If any API call fails after all retries, an error is returned to the frontend
5. If all API calls succeed, Flask server returns all results as JSON
6. Frontend displays the results with minimal JavaScript processing

## Dependencies

- Flask - Web framework for Python
- python-dotenv - Environment variable management
- requests - HTTP library for Python

## Troubleshooting

### CORS Errors
If you still experience CORS issues, ensure the Flask server is running and the frontend is making requests to `http://localhost:8000/api/create-alien`.

### API Key Issues
Verify that your API keys in the `.env` file are valid and have proper permissions for the respective services.

### Network Errors
Check your internet connection and ensure the API endpoints are accessible from your server environment.

## Debugging

When running the application in debug mode, detailed logs will be printed to the console showing:
- Incoming request data
- API responses from LLM and image services
- Content being parsed for JSON
- Error messages and retry attempts

These logs can help identify issues with API responses and parsing problems.

## Common Issues and Fixes

### JSON Parsing Errors
If you encounter "No valid JSON found in response" errors:
- Check if the API response is being cut off due to token limits
- Increase the `max_tokens` parameter in the API calls
- Verify the response content in debug logs to ensure it contains valid JSON

### API Response Truncation
The application uses 300 max_tokens for LLM calls to ensure complete JSON responses. If you still experience truncation:
- Further increase the `max_tokens` value in bioverse_app.py
- Check the debug logs to see the actual response content and length

## Future Improvements

- Add more sophisticated error handling and user feedback for API failures
- Implement caching for repeated requests
- Add support for multiple LLM providers
- Enhance security with proper API key management
- Add detailed logging for better debugging and monitoring
- Implement more advanced retry mechanisms with circuit breaker patterns