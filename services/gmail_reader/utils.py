def extract_email_body(msg_data):
    parts = msg_data.get("payload", {}).get("parts", [])
    for part in parts:
        if part.get("mimeType") == "text/plain" or part.get("mimeType") == "text/html":
            data = part.get("body", {}).get("data")
            if data:
                import base64
                result = base64.urlsafe_b64decode(data).decode("utf-8")
                return result
    return None


def get_header_value(headers, name):
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value")
    return None

