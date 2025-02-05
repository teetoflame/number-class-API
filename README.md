# Number Classification API

This API classifies a given number based on various mathematical properties and provides a fun fact about the number using an external Numbers API.

## Installation and Setup

### 1. Set Up Virtual Environment

1. SSH into your EC2 instance.

2. Install `python3` and `pip3` if not already installed:

    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
    ```

3. Install `virtualenv` if it's not already installed:

    ```bash
    sudo pip3 install virtualenv
    ```

4. Navigate to your project directory:

    ```bash
    cd /path/to/your/project
    ```

5. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

6. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

### 2. Install Dependencies

Once the virtual environment is activated, install the necessary dependencies for the project:

```bash
pip install -r requirements.txt
```

Make sure that the `requirements.txt` file includes:

```
fastapi
uvicorn
requests
```

You can generate the `requirements.txt` using:

```bash
pip freeze > requirements.txt
```

### 3. Run the Application

After installing the dependencies, you can run the application using `uvicorn`:

```bash
nohup uvicorn app:app --host 0.0.0.0 --port 8000 &
```

This will start the FastAPI application on port `8000` and make it accessible on your EC2 instance.

---

## API Documentation

### Endpoint: Classify Number

**GET** `/api/classify-number`

This endpoint classifies a given number based on various mathematical properties and provides a fun fact about it.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| number    | int  | ✅ Yes   | The number to classify |

#### 📌 Example Request:

```
GET /api/classify-number?number=42
```

---

### Response Format

#### Success Response (200 OK)

If a valid number is provided, the API returns an object with the number's properties.

##### ✅ Example Response:

```json
{
  "number": 42,
  "is_prime": false,
  "is_perfect": false,
  "properties": ["even"],
  "digit_sum": 6,
  "fun_fact": "42 is the answer to the ultimate question of life, the universe, and everything."
}
```

### Response Fields

| Field         | Type   | Description                                                                 |
|---------------|--------|-----------------------------------------------------------------------------|
| number        | int    | The number provided in the request                                           |
| is_prime      | boolean| Whether the number is prime (true or false)                                  |
| is_perfect    | boolean| Whether the number is a perfect number (true or false)                       |
| properties    | array  | List of mathematical properties (e.g., "odd", "even", "armstrong")          |
| digit_sum     | int    | Sum of the digits of the number                                             |
| fun_fact      | string | A fun fact about the number from the Numbers API                            |

---

### Error Responses

- **400 Bad Request – Missing or Invalid Number**

  ❌ Example Response (Missing Number):

  ```json
  {
    "error": "Number is required"
  }
  ```

  Occurs if the `number` parameter is missing.

  ❌ Example Response (Invalid Input):

  ```json
  {
    "error": true,
    "number": "alphabet"
  }
  ```

  Occurs if the provided value is not a valid number (e.g., "abc" instead of 42).

- **500 Internal Server Error**

  ❌ Example Response:

  ```json
  {
    "error": "Internal Server Error"
  }
  ```

  Occurs if there is an unexpected issue with the server or external API.

---

## How to Use

### With cURL

```bash
curl -X GET "http://<your-ec2-ip>:8000/api/classify-number?number=42"
```

### With JavaScript (Axios)

```javascript
import axios from "axios";

axios
  .get("http://<your-ec2-ip>:8000/api/classify-number?number=42")
  .then((response) => console.log(response.data))
  .catch((error) => console.error(error.response.data));
```

---

## Notes

- This API relies on an external Numbers API [http://numbersapi.com](http://numbersapi.com).
- Ensure your EC2 instance has internet access.
- If the Numbers API is down, the response may not include a fun fact.

---

## License

This project is licensed under the MIT License.

```

