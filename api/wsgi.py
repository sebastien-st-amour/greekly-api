from greekly import create_app
from dotenv import load_dotenv
from os import getenv

load_dotenv()

config = getenv('GREEKLY_APP_CONFIG')
app = create_app(config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)