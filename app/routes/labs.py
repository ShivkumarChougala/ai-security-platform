from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.trace_service import save_lab_attempt
from app.services.explanation_service import generate_sqli_explanation

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/labs/sqli-login", response_class=HTMLResponse)
def sqli_login_page(request: Request, db: Session = Depends(get_db)):
    attempts = db.execute(
        text("""
            SELECT
                id,
                lab_name,
                username_input,
                password_input,
                generated_query,
                success,
                vulnerability_type,
                created_at
            FROM lab_attempts
            WHERE lab_name = 'sqli_login'
            ORDER BY id DESC
            LIMIT 5
        """)
    ).fetchall()

    return templates.TemplateResponse(
        "labs/sqli_login.html",
        {
            "request": request,
            "submitted": False,
            "attempts": attempts
        }
    )


@router.post("/labs/sqli-login", response_class=HTMLResponse)
def sqli_login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    query = f"SELECT * FROM lab_users WHERE username='{username}' AND password='{password}';"

    success = False
    query_error = None

    try:
        result = db.execute(text(query))
        row = result.first()
        success = row is not None
    except Exception as e:
        query_error = str(e)

    vulnerability_type = "sql_injection" if any(
        x in password.lower() for x in ["'", "--", " or ", '"']
    ) else "none"

    explanation = generate_sqli_explanation(
        username=username,
        password=password,
        query=query,
        success=success,
        vulnerability_type=vulnerability_type,
        query_error=query_error
    )

    save_lab_attempt(
        db=db,
        lab_name="sqli_login",
        username_input=username,
        password_input=password,
        generated_query=query,
        success=success,
        vulnerability_type=vulnerability_type
    )

    attempts = db.execute(
        text("""
            SELECT
                id,
                lab_name,
                username_input,
                password_input,
                generated_query,
                success,
                vulnerability_type,
                created_at
            FROM lab_attempts
            WHERE lab_name = 'sqli_login'
            ORDER BY id DESC
            LIMIT 5
        """)
    ).fetchall()

    return templates.TemplateResponse(
        "labs/sqli_login.html",
        {
            "request": request,
            "submitted": True,
            "username": username,
            "password": password,
            "query": query,
            "success": success,
            "query_error": query_error,
            "vulnerability_type": vulnerability_type,
            "attempts": attempts,
            "explanation": explanation
        }
    )
