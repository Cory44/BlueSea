"""WSGI entry point for running the BlueSea backend."""

from bluesea_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
