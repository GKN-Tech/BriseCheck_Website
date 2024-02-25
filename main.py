from website import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000)) 
    # environ to make it work for dynamically assigned ports on hosting platform
    app.run(debug=True, host='0.0.0.0', port=port)
    
