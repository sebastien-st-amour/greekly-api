from greekly import create_app
from dotenv import load_dotenv
from os import getenv

load_dotenv()

config = getenv('GREEKLY_APP_CONFIG')
app = create_app(config)

if __name__ == '__main__':
    app.run(port=5000)