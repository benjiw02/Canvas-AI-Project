**EagleMate – Canvas AI Assistant**

EagleMate is an AI-powered assistant that connects to Canvas, parses course materials, and answers student questions using natural language. The system retrieves assignments, syllabus content, grades, and lecture files directly from Canvas, converts them into structured data, and uses the Gemini API to generate accurate and grounded responses.

**Features**

• Retrieves upcoming assignment deadlines

• Summarizes lecture materials (PDF, DOCX, PPTX)

• Extracts syllabus information from Canvas

• Generates study guides and practice quizzes

• Provides course-aware responses using a unified DataFrame

• Shows current grade averages for each course

• Includes safety rules to prevent cheating or Canvas modification

**Requirements**

You must run the assistant in a Python 3.10.11 virtual environment.

Install required dependencies:

```pip install beautifulsoup4 canvasapi pandas pandasai pandasai_litellm \```

```prompt_toolkit PyPDF2 python-docx python-pptx```

**API Keys Needed**

The following environment variables must be set before running the program:

```GEMINI_API_KEY=your_gemini_api_key```

```CANVAS_API_KEY=your_canvas_api_token```

Both keys are free to generate. 

**How to run**

1. Create and activate a Python 3.10.11 virtual environment.

2. Install all dependencies listed above.

3. Navigate to the src/ directory:
```cd src```

4. Run the assistant:  ```python Canvas_Assistant.py```

The system will fetch your Canvas courses, download and parse all relevant files, and load everything into memory. When loading is complete, you will be prompted for your name and entered into the chat interface.
