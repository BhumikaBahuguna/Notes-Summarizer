import os
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

# Load credentials from .env
load_dotenv()
endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

# Initialize client
client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# File to test
file_path = os.path.join("tests", "day2.pdf")

with open(file_path, "rb") as f:
    poller = client.begin_analyze_document(
        model_id="prebuilt-read",  # Best for OCR & handwriting
        body=f
    )
    result = poller.result()

# Print recognized text
print("\n📄 Extracted Text from pdf:\n")
for page in result.pages:
    for line in page.lines:
        print(line.content)
