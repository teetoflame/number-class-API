from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
    num_str = str(n)
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == n

def get_digit_sum(n: int) -> int:
    """Calculate sum of digits."""
    return sum(int(digit) for digit in str(n))

def get_properties(n: int) -> List[str]:
    """Get list of number properties."""
    properties = []
    
    # Check Armstrong
    if is_armstrong(n):
        properties.append("armstrong")
    
    # Check odd/even
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    return properties

async def get_fun_fact(n: int) -> str:
    """Get fun fact from Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        return response.text
    except:
        return f"{n} is a number"

@app.get("/")
async def read_root():
    """Root endpoint."""
    return {"message": "Welcome to the Number Classification API!"}

@app.get("/api/classify-number")
async def classify_number(number: str) -> Dict[str, Union[int, bool, List[str], str]]:
    """Classify a number and return its properties."""
    try:
        num = int(number)
    except ValueError:
        return {"number": number, "error": True}
    
    properties = get_properties(num)
    fun_fact = await get_fun_fact(num)
    
    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": get_digit_sum(num),
        "fun_fact": fun_fact
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
