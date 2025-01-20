from flask import Flask
#from views import views
import views

import time

from apscheduler.schedulers.background import BackgroundScheduler


def schedule_run():
    data = views.mainProcess()   
    # views.pdfProcess()
    print("Executed: "+str(time.strftime("%A, %d. %B %Y %I:%M:%S %p")))
    
#Scheduler    
sched = BackgroundScheduler(daemon=True)
sched.add_job(schedule_run,'interval',seconds=10)
sched.start()   
app = Flask(__name__)

    
#app.register_blueprint(views,url_prefix="/")

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)
    #app.run(debug=True,port=8000)