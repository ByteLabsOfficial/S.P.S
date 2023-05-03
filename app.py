from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load the json file with the student scores
with open("student_scores.json", "r", encoding="utf-8") as f:
    student_scores = json.load(f)
with open('ProjectStocks.json') as f:
    project_stocks = json.load(f)


@app.route("/add_student", methods=["POST"])
def add_student():
    # Get the student name, password and api key from the request body
    student_name = request.json.get("student_name")
    student_password = request.json.get("student_password")
    api_key = request.json.get("api_key")
    # Check if the student name, password and api key are valid
    if not student_name or not isinstance(student_name, str):
        return jsonify({"error": "Invalid student name"}), 400
    if not student_password or not isinstance(student_password, str):
        return jsonify({"error": "Invalid student password"}), 400
    if not api_key or not isinstance(api_key, str):
        return jsonify({"error": "Invalid api key"}), 400
    # Check if the api key matches the secret string
    if api_key != "secret123":
        return jsonify({"error": "Unauthorized access"}), 401
    # Check if the student already exists in the json file
    if student_name in student_scores:
        return jsonify({"error": "Student already exists"}), 409
    # Add the student with the default score of 10 and the given password to the json file
    student_scores[student_name] = {"password": student_password, "score": 10}
    with open("student_scores.json", "w", encoding="utf-8") as f:
        json.dump(student_scores, f, ensure_ascii=False)
    # Return a success message
    return jsonify({"message": f"Student {student_name} added with score 10 and password {student_password}"}), 201


@app.route("/change_student_score", methods=["PUT"])
def change_student_score():
    # Get the student name, score and api key from the request body
    student_name = request.json.get("student_name")
    student_score = request.json.get("student_score")
    api_key = request.json.get("api_key")
    # Check if the student name, score and api key are valid
    if not student_name or not isinstance(student_name, str):
        return jsonify({"error": "Invalid student name"}), 400
    if not student_score or not isinstance(student_score, int):
        return jsonify({"error": "Invalid student score"}), 400
    if not api_key or not isinstance(api_key, str):
        return jsonify({"error": "Invalid api key"}), 400
    # Check if the api key matches the secret string
    if api_key != "secret123":
        return jsonify({"error": "Unauthorized access"}), 401
    # Check if the student exists in the json file
    if student_name not in student_scores:
        return jsonify({"error": "Student not found"}), 404
    # Change the student score in the json file
    student_scores[student_name]["score"] = student_score
    with open("student_scores.json", "w", encoding="utf-8") as f:
        json.dump(student_scores, f, ensure_ascii=False)
    # Return a success message
    return jsonify({"message": f"Student {student_name} score changed to {student_score}"}), 200


@app.route("/read_student_score", methods=["GET"])
def read_student_score():
    # Get the student name from the query string
    student_name = request.json.get("student_name")
    print(student_name)
    # Check if the student name is valid
    if not student_name or not isinstance(student_name, str):
        return jsonify({"error": "Invalid student name"}), 400
    # Check if the student exists in the json file
    if student_name not in student_scores:
        return jsonify({"error": "Student not found"}), 404
    # Return the student score from the json file
    return jsonify({"student_name": student_name, "student_score": student_scores[student_name]["score"]}), 200


@app.route("/sign_in", methods=["POST"])
def sign_in():
    # Get the student name and password from the request body
    student_name = request.json.get("student_name")
    student_password = request.json.get("student_password")
    # Check if the student name and password are valid
    if not student_name or not isinstance(student_name, str):
        return jsonify({"error": "Invalid student name"}), 400
    if not student_password or not isinstance(student_password, str):
        return jsonify({"error": "Invalid student password"}), 400
    # Check if the student exists in the json file
    if student_name not in student_scores:
        return jsonify({"error": "Student not found"}), 404
    # Check if the password matches the one in the json file
    if student_password != student_scores[student_name]["password"]:
        return jsonify({"error": "Wrong password"}), 401
    # Return a success message
    return jsonify({"message": f"Student {student_name} signed in successfully"}), 200


@app.route('/invest', methods=['POST'])
def invest():
    # Parse request data
    data = request.get_json()
    student_name = data['student_name']
    project_name = data['project_name']
    invest_points = data['invest_points']

    # Check if student exists and has enough points to invest
    if student_name not in student_scores:
        return f"Error: {student_name} is not a valid student name"
    if student_scores[student_name]['score'] < invest_points:
        return f"Error: {student_name} does not have enough points to invest {invest_points}"

    # Update project stock and student scores
    if project_name not in project_stocks:
        project_stocks[project_name] = {
            'CEO': '', 'Type': '', 'StockValue': 0, 'StockAmmount': 0}
    stock_amount = project_stocks[project_name]['StockAmmount']
    stock_value = project_stocks[project_name]['StockValue']
    new_stock_amount = stock_amount + invest_points
    # TODO: Make the stock_value better go up when there are more investments and not tank down when someone takes their money out
    stock_value = (stock_value * stock_amount +
                   invest_points) / new_stock_amount
    project_stocks[project_name]['StockAmmount'] = new_stock_amount
    project_stocks[project_name]['StockValue'] = stock_value
    student_scores[student_name]['score'] -= invest_points
    if project_name not in student_scores[student_name]:
        student_scores[student_name][project_name] = invest_points
    else:
        student_scores[student_name][project_name] += invest_points

    # Write updated data to json files
    with open('student_scores.json', 'w') as f:
        json.dump(student_scores, f)
    with open('ProjectStocks.json', 'w') as f:
        json.dump(project_stocks, f)

    return f"{student_name} invested {invest_points} points in {project_name}"


@app.route('/withdraw', methods=['POST'])
def withdraw():
    # Parse request data
    data = request.get_json()
    student_name = data['student_name']
    project_name = data['project_name']

    # Check if student and project exist and if the student invested in the project
    if student_name not in student_scores:
        return f"Error: {student_name} is not a valid student name"
    if project_name not in project_stocks:
        return f"Error: {project_name} is not a valid project name"
    if project_name not in student_scores[student_name]:
        return f"Error: {student_name} did not invest in {project_name}"

    # Calculate profit/loss based on stock value change
    invested_points = student_scores[student_name][project_name]
    stock_amount = project_stocks[project_name]['StockAmmount']
    stock_value = project_stocks[project_name]['StockValue']
    new_stock_amount = stock_amount - invested_points
    if new_stock_amount == 0:
        new_stock_value = 0
    else:
        new_stock_value = (stock_value * stock_amount -
                           invested_points) / new_stock_amount
    profit_loss = (new_stock_value - stock_value) * invested_points

    # Update project stock and student scores
    project_stocks[project_name]['StockAmmount'] = new_stock_amount
    project_stocks[project_name]['StockValue'] = new_stock_value
    student_scores[student_name]['score'] += invested_points
    del student_scores[student_name][project_name]

    # Write updated data to json files
    with open('student_scores.json', 'w') as f:
        json.dump(student_scores, f)
    with open('ProjectStocks.json', 'w') as f:
        json.dump(project_stocks, f)

    return f"{student_name} withdrew {invested_points} points from {project_name} with a profit/loss of {profit_loss}"
