Phishing Domain Detection API
Description
This API detects whether a given website domain is legitimate or potentially a phishing site. It leverages a machine learning model trained on various domain features.

Key Features:

Accurately distinguishes legitimate domains from phishing domains with a 96% accuracy rate.
Can be deployed on AWS App Runner for easy scalability and access.
Alternatively, can be run locally for development or testing purposes.

Installation
Option 1: Deployment on AWS App Runner
Create an AWS App Runner service using the provided Dockerfile.
Push the Docker image to AWS ECR (Elastic Container Registry).
Configure the App Runner service to use the ECR image.
Option 2: Running Locally
Install dependencies:
Bash
pip install -r requirements.txt
Use code with caution. 
Run the API:
Bash
python app.py
Use code with caution. 

Dataset Features: The model is trained on a dataset with 111 diverse features, categorized as follows:
Attributes based on the URL itself (e.g., length, presence of special characters, suspicious keywords)
Attributes based on the domain name (e.g., length, age, IP address)
Attributes based on the URL directory structure (e.g., depth, presence of specific directories)
Attributes based on the URL file name (e.g., length, common patterns, extensions)
Attributes based on URL parameters (e.g., number, length, suspicious values)
Attributes based on resolving the URL and using external services (e.g., WHOIS information, domain reputation scores)

Usage
Send a POST request to the API endpoint with the domain name to be checked in the request body.
The API will respond with a JSON object indicating whether the domain is legitimate or a potential phishing site.
Example Usage
Bash
curl -X POST -H "Content-Type: application/json" -d '{"domain": "example.com"}' http://localhost:5000/predict
Use code with caution. 


Contact
https://www.linkedin.com/in/aryan-gaur-b49550258/
