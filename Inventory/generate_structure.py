import os

# Define the folder and file structure
structure = {
    "it_asset_portal": [
        "run.py",
        "config.py",
        "requirements.txt",
        "README.md",
        {
            "database": [
                "it_assets.db",
                ".gitignore"
            ]
        },
        "migrations",  # folder
        {
            "app": [
                "__init__.py",
                {
                    "models": [
                        "__init__.py",
                        "asset.py",
                        "user.py",
                        "lifecycle.py",
                        "transaction.py"
                    ]
                },
                {
                    "routes": [
                        "__init__.py",
                        "auth_routes.py",
                        "dashboard_routes.py",
                        "asset_routes.py",
                        "report_routes.py",
                        "user_routes.py"
                    ]
                },
                {
                    "templates": [
                        "base.html",
                        "login.html",
                        "dashboard.html",
                        {
                            "assets": [
                                "add_asset.html",
                                "view_asset.html",
                                "edit_asset.html",
                                "assign_asset.html"
                            ]
                        },
                        {
                            "users": [
                                "list_users.html",
                                "add_user.html",
                                "edit_user.html"
                            ]
                        },
                        {
                            "reports": [
                                "report_dashboard.html",
                                "report_detail.html"
                            ]
                        },
                        {
                            "lifecycle": [
                                "asset_timeline.html",
                                "asset_status_log.html"
                            ]
                        }
                    ]
                },
                {
                    "static": [
                        {
                            "css": ["style.css"]
                        },
                        {
                            "js": ["form_validations.js"]
                        },
                        {
                            "images": ["logo.png"]
                        }
                    ]
                },
                {
                    "utils": [
                        "__init__.py",
                        "decorators.py",
                        "auth_helpers.py",
                        "export_excel.py",
                        "import_excel.py",
                        "report_builder.py",
                        "lifecycle_helper.py"
                    ]
                },
                {
                    "forms": [
                        "__init__.py",
                        "asset_forms.py",
                        "login_form.py",
                        "user_forms.py",
                        "report_filter_form.py"
                    ]
                }
            ]
        }
    ]
}

# Helper function to recursively create directories and files
def create_structure(base_path, items):
    for item in items:
        if isinstance(item, str):
            # It's a file or a directory
            if '.' in item:
                with open(os.path.join(base_path, item), 'w') as f:
                    pass  # Create an empty file
            else:
                os.makedirs(os.path.join(base_path, item), exist_ok=True)
        elif isinstance(item, dict):
            for folder, contents in item.items():
                folder_path = os.path.join(base_path, folder)
                os.makedirs(folder_path, exist_ok=True)
                create_structure(folder_path, contents)

# Create base structure
create_structure(".", structure["it_asset_portal"])

print("Folder structure created successfully.")
