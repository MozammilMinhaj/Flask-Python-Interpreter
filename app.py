from flask import Flask, render_template, request
import subprocess
import re
 
app = Flask(__name__)
 
@app.route('/')
def code():
    result={"code":"print('Hello World')","codeoutput":"Hello World"}
    return render_template('code.html',result=result)

@app.route('/code', methods = ['POST'])
def code_compile():
    if request.method == 'POST':
        code = request.form['pycode']

    f = open("onlinecode.py", "w")
    f.write(code)
    f.close()
    pipe = subprocess.run(["python", "onlinecode.py"], capture_output=True)

    if pipe.returncode == 0:
        codeoutput = re.sub('[^A-Za-z0-9().,\n\t ]+', '',pipe.stdout.decode('utf-8'))
        result={"code":code,"codeoutput":codeoutput}
        return render_template('code.html',result=result)
    else:
        codeoutput = re.sub('[^A-Za-z0-9().,\n\t ]+', '',pipe.stderr.decode('utf-8'))
        result={"code":code,"codeoutput":codeoutput}
        return render_template('code.html',result=result)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
