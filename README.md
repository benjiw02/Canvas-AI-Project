Running the Canvas Assistant chat bot requires a active python 3.10.11 virtual enviroment with the following dependacies 
being required (pip install beautifulsoup canvasapi pandas pandasai pandasai_litellm prompt_toolkit PyPDF2 python_docx python_pptx)

The User must also set a Gemini API key (currently free) and a Canvas access token (Free from canvas) as GEMINI_API_KEY and CANVAS_API_KEY in either their enviromental variables for the program to function as intended. 

After handling the dependacies and variables type: python Canvas_Assitant.py into the virtual enviorment from the src directory and the script will begin loading your canvas data from the Canvas API. Once all data is loaded into memmory
you will be prompted for a name. Enter the name of your choosing and you will proceed to the chat terminal. Ensure you are specific and concise with your prompts for the best results. The AI is capable of summarizing and gathering information from files, showing upcomming deadlines, Showing grade averages for courses, creating a practice quiz and study guide based on a file and other features.