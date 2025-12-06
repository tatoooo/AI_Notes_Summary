import google.generativeai as genai
from backend.config import settings

# Initialize Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

def summarize_content(text: str) -> str:
    """Use Gemini to summarize the text into Notion-friendly Markdown."""
    if not settings.GEMINI_API_KEY:
        return "Error: Gemini API Key not found."
    
    if not text.strip():
        return "Error: No text could be extracted from the document."

    prompt = (
        "You are an expert note-taker. Summarize the following document content into a structured "
        "Notion-friendly format (Markdown). \n"
        "Requirements:\n"
        "1. Use H2 (##) for main sections.\n"
        "2. Use bullet points for key details.\n"
        "3. Bold (**text**) important keywords.\n"
        "4. Keep it concise but comprehensive.\n\n"
        "Content:\n"
        f"{text[:15000]}" # Truncate to avoid context limit issues for MVP
    )

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"
