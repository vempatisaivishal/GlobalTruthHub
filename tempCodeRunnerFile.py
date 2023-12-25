@app.route('/update_progress', methods=['POST', 'GET'])
def update_progress():
    global last_executed
    if last_executed == True:
        return jsonify(render_next=True)
    else:
        return jsonify(render_next=False)