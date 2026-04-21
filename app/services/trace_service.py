from sqlalchemy import text
from sqlalchemy.orm import Session


def save_lab_attempt(
    db: Session,
    lab_name: str,
    username_input: str,
    password_input: str,
    generated_query: str,
    success: bool,
    vulnerability_type: str
):
    db.execute(
        text("""
            INSERT INTO lab_attempts (
                lab_name,
                username_input,
                password_input,
                generated_query,
                success,
                vulnerability_type
            )
            VALUES (
                :lab_name,
                :username_input,
                :password_input,
                :generated_query,
                :success,
                :vulnerability_type
            )
        """),
        {
            "lab_name": lab_name,
            "username_input": username_input,
            "password_input": password_input,
            "generated_query": generated_query,
            "success": success,
            "vulnerability_type": vulnerability_type
        }
    )
    db.commit()
