import pandasai as pai
from pandasai_litellm import LiteLLM
from canvasapi import Canvas
import os
def assignments():
    #pull assignments from canvasapi
    return

if __name__ == "__main__":
    #Set up canvas object
    CANVAS_URL = "https://unt.instructure.com/"
    CANVAS_API = os.environ.get("CANVAS_API_KEY")
    user_canvas = Canvas(CANVAS_URL, CANVAS_API)
    user = user_canvas.get_current_user()
    data = user.get_courses()
    userList = list(data)


    userName = input("Please enter your name: ")
    llm = LiteLLM(model="gemini-2.5-flash", gemini_api = os.environ.get("GEMINI_API_KEY"))
    pai.config.llm = llm
    pai.config.temperature = 40
    pai.config.seed = 26

    while True:
        prompt = input(f"Hello {userName}, how may I help you?: ")
        
        
        