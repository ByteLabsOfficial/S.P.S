from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load the json file with the student scores
with open("student_scores.json", "r", encoding="utf-8") as f:
    student_scores = json.load(f)

# Load the json file with the project stocks
with open("project_stocks.json", "r", encoding="utf-8") as f:
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

@app.route("/invest_in_project", methods=["POST"])
def invest_in_project():
    # Get the student name, password, project name and points from the request body
    student_name = request.json.get("student_name")
    student_password = request.json.get("student_password")
    project_name = request.json.get("project_name")
    points = request.json.get("points")
    # Check if the parameters are valid
    if not student_name or not isinstance(student_name, str):
        return jsonify({"error": "Invalid student name"}), 400
    if not student_password or not isinstance(student_password, str):
        return jsonify({"error": "Invalid student password"}), 400
    if not project_name or not isinstance(project_name, str):
        return jsonify({"error": "Invalid project name"}), 400
    if not points or not isinstance(points, int) or points <= 0:
        return jsonify({"error": "Invalid points"}), 400
    # Check if the student exists in the student scores file
    if student_name not in student_scores:
        return jsonify({"error": "Student not found"}), 404
    # Check if the password matches the one in the student scores file
    if student_password != student_scores[student_name]["password"]:
        return jsonify({"error": "Wrong password"}), 401
    # Check if the project exists in the project stocks file
    if project_name not in project_stocks:
        return jsonify({"error": "Project not found"}), 404
    # Check if the student has enough points to invest
    if points > student_scores[student_name]["score"]:
        return jsonify({"error": "Insufficient points"}), 403
    # Deduct the points from the student score in the student scores file
    student_scores[student_name]["score"] -= points
    # Add the points to the project stock amount in the project stocks file
    project_stocks[project_name]["stock_amount"] += points
    # Update the project stock value based on a formula that depends on the stock amount and type of project
    # For simplicity, I will use a linear formula: stock_value = base_value + factor * stock_amount / 1000
    # The base value and factor are different for each type of project
    base_value = {"programming": 5, "design": 10, "business": 15}
    factor = {"programming": 2, "design": 1.5, "business": 1}
    project_type = project_stocks[project_name]["type"]
    project_stocks[project_name]["stock_value"] = base_value[project_type] + factor[project_type] * project_stocks[project_name]["stock_amount"] / 1000
    # Round the stock value to two decimal places
    project_stocks[project_name]["stock_value"] = round(project_stocks[project_name]["stock_value"], 2)
    # Keep track of how many points each student invested in each project in a nested dictionary in the project stocks file
    # The format is: {"investors": {"student_name": points, ...}, ...}
    if "investors" not in project_stocks[project_name]:
        project_stocks[project_name]["investors"] = {}
    if student_name not in project_stocks[project_name]["investors"]:
        project_stocks[project_name]["investors"][student_name] = 0
    project_stocks[project_name]["investors"][student_name] += points
    # Save the changes to both files
    with open("student_scores.json", "w", encoding="utf-8") as f:
        json.dump(student_scores, f, ensure_ascii=False)
    with open("project_stocks.json", "w", encoding="utf-8") as f:
        json.dump(project_stocks, f, ensure_ascii=False)
    # Return a success message with the profit or loss information
    if profit_or_loss > 0:
        return jsonify({"message": f"Student {student_name} withdrew {points} points from project {project_name} and made a profit of {profit_or_loss} points"}), 200
    elif profit_or_loss < 0:
        return jsonify({"message": f"Student {student_name} withdrew {points} points from project {project_name} and made a loss of {abs(profit_or_loss)} points"}), 200
    else:
        return jsonify({"message": f"Student {student_name} withdrew {points} points from project {project_name} and broke even"}), 200