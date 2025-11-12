import pandas as pd
import pandasai as pai
from pandasai_litellm import LiteLLM
from pandasai import smart_dataframe as sdf
from canvasapi import Canvas
from canvasapi.exceptions import Unauthorized, Forbidden, CanvasException
from prompt_toolkit.shortcuts import ProgressBar
import os
def assignments(courses):
    #pull grades from canvasapi
    course_assignments = []
    all_courses = []
    for course in courses:
        course_assignments = course.get_assignments(include=['rubric_settings', 'submission'])
        all_courses.append(course_assignments)
  
    '''
    for course in all_courses:
        for i in course:
            print(i.name)
    '''
    return all_courses
def dictionize_assignment(course ,assignment):
    graded = False
    score = "Ungraded"
    rubric_id = "None"
    rubric = "No Rubric"
    if hasattr(assignment, 'submission'):
        sub = assignment.submission
        if sub.get('workflow_state') == 'graded':
            score = sub.get('score')
            graded = True
    if hasattr(assignment, 'rubric_settings'):
        try:
            rubric_id = assignment.rubric_settings.get('id')
            if rubric_id:
                rubric_obj = course.get_rubric(rubric_id)
                rubric_list = []
                for fields in rubric_obj.criteria:
                    desc = fields.get('description', 'No Description')
                    points = fields.get('points', 0)
                    rubric_list.append(f".Desc: {desc}, points: {points}")
                rubric = "\n".join(rubric_list)
        except:
            pass
    dict_assignment = {
        'id': assignment.id,
        'name': assignment.name,
        'url': assignment.html_url,
        'prob_description': assignment.description,
        'max_points': assignment.points_possible,
        'due_date': assignment.due_at,
        'late_end_date': assignment.lock_at,
        'type': assignment.grading_type,
        'sub_type': ", ".join(assignment.submission_types),
        'timezone': "UTC",
        'score': score,
        'grade_state': graded,
        'rubric_exists': rubric_id,
        'rubric': rubric,
        'in_final_grade_calc': assignment.omit_from_final_grade
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
'''    
    from datetime import datetime, timezone

    def parse_due_at(iso):
        if not iso:
            return None
        try:
            return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)
        except Exception:
            return None
        
    upcoming_assignments(all_course_pages, days_ahead=7):
    import pandas as pd
    rows =[]
    for page in all_course_pages:
        if not page:
            continue
        for a in page:
            rows.append({
                "name": a.name,
                "url" : getattr(a, "html_url", None),
                "due at": getattr(a, "due at", None),
                "published": getattr(a, "published", None)
                
            )}
            df = pd.DataFrame(row)
            if df.empty:
                print("No assignments found.")
                return
            df["due_dt"]= df["due_at"].apply(parse_due_at)
            now = datetime.now(timezone.utc)
            horizon = now + pd.Timedelta(days=days_ahead)
            soon = df[(df["due_dt"].notna()) & (df["due_dt"] <= horizon)]
            print(f"\n== Upcoming Assignments (next {days_ahead} days) ===")
            print(soon [["name", "due_at", "url"]].sort_values("due at").to_string(index=False))

            upcoming_assignments(asmn_list, days_ahead=7)

horizon = now + pd.            
            
    df = pd.DataFrame(rows)

    def compare_to_rubric(submission_text: str, rubric_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Function to compare submission text to rubric items
        use_gemini: bool = False, gemin_key: str = None) -> Dict[str, Any]:

    results = []
    for item in rubric_items or []:
        desc = item.get("description", "") if isinstance(item, dict) else str(item)
        pts = item.get("points", 0) if isinstance(item, dict) else 0
        score_pct, evidence = simple_text_scores(submision_text, desc)
        results.append({
            "rubric_description": desc,
            "rubric_points": pts,
            "score_percentage": score_pct,
            "evidence": evidence,
            "note":"" # Placeholder for additional notes
        })
'''
if __name__ == "__main__":
    #Set up canvas object
    CANVAS_URL = "https://unt.instructure.com/"
    CANVAS_API = os.environ.get("CANVAS_API_KEY")
    GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
    asng_dictions = []
    course_dictions = []
    course_names = []
    if not CANVAS_API and GEMINI_KEY:
        SystemExit("ERROR: Ensure Canvas and GEMINI API keys are stored in system variables as CANVAS_API_KEY and GEMINI_API_KEY")

    try:
        user_canvas = Canvas(CANVAS_URL, CANVAS_API)
        user = user_canvas.get_current_user()
    except (Unauthorized, Forbidden, CanvasException) as e:
        print("Canvas authorization failed:", str(e))
        raise SystemExit("Check CANVAS_API_KEY yenviromental variable.")
    else:

        courses = user.get_courses(enrollment_status='active')
        all_courses = allowed_courses(courses)
        for course in all_courses:
            course_names.append(course.name)
        asmn_list = assignments(all_courses)
        i = 0
        for course in asmn_list:
            for assingment in course:
                asng_dictions.append(dictionize_assignment(all_courses[i], assingment))
            course_dictions.append(asng_dictions)
            i += 1
            asng_dictions.clear()

        #graded = grades(data)
    #inspect_paginated_list(data)
    data = {
        'courses': course_names,
        'course Assignments': course
    }
    
    dataframe = pd.DataFrame(data)

    userName = input("Please enter your name: ")
    llm = LiteLLM(model="gemini-2.5-flash", gemini_api = GEMINI_KEY)

    ai_dataframe = sdf.SmartDataframe(dataframe)
    pai.config.llm = llm
    pai.config.temperature = 40
    pai.config.seed = 26


    while True:
        prompt = ai_dataframe.chat(f"Hello {userName}, how may I help you?: ")
        print(prompt)
    
        
        
        