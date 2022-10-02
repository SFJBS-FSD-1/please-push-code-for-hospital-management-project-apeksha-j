from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import os

app = Flask(__name__)
# app.config.from_object(config_str)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:welcome$1234@localhost/hospitaldb'
db = SQLAlchemy(app)
# migrate = Migrate(app,db)

class Patient(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80),  nullable = False)
    phone_number = db.Column(db.String(20), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String(150), nullable = False)
    state = db.Column(db.String(50),  nullable = False)
    city = db.Column(db.String(50), nullable=False)
    patient_status = db.Column(db.String(20), nullable = True)
    bed_type = db.Column(db.String(20), nullable=True)

def get_patients():
    patients = Patient.query.all()
    patients_list = []
    for patient in patients:
        dict = {}
        dict['id'] = patient.id
        dict['name'] = patient.name
        dict['phone'] = patient.phone_number
        dict['age'] = patient.age
        dict['address'] = patient.address
        dict['state'] = patient.state
        dict['city'] = patient.city
        dict['status'] = patient.patient_status
        dict['bed'] = patient.bed_type
        patients_list.append(dict)
    return patients_list

def patient_data():
    phone = request.form["phone"]
    patient = Patient.query.filter_by(phone_number=phone).first()
    patient_data ={}
    if patient:
        patient_data = {'id': patient.id, 'name': patient.name, 'phone': patient.phone_number,
                        'age': patient.age, 'address': patient.address,
                        'state': patient.state, 'city': patient.city,
                        'status': patient.patient_status, 'bed': patient.bed_type
                        }
    return patient_data

@app.route('/',methods=['GET'])
def home_page():
    return render_template("homepage.html")

@app.route('/register_patient',methods=['GET','POST'])
def register_patient():
    if request.method == "GET":
        return render_template("patientdata.html")

    if request.method == "POST":
        name = request.form["name"]
        phone_no = request.form["phone"]
        age = request.form["age"]
        address = request.form["address"]
        state = request.form["state"]
        city = request.form["city"]
        patient_status = request.form["status"]
        bed_type = request.form["bed"]

        patient = Patient.query.filter_by(phone_number=phone_no).first()
        if patient:
            return render_template("patientdata.html",msg = "Patient already registered")
        else:
            new_patient = Patient(name=name, phone_number=phone_no, age=age, address=address, state=state, city=city,
                                  patient_status=patient_status, bed_type=bed_type)
            db.session.add(new_patient)
            db.session.commit()
            return render_template("patientdata.html",patient = name)

@app.route('/getAllPatients',methods=['GET'])
def patients_list():
    if request.method == 'GET':
        patients_list = get_patients()
        return render_template("PatientDatainfo.html",patient = patients_list)

@app.route('/getActivePatients',methods=['GET'])
def active_patients():
    if request.method == 'GET':
        patients_list = get_patients()
        active_patients = []

        for patient in patients_list:
            if patient['status'] == 'Active':
                active_patients.append(patient)
        return render_template("PatientDatainfo.html", patient=active_patients)

@app.route('/getPatient',methods=['GET'])
def patient_details():
    if request.method == 'GET':
        return render_template("PatientActions.html")

@app.route('/getPatientByPhone', methods=['GET','POST'])
def patient_by_Id():
    if request.method == 'POST':
        patient_dtls = patient_data()
        if patient_data:
            return render_template("PatientActions.html",data=patient_dtls)
        else:
            return render_template("PatientActions.html", msg="Patient not Found")

@app.route('/patient/update', methods=['POST'])
def patient_update():
    if request.method == 'POST':
        patient_dtls = patient_data()
        if patient_dtls:
            return render_template("PatientActions.html", update_msg=patient_dtls)
        else:
            return render_template("PatientActions.html", msg="Patient not Found")

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address=request.form['address']
        state=request.form['state']
        city=request.form['city']
        age=request.form['age']
        patient_status=request.form['status']
        bed_type=request.form['bed']

        update_patient = Patient(name=name,phone_number=phone,address=address,state=state,city=city,age=age,patient_status=patient_status,bed_type=bed_type)
        patient_data = {'name': update_patient.name, 'phone_number': update_patient.phone_number,
                        'age': update_patient.age, 'address': update_patient.address,
                        'state': update_patient.state, 'city': update_patient.city,
                        'patient_status': update_patient.patient_status, 'bed_type': update_patient.bed_type
                        }
        Patient.query.filter_by(phone_number=phone).update(patient_data)
        db.session.commit()
        return render_template("PatientActions.html", update=patient_data)

@app.route('/patient/delete', methods=['GET','POST'])
def patient_delete():
    if request.method == 'POST':
        phone = request.form["phone"]
        patient = Patient.query.filter_by(phone_number=phone).first()
        if patient:
            Patient.query.filter_by(phone_number=phone).delete()
            db.session.commit()
            return("Patient deleted successfully.")
        else:
            return("Patient not found.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(port=port)