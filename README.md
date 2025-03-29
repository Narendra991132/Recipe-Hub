# Recipe Hub - Cloud-Based Recipe Management System

Recipe Hub is a cloud-based recipe management system built with Django that allows users to store, organize, and share their favorite recipes. The application is deployed on AWS Elastic Beanstalk and includes a complete CI/CD pipeline for continuous integration and deployment.

## Features

- **User Authentication**: Register, login, and manage user profiles
- **Recipe Management**: Full CRUD operations for recipes
- **Category Organization**: Group recipes by categories
- **User Permissions**: Users can only edit/delete their own recipes
- **Responsive Design**: Works on all devices (desktop, tablet, mobile)
- **Search & Filter**: Find recipes by name, category, or ingredients
- **Cloud Storage**: All data securely stored in the cloud

## Technology Stack

- **Backend**: Python 3.12, Django 5.1
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production)
- **Deployment**: AWS Elastic Beanstalk
- **CI/CD**: AWS CodePipeline, AWS CodeBuild
- **Code Quality**: Pytest, Pylint, SonarQube
- **Version Control**: Git, GitHub

## Installation and Setup

### Prerequisites

- Python 3.12 or later
- pip
- Git

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/Narendra991132/Recipe-Hub.git
cd recipe-hub
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsu
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## Testing

The application includes comprehensive testing for both the recipes and accounts apps:

```bash
# Run all tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=recipes --cov=accounts --cov-report=html
```

View the coverage report in the `htmlcov` directory.

## CI/CD Pipeline

The application uses AWS services for CI/CD:

1. **Source Control**: Code changes are pushed to a private GitHub repository
2. **Code Build**: AWS CodeBuild runs tests, static code analysis, and security checks
3. **Deployment**: AWS Elastic Beanstalk deploys the application

## Code Quality & Security

Code quality is maintained through:

- **Pytest**: For unit and integration testing
- **Pylint**: For static code analysis
- **SonarQube**: For code quality and security vulnerability analysis

## AWS Deployment

To deploy to AWS Elastic Beanstalk:

1. Install the EB CLI:
```bash
pip install awsebcli
```

2. Initialize EB:
```bash
eb init -p python-3.12 recipe-management
```

3. Create an environment:
```bash
eb create recipe-management-prod
```

4. Deploy changes:
```bash
eb deploy
```
AWS link : recipeshubapp-env.eba-pw28fxmm.us-west-2.elasticbeanstalk.com/


## User Roles and Permissions

- **Regular Users**: Can create, view, edit, and delete their own recipes and categories
- **Admin Users**: Have full access to all recipes and categories

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Bootstrap for the responsive design framework
- Django for the powerful Python web framework
- AWS for cloud hosting and CI/CD services
