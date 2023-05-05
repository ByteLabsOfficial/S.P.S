# School Point System (S.P.S)
S.P.S is a simple flask python app that manages the score of students. We looked at the score of each student as the amount of money they have, therefore we decided to add a simple stock market.<br/>
The stock market currently is based around the idea that different school projects are stocks and people can invest in and redraw from them, to make a profit.</br>
**Note: This project is a WIP (work in progress), therefore it's not in a usable state right now. But we expect to have it be functional soon with the help of online contributors**

## Functions
*API Key is currently the following:*<br/>
```8881626825596828425145363414598667531018683```

### 1- /add_student
**Description:** adds the student to the student_scores.json file<br/><br/>
**Input:** a json consisting of a student_name, student_password, and api_key<br/> An example would be: <br/>
```
{
"student_name": "Sam",
"student_password": "1234",
"api_key": "8881626825596828425145363414598667531018683"
}
```
</br><br/>
**Output:** a json with the format of</br>
```{"message": "Student SAMPLE_STUDENT added with score 10 and password STUDENT_PASSWORD"}```<br/><br/>
**Errors:**<br/>
- ```{"error": "Invalid student name"}``` - You didn't provide a string as student_name in the inputed json
- ```{"error": "Invalid student password"}``` - You didn't provide a string as student_password in the inputed json
- ```{"error": "Invalid api key"}``` - You didn't provide a string as api_key in the inputed json
- ```{"error": "Unauthorized access"}``` - You didn't provide the correct api_key in the inputed json
- ```{"error": "Student already exists"}``` - The student_name you provided in the inputed json already exists
<br/><br/><br/><br/>

### 2- /change_student_score
**Description:** *changes* the student's score in the student_scores.json file by the amount provided<br/><br/>
**Input:** a json consisting of a student_name, student_score, and api_key<br/> An example would be: <br/>
```
{
"student_name": "Sam",
"student_score": 20,
"api_key": "8881626825596828425145363414598667531018683"
}
```
</br></br>
**Output:** a json with the format of</br>
```{"message": "Student SAMPLE_STUDENT score changed to NEW_SCORE"}```<br/><br/>
**Errors:**<br/>
- ```{"error": "Invalid student name"}``` - You didn't provide a string as student_name in the inputed json
- ```{"error": "Invalid student score"}``` - You didn't provide an int as student_score in the inputed json
- ```{"error": "Invalid api key"}``` - You didn't provide a string as api_key in the inputed json
- ```{"error": "Unauthorized access"}``` - You didn't provide the correct api_key in the inputed json
- ```{"error": "Student not found"}``` - The student_name you provided wasn't found in the student_scores.json file
<br/><br/><br/><br/>

### 3- /read_student_score
**Description:** returns a student's score<br/><br/>
**Input:** a json consisting of a student_name<br/> An example would be: <br/>
```
{
"student_name": "Sam"
}
```
</br></br>
**Output:** a json with the format of</br>
```{"student_name": "SAMPLE_STUDENT", "student_score": 10}```<br/><br/>
**Errors:**<br/>
- ```{"error": "Invalid student name"}``` - You didn't provide a string as student_name in the inputed json
- ```{"error": "Student not found"}``` - The student_name you provided wasn't found in the student_scores.json file
<br/><br/><br/><br/>
