import pandas as pd
import pandasai as pai
from pandasai_litellm import LiteLLM
from pandasai import smart_dataframe as sdf
from canvasapi import Canvas
from canvasapi.exceptions import Unauthorized, Forbidden, CanvasException
import os, csv, json, itertools
def assignments(courses):
    #pull grades from canvasapi
    course_assignments = []
    all_courses = [[]]
    for course in courses:
        course_assignments = course.get_assignments(include=['rubric_settings', 'submission'])
        all_courses.append(course_assignments)
  
    for course in all_courses:
        for i in course:
            print(i.name)

    return all_courses
def dictionize_assignment(assignment):
    if hasattr(assignment, 'submission'):
        sub = assignment.submission
        if sub.get('workflow_state') == 'graded':
            score = sub.get('score')
            graded = True
        else:
            graded = False
    if hasattr(assignment, 'rubric_settings'):
        rubric = assignment.get

    dict_assignment = {
        'id': assignment.id,
        'name': assignment.name,
        'url': assignment.html_url,
        'prob_description': assignment.description,
        'score': score,
        'grade_state': graded,
        'rubric_exists': 
        'rubric': 

    }
def allowed_courses(courses):
    all_courses = []
    for course in courses:
        try:
            name = course.name
            assignments = course.get_assignments()
            print(f"Name: {name}\n")
            #if name != "no-name":
            all_courses.append(course)

        except:
            print("exception\n")
            pass    
    return all_courses
    

if __name__ == "__main__":
    #Set up canvas object
    CANVAS_URL = "https://unt.instructure.com/"
    CANVAS_API = os.environ.get("CANVAS_API_KEY")
    GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
    if not CANVAS_API and GEMINI_KEY:
        SystemExit("ERROR: Ensure Canvas and GEMINI API keys are stored in system variables as CANVAS_API_KEY and GEMINI_API_KEY")

    try:
        user_canvas = Canvas(CANVAS_URL, CANVAS_API)
        user = user_canvas.get_current_user()
    except (Unauthorized, Forbidden, CanvasException) as e:
        print("Canvas authorization failed:", str(e))
        raise SystemExit("Check CANVAS_API_KEY, CANVAS_URL and token permissions.")
    else:
        courses = user.get_courses(enrollment_status='active')
        all_courses = allowed_courses(courses)
        for i in all_courses:
            print(i.name, end='\n')
        assignments = assignments(all_courses)
        #graded = grades(data)
    #inspect_paginated_list(data)
    
    '''
    userList = list(data)
    graded = grades(data)
    dataframe = pd.DataFrame(graded)

    userName = input("Please enter your name: ")
    llm = LiteLLM(model="gemini-2.5-flash", gemini_api = GEMINI_KEY)

    ai_dataframe = sdf.SmartDataframe(dataframe)
    pai.config.llm = llm
    pai.config.temperature = 40
    pai.config.seed = 26


    while True:
        prompt = ai_dataframe.chat(f"Hello {userName}, how may I help you?: ")
        print(prompt)
    '''
        
        
        