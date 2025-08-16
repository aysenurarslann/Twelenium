# prompt_safety.py
def validate_search_query(query: str) -> bool:
    """
    Validates user search queries to prevent malicious or unsafe inputs.
    """
    blocked_keywords = ["admin", "password", "root", "sudo", "delete", "hack", "malware", "phishing"]
    
    for word in blocked_keywords:
        if word.lower() in query.lower():
            raise ValueError(f"Blocked keyword detected: '{word}'")
    
    # Prevent overly long queries (avoid system overload)
    if len(query.split()) > 50:
        raise ValueError("Query too long — may cause performance issues.")
    
    return True
