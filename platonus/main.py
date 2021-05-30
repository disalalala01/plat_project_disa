from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# from platonus import logger
from platonus_marks import get_all
from login import get_session


@app.route('/login', methods=['POST'])
def login_to_platonus():
    global main_session
    try:
        data = request.json
        if len(data['iin']) > 12:
            return jsonify({
                'msg': 'iin is not correct'
            })
        session = get_session(iin=data['iin'], password=data['password'])
        if not session:
            return jsonify({'msg': 'cant login in platonus'})
        result = get_all(session)
        return jsonify(result)
    except Exception as e:
        # logger.exception(e)
        print(e)
        logging.exception(e)
    return {'msg': 'error'}


if __name__ == '__main__':
    app.run(host='localhost', port=5000)