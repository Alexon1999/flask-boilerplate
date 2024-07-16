from configs import create_app
from configs.settings import config_dict
import environ

env = environ.Env()

config_name = env("CONFIG_MODE", default="development")
app_config = config_dict[config_name]

app = create_app(name="FlaskAPP", config=app_config)

if __name__ == "__main__":
    app.run(port=8000)
