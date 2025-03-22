from news import app
from news import views, admins

if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.160', port=8000)
