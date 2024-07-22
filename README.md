# API Documentation

## Base URL
`your_base_url`

## Endpoints

### 1. Developed By
- **URL**: `/developedby/`
- **Method**: `GET`
- **Description**: Returns the `developedby.html` page.

#### Response
- **Status Code**: `200 OK`
- **Content**: Renders the `developedby.html` page.

---

### 2. Registration Page
- **URL**: `/registerPage/`
- **Method**: `GET`
- **Description**: Returns the `register.html` page.

#### Response
- **Status Code**: `200 OK`
- **Content**: Renders the `register.html` page.

---

### 3. Verification Page
- **URL**: `/verifyPage/`
- **Method**: `GET`
- **Description**: Returns the `verify.html` page.

#### Response
- **Status Code**: `200 OK`
- **Content**: Renders the `verify.html` page.

---

### 4. Register User
- **URL**: `/register/`
- **Method**: `GET`
- **Description**: Retrieves a list of users with their IDs and timestamps.

#### Response
- **Success Response**:
  - **Status Code**: `200 OK`
  - **Content**:
    ```json
    {
      "message": "Hello, world!",
      "data": [
        {
          "id": "user_id_1",
          "timestamp": "timestamp_1"
        },
        {
          "id": "user_id_2",
          "timestamp": "timestamp_2"
        }
      ]
    }
    ```

---

### 5. Register User
- **URL**: `/register/`
- **Method**: `POST`
- **Description**: Registers a new user with an image.

#### Request Body
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `id` (string): The unique ID of the user.
  - `image` (file): The image file associated with the user.

#### Response
- **Success Response**:
  - **Status Code**: `201 Created`
  - **Content**:
    ```json
    {
      "message": "Data inserted successfully"
    }
    ```
- **Error Responses**:
  - **Status Code**: `400 Bad Request`
    - **Content**:
      ```json
      {
        "error": "ID and image are required"
      }
      ```
  - **Status Code**: `409 Conflict`
    - **Content**:
      ```json
      {
        "error": "User already exists"
      }
      ```
  - **Status Code**: `500 Internal Server Error`
    - **Content**:
      ```json
      {
        "error": "Error details"
      }
      ```

---

### 6. Verify User
- **URL**: `/verify/`
- **Method**: `POST`
- **Description**: Verifies a user by recognizing their face in the uploaded image.

#### Request Body
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `image` (file): The image file to be verified.

#### Response
- **Success Response**:
  - **Status Code**: `200 OK`
  - **Content**:
    ```json
    {
      "message": "Image received successfully!",
      "recognition": "identity or 'Unknown'"
    }
    ```
- **Error Responses**:
  - **Status Code**: `400 Bad Request`
    - **Content**:
      ```json
      {
        "error": "Image is required"
      }
      ```
  - **Status Code**: `500 Internal Server Error`
    - **Content**:
      ```json
      {
        "error": "Error details",
        "recognition": "Unknown"
      }
      ```

---

### 7. Delete User
- **URL**: `/register/`
- **Method**: `DELETE`
- **Description**: Deletes a user and their associated image.

#### Request Body
- **Content-Type**: `application/json`
- **JSON Data**:
  - `id` (string): The unique ID of the user to be deleted.

#### Response
- **Success Response**:
  - **Status Code**: `204 No Content`
  - **Content**:
    ```json
    {
      "message": "Data deleted successfully",
      "files_deleted": ["list_of_deleted_files"]
    }
    ```
- **Error Responses**:
  - **Status Code**: `400 Bad Request`
    - **Content**:
      ```json
      {
        "error": "ID is required"
      }
      ```
  - **Status Code**: `404 Not Found`
    - **Content**:
      ```json
      {
        "error": "User not found"
      }
      ```
  - **Status Code**: `500 Internal Server Error`
    - **Content**:
      ```json
      {
        "error": "Error details"
      }
      ```

---

