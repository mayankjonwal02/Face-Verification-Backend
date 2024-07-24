
### **API Documentation for `Facial Verification Backend`**

#### **1. Register User**
- **URL:** `/register/`
- **Method:** `POST`
- **Request Format:** `multipart/form-data`
- **Request Body:**
  - `id` (string): The user's ID. (Required)
  - `image` (file): The user's image file. (Required)

- **Response Body:**
  - **Success (201 Created):**
    ```json
    {
      "message": "Data inserted successfully"
    }
    ```
  - **Errors:**
    - **400 Bad Request:**
      ```json
      {
        "error": "ID and image are required"
      }
      ```
    - **409 Conflict:**
      ```json
      {
        "error": "User already exists"
      }
      ```
    - **500 Internal Server Error:**
      ```json
      {
        "error": "Error message describing the issue"
      }
      ```

#### **2. Verify User**
- **URL:** `/verify/`
- **Method:** `POST`
- **Request Format:** `multipart/form-data`
- **Request Body:**
  - `id` (string): The user's ID. (Required)
  - `image` (file): The image file to verify. (Required)

- **Response Body:**
  - **Success (200 OK):**
    ```json
    {
      "message": "Image received successfully!",
      "recognition": "Recognized User ID",
      "verified": true
    }
    ```
  - **Errors:**
    - **400 Bad Request:**
      ```json
      {
        "error": "Image and ID are required",
        "verified": false
      }
      ```
      ```json
      {
        "error": "Invalid User",
        "verified": false
      }
      ```
    - **500 Internal Server Error:**
      ```json
      {
        "error": "Error message describing the issue",
        "verified": false
      }
      ```

#### **3. Delete User**
- **URL:** `/register/`
- **Method:** `DELETE`
- **Request Format:** `multipart/form-data`
- **Request Body:**
  - `id` (string): The user's ID. (Required)

- **Response Body:**
  - **Success (204 No Content):**
    ```json
    {
      "message": "Data deleted successfully",
      "files_deleted": ["list_of_deleted_files"]
    }
    ```
  - **Errors:**
    - **400 Bad Request:**
      ```json
      {
        "error": "ID is required"
      }
      ```
    - **404 Not Found:**
      ```json
      {
        "error": "User not found"
      }
      ```


---

### **Additional Information**

#### **Models**

- **User Model:**
  - `id` (string): User ID (Primary Key)
  - `timestamp` (datetime): Timestamp of registration



---

