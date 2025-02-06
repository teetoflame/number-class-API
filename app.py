from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Union
import requests
import math

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Helper functions
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
        response = requests.get(f"http://numbersapi.com/{n}/math", timeout=5)
        return response.text
    except requests.RequestException:
        return f"{n} is a number"

# Main route to classify number
@app.get("/classify-number")
async def classify_number(number: int = Query(..., description="The number to classify")) -> Dict[str, Union[int, bool, List[str], str]]:
    """Classify a number and return its properties."""
    # Validate if the number is negative
    if number < 0:
        raise HTTPException(status_code=400, detail="Number must be non-negative")

    # Get properties and calculations
    properties = get_properties(number)
    fun_fact = await get_fun_fact(number)

    # Return the classification
    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": get_digit_sum(number),
        "fun_fact": fun_fact
    }

# Error handling for invalid input
@app.get("/api/classify-number")
async def classify_number_with_string(number: str) -> Dict[str, Union[int, bool, List[str], str]]:
    """Classify a number and handle invalid inputs."""
    try:
        num = int(number)
    except ValueError:
        raise HTTPException(status_code=400, detail="Number must be numeric")
    
    if num < 0:
        raise HTTPException(status_code=400, detail="Number must be non-negative")
    
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
