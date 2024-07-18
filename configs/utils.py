from importlib import import_module
from flask_smorest import Api


def register_models(installed_apps):
    """
    This function imports all the models from the installed apps.
    """
    for module_name in installed_apps:
        try:
            import_module(f"{module_name}.models")
        except ImportError as e:
            print(f"Error importing {module_name}.models: {e}")


def register_blueprints(api, apps_list):
    for module_name in apps_list:
        module = import_module("{}.routes".format(module_name))
        getattr(module, "blueprints", None)
        if getattr(module, "blueprints", None):
            for blueprint in module.blueprints:
                api.register_blueprint(blueprint)


def configure_database(app, db):
    with app.app_context():
        try:
            from sqlalchemy import text

            # check db connection
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            print("Database Connection error: ", e)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()
