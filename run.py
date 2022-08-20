import uvicorn
"""
DCM app server
Document control manager
"""

from app.main import app 

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    uvicorn.run(app)