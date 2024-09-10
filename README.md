<h1 align="center" id="title">Pastebin</h1>

<p align="center"><img src="https://github.com/user-attachments/assets/b4e0a756-3835-4971-8c2e-12393a239945" width="160" height="170" alt="project-image"></p>

<p id="description">Pastebin is a Django-based web application that allows users to create view and manage text snippets. Users can register log in log out and create text snippets which are stored in Amazon S3. The application features session-based authorization snippet likes and view counts. It is hosted on an EC2 instance with a load balancer and uses Redis for caching popular snippets.</p>

<h2>Project Screenshots:</h2>

![image](https://github.com/user-attachments/assets/f1015c73-0b6d-442d-aee5-daf057ff635e)

![image](https://github.com/user-attachments/assets/4e910b23-8cf2-42a5-9e51-7a9ffaa1b344)

![image](https://github.com/user-attachments/assets/c20931eb-547d-4eb1-abde-b8a0af36c3d3)

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   User Management: Register log in and log out.
*   Snippet Management: Create view and like text snippets.
*   Dynamic Views: Display snippets with sorting options (by time popularity and alphabet).
*   Caching: Utilize Redis to cache popular snippets for improved performance.
*   Amazon S3 Integration: Store text snippets in Amazon S3.
*   Elastic Load Balancing: Use an Amazon ELB load balancer for scalability.

<h2>🛠️ Installation Steps:</h2>

<p>1. Prerequisites:</p>

```
- Python 3.x - Django 4.2.11 - PostgreSQL - Redis - Amazon S3 account
```

<p>2. Setup:</p>

```
https://github.com/4rsa/Pastebin.git    cd Pastebin
```

<p>3. Create a Virtual Environment:</p>

```
python -m venv venv   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

<p>4. Install Dependencies:</p>

```
pip install -r requirements.txt
```

<p>5. Configure Environment Variables:</p>

```
DEBUG=True SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/yourdatabase
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
REDIS_URL=redis://localhost:6379/1
```

<p>6. Run Migrations:</p>

```
python manage.py migrate
```

<p>7. Run the Development Server:</p>

```
python3 mange.py runserver
```

### Usage

**Access the Application:**

Open your browser and navigate to `http://127.0.0.1:8000/`.

**User Registration and Login:**

Use the registration and login forms to create an account or log in.

**Create Snippets:**

Once logged in, you can create text snippets from the `create_snippet` page.

**View and Like Snippets:**

Browse snippets on the `all_snippets` page. You can like snippets and view them in detail.

### API Endpoints

- `GET /snippets/`: List all snippets.
- `POST /snippets/`: Create a new snippet.
- `GET /snippets/{id}/`: Retrieve a specific snippet.
- `PUT /snippets/{id}/`: Update a snippet.
- `DELETE /snippets/{id}/`: Delete a snippet.
- `POST /snippets/{id}/like/`: Like a snippet.

### Contributing

If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments

- Django
- Redis
- Amazon S3
- EC2
- AWS Elastic Load Balancer
- Kotlin
