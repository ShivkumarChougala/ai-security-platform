def generate_sqli_explanation(
    username: str,
    password: str,
    query: str,
    success: bool,
    vulnerability_type: str,
    query_error: str | None = None
):
    if query_error:
        return {
            "title": "SQL Query Error",
            "what_happened": (
                "The application tried to execute the SQL query, but the database returned an error."
            ),
            "why_it_worked": (
                "The input changed the query in a way that produced invalid SQL syntax or an unexpected database error."
            ),
            "impact": (
                "In insecure applications, SQL errors can leak useful information about the database structure to an attacker."
            ),
            "fix": (
                "Use parameterized queries and avoid building SQL statements with raw string concatenation."
            )
        }

    if vulnerability_type == "sql_injection" and success:
        return {
            "title": "SQL Injection Authentication Bypass",
            "what_happened": (
                f"The password input `{password}` changed the intended login query and allowed the application to return a valid user row."
            ),
            "why_it_worked": (
                "The injected condition `OR '1'='1'` is always true. "
                "Because the query was built using raw string concatenation, the database evaluated the injected logic as part of the SQL statement."
            ),
            "impact": (
                "This caused an authentication bypass. An attacker could log in without knowing the real password."
            ),
            "fix": (
                "Use parameterized queries or prepared statements. Never insert raw user input directly into SQL strings."
            )
        }

    if vulnerability_type == "sql_injection" and not success:
        return {
            "title": "Suspicious SQL Injection Attempt",
            "what_happened": (
                "The input looked like a SQL injection payload, but this particular attempt did not produce a successful login."
            ),
            "why_it_worked": (
                "The payload contains SQL control characters or logic patterns, but the final query did not return a matching row in this case."
            ),
            "impact": (
                "Even though this attempt failed, the application is still unsafe because it builds SQL queries directly from user input."
            ),
            "fix": (
                "Use parameterized queries and validate input where appropriate."
            )
        }

    if not success:
        return {
            "title": "Normal Login Failure",
            "what_happened": (
                "The application ran the SQL query using the provided username and password, but no matching user was found."
            ),
            "why_it_worked": (
                f"The query checked for a row matching username `{username}` and password `{password}`. "
                "Since no such row existed, authentication failed."
            ),
            "impact": (
                "There is no authentication bypass in this specific attempt."
            ),
            "fix": (
                "The application should still use parameterized queries to stay secure, even when the login fails normally."
            )
        }

    return {
        "title": "Normal Login Success",
        "what_happened": (
            "The application found a matching username and password in the database."
        ),
        "why_it_worked": (
            f"The query matched a stored row for username `{username}` and the provided password."
        ),
        "impact": (
            "This is the expected behavior for a valid login attempt."
        ),
        "fix": (
            "Even valid logins should use parameterized queries to prevent injection attacks."
        )
    }
