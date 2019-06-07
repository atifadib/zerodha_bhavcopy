from flask import Flask, render_template, jsonify, request
import subprocess
import pandas as pd
from os import listdir

app = Flask(__name__, template_folder='./templates/')


@app.route('/')
def index():
    """
    :return: Loads the Index Page of the Application
    """
    return render_template('index.html')


def bse_bhav_table_object(df):
    """
    :param df: DataFrame object from BSE Website
    :return: DataTable object for HTML
    """
    df = df.fillna('No-Value')
    json_data = []
    for row in df.itertuples():
        json_data.append(row._asdict())
    return json_data


@app.route('/bse_bhav', methods=['POST'])
def bse_bhav():
    """
    :return: Collects the BHAVCOPY Data from BSE Website and returns a jsonified string
    """
    form_data = request.form
    date = form_data['bhav_date']
    date = date.split("-")
    date = date[-1]+date[-2]+date[0][-2:]
    json_response = {"status": "", "data": []}
    filename = 'EQ' + date + '.CSV'
    print("Fetch BSE Bhav for Date: ", date)
    print("BSE File name:", filename)
    try:
        if filename in listdir('./BHAV_DATA/'):
            data = pd.read_csv('./BHAV_DATA/'+filename)
            json_response['status'] = 'OK'
            json_data = bse_bhav_table_object(data)
            json_response['data'] = json_data
        else:
            process = subprocess.Popen('sh get_bhav_copy.sh '+date, shell=True)
            process.wait()
            response_code = open('bse_response.txt', 'r')
            response_code = response_code.readlines()[0].strip()
            if response_code == '200':
                data = pd.read_csv('./BHAV_DATA/'+filename)
                json_response['status'] = 'OK'
                json_data = bse_bhav_table_object(data)
                json_response['data'] = json_data
            else:
                json_response['status'] = 'BSE Server Error, Code:'+str(response_code)
    except Exception as e:
        json_response['status'] = 'Error Occured:'+str(e)
    print(json_response['status'], 'Size of Data:', len(json_response['data']))
    return jsonify(json_response)


if __name__ == '__main__':
    app.run()
