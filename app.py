from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import math
from typing import List, Dict, Union

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class CustomHTTPException(Exception):
    def __init__(self, status_code: int, content: dict):
        self.status_code = status_code
        self.content = content

@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(status_code=exc.status_code, content=exc.content)

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is perfect."""
    if n < 1:
        return False
    sum_divisors = sum(i for i in range(1, n) if n % i == 0)
    return sum_divisors == n

def is_armstrong(n: int) -> bool:
    """Check if a number is Armstrong."""
    num_str = str(abs(n))  # Use absolute value for Armstrong check
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == abs(n)

def get_digit_sum(n: int) -> int:
    """Calculate sum of digits."""
    return sum(int(digit) for digit in str(abs(n)))

def get_properties(n: int) -> List[str]:
    """Get list of number properties."""
    properties = []
    
    if is_armstrong(n):
        properties.append("armstrong")
    
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    return properties

async def get_fun_fact(n: int) -> str:
    """Get fun fact from Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math", timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        pass
    return f"{n} is a number."

@app.get("/api/classify-number", response_model=Dict[str, Union[int, float, bool, List[str], str]] )
async def classify_number(number: str):
    """Classify a number and return its properties."""
    try:
        num = float(number) if '.' in number else int(number)
    except ValueError:
        raise CustomHTTPException(status_code=400, content={"number": number, "error": True})
    
    properties = get_properties(int(num)) if num == int(num) else []
    fun_fact = await get_fun_fact(int(num)) if num == int(num) else "Fun facts are only available for integers."
    
    return {
        "number": num,
        "is_prime": is_prime(int(num)) if num == int(num) and num > 0 else False,
        "is_perfect": is_perfect(int(num)) if num == int(num) and num > 0 else False,
        "properties": properties,
        "digit_sum": get_digit_sum(int(num)),
        "fun_fact": fun_fact
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
