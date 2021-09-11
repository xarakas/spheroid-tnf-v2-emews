from flask import Flask, render_template
from threading import Event
import signal
import glob
import parsing
import os
import time, json, subprocess, sys, os, re
import paramiko
# from PIL import Image
# from io import StringIO
from flask import flash, abort, request, redirect, url_for, jsonify, send_file
from flask_kafka import FlaskKafka
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'txt', 'sh'}

app = Flask(__name__)
app.secret_key = "dsyHbaej998jj86wgsu__sdsTs51321bioUC1cal4124"

INTERRUPT_EVENT = Event()

# bus = FlaskKafka(INTERRUPT_EVENT,
#                  bootstrap_servers=",".join(["45.10.26.123:19092"]),
#                  group_id="ncsr-test",
#                  auto_offset_reset='earliest'
#                  )

# # Register termination listener
# def listen_kill_server():
#     signal.signal(signal.SIGTERM, bus.interrupted_process)
#     signal.signal(signal.SIGINT, bus.interrupted_process)
#     signal.signal(signal.SIGQUIT, bus.interrupted_process)
#     signal.signal(signal.SIGHUP, bus.interrupted_process)

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # Handle message received from a Kafka topic
# @bus.handle('testing')
# def test_topic_handler(msg):
#     print("consumed {} from test-topic".format(msg))


if __name__ == '__main__':
    # Start consuming from the Kafka server
    # bus.run()
    # Termination listener
    # listen_kill_server()
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

    @app.route('/api/v1/getpng/<expname>/<id>', methods=['GET'])
    def image(expname, id):
        try:
            filename = "../experiments/{}/figures/{}variables_vs_time.png".format(expname,id)
            return send_file(filename, mimetype='image/gif')

        except IOError as e:
            print(e)
            abort(404)

        # return send_from_directory('.', filename)
    # def getgapng(id):
    #     return jsonify("requested png for {}".format(id))

    @app.route('/api/v1/getexpdetails/<id>', methods=['GET'])
    def getexpdetails(id):
        return jsonify(parsing.getexpdetails(id))

    @app.route('/api/v1/getcsv/<id>', methods=['GET'])
    def getgacsv(id):
        return jsonify("requested csv for {}".format(id))

    @app.route('/api/v1/getlogs/<id>', methods=['GET'])
    def listlogbyid(id):
        return jsonify(parsing.getgatimecourse(id))

    @app.route('/api/v1/getgalogbook/<id>', methods=['GET'])
    def listlogbookbyid(id):
        return jsonify(parsing.getgalogbook(id))

    @app.route('/api/v1/getga3d/<id>/<limit>', methods=['GET'])
    def list3dbyid(id, limit):
        return jsonify(parsing.getga3d(id,limit))

    @app.route('/api/v1/getinds/<id>', methods=['GET'])
    def listindsbyid(id):
        return jsonify(parsing.getindividuals(id))

    @app.route('/api/v1/createbootstrappop', methods=['POST'])
    def createpop():
        # print(json.loads(request.data))
        tofile = json.loads(request.data)
        with open('./interesting_points.json', 'w') as outfile:
            json.dump(tofile, outfile)
        with open('./interesting_points.txt', 'w') as outfile2:
            a =[]
            for subitem in tofile:
                b=[]
                pairs = subitem.items()
                for key, value in pairs:
                    b.append(float(value))
                a.append(b)
            outfile2.write(str(a))
        return jsonify("OK")
    #def listindsbyid(id):
    #    return jsonify(parsing.getindividuals(id))

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
        f = open('./credentials.json',)
        cred = json.load(f) #credentials
        print("Run function!!!")
        #open ssh connection
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ("ssh: connecting")
        c.connect( hostname = cred['hostname'], username = cred['username'], password = cred['password'])
        print ("ssh: connected")
        ######
        if request.method == 'POST':
            #start exp TODO
            print(str(request.data))
            res = json.loads(request.data)
            #commands = "module load python java R/3.4.0 swiftt/1.4.3; cd /gpfs/scratch/bsc08/bsc08646/eleni/spheroid-tnf-v2-emews/"
            commands = "module load python java R/3.4.0 swiftt/1.4.3; cd "
            commands = commands + res['path']
            #bash swift/swift_run_eqpy_compare.sh <EXPERIMENT_ID> <GA_PARAMS_FILE> <GA_CONFIG> <CHECKPOINT_FILE>
            if (res['interimresults'] == ""):
                print("No checkpoints provided")
                command = ";bash " + "./swift/" + res['scriptname'] + " " + res['expname'] + " " + "data/" + res['inputfile'] + " " + "data/" + res['conffile']
            else:
                command = ";bash " + "./swift/" + res['scriptname'] + " " + res['expname'] + " " + "data/" + res['inputfile'] + " " + "data/" + res['conffile'] + " " + res['interimresults']
            commands = [commands + command]
            for command in commands:
                print ("Executing {}".format( command ))
                stdin , stdout, stderr = c.exec_command(command)
                print("After Executing")
                print (stdout.read())
                print("After Executing2")
                print( "Errors")
                print (stderr.read())
                print("After Executing3")


            # print ("Executing {}".format( commands ))
            # stdin , stdout, stderr = c.exec_command(commands)
            # print (stdout.read())
            # print( "Errors")
            # print (stderr.read())
            c.close()
            print ("close ssh connection")
            return jsonify("Experiment " + res['expname'] + " submitted!")

        else:
            #query status TODO
            command = "squeue"
            print ("Executing {}".format( command ))
            stdin , stdout, stderr = c.exec_command(command)
            output = stdout.read().decode()
            errors = stderr.read().decode()
            print (output)
            print( "Errors")
            print (errors)
            c.close()
            print ("close ssh connection")
            #return (json.dumps((stdout.read().decode())))
            return jsonify(output)

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
