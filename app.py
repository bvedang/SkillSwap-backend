from rtcapp import app
from rtcapp.apis.routes import init_routes

init_routes()




if __name__ == "__main__":
    app.run(debug=True)