import uvicorn
import webbrowser
"""
DCM app server
Document control manager
"""

from app.main import app 

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    webbrowser.open_new(url='http://localhost:8000')
    uvicorn.run(app)