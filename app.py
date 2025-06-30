from flask import Flask, render_template, request, redirect
from models import db, Job
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    selected_date = request.args.get('date')
    if selected_date:
        date_obj = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()
        jobs = Job.query.filter_by(date=date_obj).all()
    else:
        jobs = Job.query.all()
    return render_template('index.html', jobs=jobs, selected_date=selected_date)

@app.route('/new', methods=['GET', 'POST'])
def new_job():
    if request.method == 'POST':
        description = request.form['description']
        driver = request.form['driver']
        truck_number = request.form['truck_number']
        status = request.form['status']
        notes = request.form['notes']
        date_str = request.form['date']
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.date.today()
        
        new_job = Job(description=description, driver=driver,
                      truck_number=truck_number, status=status, notes=notes, date=date_obj)
        db.session.add(new_job)
        db.session.commit()
        return redirect('/')
    return render_template('new_job.html')

@app.route('/update_status/<int:job_id>', methods=['POST'])
def update_status(job_id):
    job = Job.query.get_or_404(job_id)
    job.status = request.form['status']
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        job.description = request.form['description']
        job.driver = request.form['driver']
        job.truck_number = request.form['truck_number']
        job.status = request.form['status']
        job.notes = request.form['notes']
        date_str = request.form['date']
        job.date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.date.today()
        db.session.commit()
        return redirect('/')
    return render_template('edit_job.html', job=job)

if __name__ == '__main__':
    app.run()
