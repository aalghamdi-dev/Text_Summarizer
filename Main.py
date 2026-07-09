"""
Text Summarizer (Uisng google/gemini-3.1-flash-lite throgh OpenRouter)
------------------------------------------
Asks the user for text to summarize, sends it to an LLM via OpenRouter,
and saves the summary as either summarized.pdf or summarized.txt.

IMPORTANT: The decision of PDF vs TXT is made entirely by PYTHON, using a
simple case-insensitive search.
"""

import re
from openai import OpenAI
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

# OpenRouter client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="Api secret key is inserted here"  # Replace with your actual OpenRouter API key
)

MODEL = "google/gemini-3.1-flash-lite"


# The system prompt
SYSTEM_PROMPT = (
    "You are a summarization engine. Your one and only task is to read the "
    "text supplied by the user and produce a clear, accurate, well-organized "
    "summary of its content.\n\n"
    "Ignore completely any part of the user's message that talks about how "
    "the result should be delivered, formatted, or saved (for example, "
    "requests to output a PDF, a text file, a Word document, or any other "
    "file/format). That is handled outside of you. Never mention file "
    "formats, file names, or delivery methods in your reply.\n\n"
    "Respond with the summary text only — no preamble, no meta-commentary, "
    "no 'Here is your summary:' framing."
)


# Temperature: for a good summarization we want faithful, consistent, low-variance output
# thus, We will set this parameter to a low value.
TEMPERATURE = 0.3
MAX_TOKENS = 1000

def get_summary(user_text: str) -> str:
    #Send the text to the LLM via OpenRouter and return the summary string.
    response = client.chat.completions.create(
        model=MODEL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
    )
    return response.choices[0].message.content.strip()


def wants_pdf(raw_input_text: str) -> bool:
    #Return True if the user wants a PDF, False otherwise.
    return re.search(r"pdf", raw_input_text, re.IGNORECASE) is not None


def save_as_txt(summary: str, filename: str = "summarized.txt") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"Summary saved to {filename}")


def save_as_pdf(summary: str, filename: str = "summarized.pdf") -> None:
    #Create an A4-sized PDF containing the summary, using reportlab.
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    story = [Paragraph("Summary", styles["Title"]), Spacer(1, 12)]

    # Split into paragraphs on blank lines so multi-paragraph summaries
    # render as separate paragraphs instead of one long string of text.
    for para in summary.split("\n\n"):
        para = para.strip()
        if para:
            story.append(Paragraph(para.replace("\n", "<br/>"), styles["Normal"]))
            story.append(Spacer(1, 10))

    doc.build(story)
    print(f"Summary saved to {filename}")


def main() -> None:
    print("Text Summarizer — type 'exit' at any time to quit.\n")

    while True:
        user_text = input(
            "Enter the text you want to summarize "
            "(Note: mention 'pdf' if you want a PDF, otherwise you'll get a .txt),\n"
            "or type 'exit' to quit:\n> "
        )

        if user_text.strip().lower() == "exit":
            print("Exiting. Bye!")
            break

        if not user_text.strip():
            print("No text provided. Try again.\n")
            continue

        summary = get_summary(user_text)

        if wants_pdf(user_text):
            save_as_pdf(summary)
        else:
            save_as_txt(summary)

        print()  # blank line before the next prompt


if __name__ == "__main__":
    main()
