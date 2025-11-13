import pandasai as pai
import pandas as pd
from pandasai_litellm.litellm import LiteLLM
from canvasapi import Canvas
from pptx import Presentation
from docx import Document
from canvasapi.exceptions import Unauthorized, Forbidden, CanvasException
from prompt_toolkit.shortcuts import ProgressBar
import os, io
def assignments(courses):
    #pull grades from canvasapi
    course_assignments = []
    all_courses = []
    for course in courses:
        course_assignments = course.get_assignments(include=['rubric', 'rubric_settings', 'submission'])
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
                rubric_list = []
                for fields in assignment.rubric:
                    desc = fields.get('description', 'No Description')
                    points = fields.get('points', 0)
                    rubric_list.append(f".Desc: {desc}, points: {points}")
                rubric = "\n".join(rubric_list)
        except Exception as e:
            print(e)
            pass
    course_name = course.name
    dict_assignment = {
        'course': course_name,
        'id': str(getattr(assignment, "id", None)),
        'name': getattr(assignment, "name", None),
        'url': getattr(assignment, "html_url", None),
        'prob_description': getattr(assignment, "description", None),
        'max_points': str(getattr(assignment, "points_possible", None)),
        'due_date': getattr(assignment, "due_at", None),
        'late_end_date': getattr(assignment, "lock_at", None),
        'type': getattr(assignment, "grading_type", None),
        'sub_type': ", ".join(getattr(assignment, "grading_type", None)),
        'timezone': "UTC",
        'score': str(score),
        'grade_state': graded,
        'rubric_exists': str(rubric_id),
        'rubric': rubric,
    }
    return dict_assignment
def bytes_powerpoint(bytes):
    slides = []
    texts = []
    pres = Presentation(io.BytesIO(bytes))
    number = 1
    for slide in pres.slides:
        for shape in slide.shapes:
            if hasattr(shape, 'text'):
                text = shape.text.strip()
                texts.append(text)
        slide_txt = "\n".join(texts).strip()
        slides.append({
            'slide_number': number, 
            'text': slide_txt    
                       })
        number += 1
        texts.clear()
    return slides
def bytes_docx(bytes):
    tot_doc = []
    try:
        doc = Document(io.BytesIO(bytes))
        number = 1
        for paragraph in doc.paragraphs:
            sentances = paragraph.text.strip().split(".")
            
            for sentance in sentances:
                tot_doc.append({'sentance_number': number, 'sentance_text': sentance})
                number += 1
    except Exception as e:
        print(f"Error in byte_docx {e}")
    return tot_doc

def dictionize_files(course, course_file):
        contents = "Download failed"
        filename = "Unaccessable"
        type = "None"
        content_string = "No Content"
        content_list = []
        try:
            contents = course_file.get_contents(binary=True)
            type = course_file.content_type
        except:

            pass
        filename = course_file.display_name
        try: 
            if (str(filename)).lower().endswith(".pptx"):
                slides = bytes_powerpoint(contents)
                if slides:
                    for slide in slides:
                        content_list.append({'file_name': filename, 'file type': type, 'slide_number': str(slide['slide_number']), 'slide_text': str(slide['text'])})
                    return content_list, "Powerpoint"
            elif (str(filename)).lower().endswith((".docx", ".doc")):
                sentances = bytes_docx(contents)
                if sentances:
                    for sentance in sentances:
                        content_list.append({'file_name': filename, 'file type': type, 'paragraph_number': str(sentance['sentance_number']), 'sentance_text': str(sentance['sentance_text'])})
                    return content_list, "Docx"
            else:
                    file_dic = {
                        'course_name': getattr(course, "name", None),
                        'filename': getattr(course_file, "display_name", None),
                        'type': getattr(course_file, "content_type", None),
                        'file_content': contents,
                    }
                    return file_dic, "Other"
        except Exception as e:
            print(e)
            return [], "Failure"

def allowed_courses(courses):
    all_courses = []
    for course in courses:
        try:
            name = course.name
            assignments = course.get_assignments()
            #print(f"Name: {name}\n")
            #if name != "no-name":
            all_courses.append(course)

        except:
            #print("exception\n")
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
    pptx_files = []
    docx_files = []
    other_files = []
    course_dicts = []
    allowed_class = []
    allowed_files =[]
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
            try:
                folders = list(course.get_folders())
            except:
                continue
            for folder in folders:
                if getattr(folder, 'hidden', False):
                    continue
                try:
                    files = list(folder.get_files())
                except:
                    continue
                for file in files:
                    if getattr(file, 'hidden_for_user', False) or getattr(file, 'locked', False):
                        continue    
                    file_contents, type = dictionize_files(course, file)
                    if file_contents:
                        if type == "Powerpoint":
                            pptx_files += file_contents
                        elif type == "Docx":
                            docx_files += file_contents
                        elif type == "Other":
                            other_files.append(file_contents)
                        else:
                            continue
        
        asmn_list = assignments(all_courses)
        course_objs = all_courses.copy()

        i = 0
        for course in asmn_list:
            for assingment in course:
                asng_dictions.append(dictionize_assignment(course_objs[i], assingment))
            i += 1
    '''
    print("Debug")
    print("files:")
    for file in course_files:
        print(file)
        '''
        #graded = grades(data)
    #inspect_paginated_list(data)
    userName = input("Please enter your name: ")
    user_data = {
        'users_name': userName,
        'courses': course_names,
        'quit_instructions': "Type Quit to exit program"
    }


    from pandasai import SmartDataframe
    from pandasai.config import Config
    from pandasai_litellm.litellm import LiteLLM

    llm = LiteLLM(model="gemini/gemini-2.5-flash", provider="google_ai_studio", api_key=GEMINI_KEY)
    config = Config(
        llm=llm,
        temperature=0.4,
        seed=26
    )
    assingment_data = pd.DataFrame(asng_dictions)
    user_info = pd.DataFrame(user_data)
    pptx_frame = pd.DataFrame(pptx_files)
    docx_frame = pd.DataFrame(docx_files)
    other_frame = pd.DataFrame(other_files)
    ai_frame = pd.concat([user_info, pptx_frame, docx_frame, other_frame, assingment_data], ignore_index=True)

    dataframe = SmartDataframe(ai_frame, config=config)
    userinput = input("How may I help you: ")
    while userinput != "quit" and userinput != "Quit":
        try:
            prompt = dataframe.chat(userinput)
            print(prompt)
        except:
            print("AI model currently unavailable ")
        userinput = input("How may I help you: ")
            
    
        
        
        