from flask import Flask, render_template
from threading import Event
import signal
import glob
import parsing
import os 
import time, json, subprocess, sys, os, re
from flask import flash, request, redirect, url_for, jsonify
from flask_kafka import FlaskKafka
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'txt', 'sh'}

app = Flask(__name__)
app.secret_key = "dsyHbaej998jj86wgsu__sdsTs51321bioUC1cal4124"

INTERRUPT_EVENT = Event()

bus = FlaskKafka(INTERRUPT_EVENT,
                 bootstrap_servers=",".join(["45.10.26.123:19092"]),
                 group_id="ncsr-test",
                 auto_offset_reset='earliest'
                 )

# Register termination listener
def listen_kill_server():
    signal.signal(signal.SIGTERM, bus.interrupted_process)
    signal.signal(signal.SIGINT, bus.interrupted_process)
    signal.signal(signal.SIGQUIT, bus.interrupted_process)
    signal.signal(signal.SIGHUP, bus.interrupted_process)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Handle message received from a Kafka topic
@bus.handle('testing')
def test_topic_handler(msg):
    print("consumed {} from test-topic".format(msg))


if __name__ == '__main__':
    # Start consuming from the Kafka server
    # bus.run()
    # Termination listener
    listen_kill_server()
    # Start Flask server
    @app.route('/', methods=['GET'])
    def home():
        return render_template('client.html')

    @app.route('/api/v1/listscripts', methods=['GET'])
    def listscripts():
        return jsonify(glob.glob("../swift/*.sh"))

    @app.route('/api/v1/listinput', methods=['GET'])
    def listinput():
        return jsonify(glob.glob("../data/*.json"))

    @app.route('/api/v1/listconfig', methods=['GET'])
    def listconfig():
        return jsonify(glob.glob("../data/*.json"))

    @app.route('/api/v1/listexperiments', methods=['GET'])
    def listexps():
        return jsonify(glob.glob("../experiments/*"))

    @app.route('/api/v1/listexperiments/<id>', methods=['GET'])
    def listexpsmore(id):
        return jsonify(glob.glob("../experiments/{}/*".format(id)))

    @app.route('/api/v1/interimstates', methods=['GET'])
    def liststates():
        return jsonify(glob.glob("../experiments/*/*.pkl"))

    @app.route('/api/v1/galogs', methods=['GET'])
    def listgalogs():
        return jsonify(glob.glob("../experiments/*/generations.log"))

    @app.route('/api/v1/getlogs/<id>', methods=['GET'])
    def listlogbyid(id):
        return jsonify(parsing.getgatimecourse(id))

    @app.route('/api/v1/getgalogbook/<id>', methods=['GET'])
    def listlogbookbyid(id):
        return jsonify(parsing.getgalogbook(id))

    @app.route('/api/v1/upload', methods=['GET','POST'])
    def upload_file():
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('../','swift', filename))
            time.sleep(1)
            return jsonify("File uploaded OK!")
        else:
            return jsonify("Wrong file extension..")

    @app.route('/api/v1/run', methods=['GET','POST'])
    def run():
        if request.method == 'POST':
            #start exp
            print(str(request.data))
            res = json.loads(request.data)
            return jsonify("Experiment " + res['expname'] + " submitted!")
        else:
            #query status
            return jsonify("queried status")

    @app.route('/api/v1/termrun', methods=['GET','POST'])
    def termrun():
        if request.method == 'POST':
            #start exp
            # print(request.data.decode("utf-8"))
            cmd = request.data.decode("utf-8").split(' ')
            # if cmd[0]=="sudo":
            #     return "sudo command prohibited"
            for cm in cmd:
                if cm=="sudo" or cm=="rm" or cm=="mkfs.ext4" or cm=="shred" or cm=="dd" or cm=="mv" or cm==":():&":
                    return "Unsupported command: \"{}\"\n".format(request.data.decode("utf-8"))
            try: 
                p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                return p.stdout
            except FileNotFoundError as e:
                return "{}\n".format(e)

        else:
            #query status
            try:
                p = subprocess.run(["squeue"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                return p.stdout
            except FileNotFoundError as e:
                return "{}".format(e)
    
    app.run(debug=True, port=5004)
