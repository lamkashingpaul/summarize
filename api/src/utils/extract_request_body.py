import json

from starlette.requests import Request


async def extract_request_body(request: Request) -> tuple[dict, str]:
    try:
        content_type = request.headers.get("content-type", "")
        if "application/json" not in content_type:
            return {}, ""

        request_body = await request.body()
        request_body = json.loads(request_body.decode("utf-8"))
        return request_body, ""

    except json.JSONDecodeError:
        return {}, "Invalid JSON body"
    except Exception as e:
        return {}, f"Error extracting request body: {str(e)}"
