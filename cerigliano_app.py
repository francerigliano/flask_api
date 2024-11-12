#Here fist I import all necessary libraries, that are mainly Flask and its extension that adds support for SQLAlchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #Now I create the instance of Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://francerigliano:Zzxq2rQr1nhnOmOhNXMTLpSKw16oPckR@dpg-cspdfg3tq21c739rtbo0-a/dna_verification' #Then I make the necessary SQL Alchemy configurations, I name the local sqlite database as dna_verification.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #This is to prevent warnings related to Flask-SQLAlchemy
db = SQLAlchemy(app) #Afterwards I initialize SQLAlchemy with the Flask app for database management.

class DNAResult(db.Model): #Class that creates the database model
     __tablename__ = 'dna_result'
    id = db.Column(db.Integer, primary_key=True) #ID column as an auto-incrementing integer, its also the primary key
    is_mutant = db.Column(db.Boolean, nullable=False) #Boolean column that indicates if its Mutant or not

#Now I construct the function that can check if DNA sequence is mutant or not
def isMutant(dna_sequence):
    if not dna_sequence or not all(isinstance(row, str) for row in dna_sequence): #First I verify if input is a list of strings
        raise ValueError("Input must be a list of strings.") #Otherwise, it raises en error
    
    n = len(dna_sequence)
    valid_chars = {'A', 'T', 'C', 'G'} #Now I check if the this list of strings cointains only ATGC letters

    for row in dna_sequence: #This For loop is to check if matrix is NxN and only contains valid characters
        if len(row) != n:
            raise ValueError("Matrix is not NxN.")
        if len(row) < 4: #I also check that he minimun is 4
            raise ValueError("Each row must have at least 4 characters.")
        if not all(char in valid_chars for char in row): #Now I check that each string has the valid characters
            raise ValueError("Matrix contains invalid characters. Only A, T, C, G are allowed.")
    
    def count_matches_in_direction(x, y, dx, dy):
        #This function starts from the initial position (x, y) and get the character at that position
        char = dna_sequence[x][y]
        count = 1  # Initialize match count to 1 to include the starting position

        for _ in range(3): #The For loop to check the next 3 positions in the specified direction
            x += dx  #Movement in the x direction by 'dx'
            y += dy  #Movement in the y direction by 'dy'

            #Then it checks if the new position is within the boundaries of the matrix and matches the character
            if 0 <= x < n and 0 <= y < n and dna_sequence[x][y] == char:
                count += 1  #If character matches, the count increments
            else:
                break  #Stop checking if the position is out of bounds or characters don't match

        #Finally it return True if there are 4 or more consecutive matching characters
        return count >= 4
        
    coincidences = 0 #Start the coincidences counter at 0

    for i in range(n): #Then I made a double For lop to check for sequences in all directions
        for j in range(n):
            if (
                count_matches_in_direction(i, j, 1, 0) or  #First vertical (down)
                count_matches_in_direction(i, j, 0, 1) or  #Second horizontal (right)
                count_matches_in_direction(i, j, 1, 1) or  #Third diagonal (down-right)
                count_matches_in_direction(i, j, 1, -1)    #Fourth diagonal (down-left)
            ):
                coincidences += 1
    if coincidences > 1:
        return coincidences, True  #Finally I return True value if more than one match found

    return coincidences, False  #If no match or only one match is found, then return False

@app.route('/') #Simple helper for me
def home():
    return "Welcome to the Flask API by Francisco Cerigliano"

@app.route('/mutant', methods=['POST'])  #Now I set up the '/mutant' endpoint to accept POST requests.
def check_dna():  #First I define the function definition for handling POST requests at the '/mutant' endpoint.
    try:
        data = request.get_json()  #This is to parse the incoming request data as JSON.
        dna = data.get('dna')  #Now I extract the 'dna' field from the parsed JSON data.
        
        _, is_mutant = isMutant(dna)  #Afterwards I run the `isMutant` function to check if the DNA sequence is mutant.
        
        #The I create a new `DNAResult` object with the result of the DNA check.
        result = DNAResult(is_mutant=is_mutant)
        db.session.add(result)  #This line is to add the new result object to the database session.
        db.session.commit()  #This other line is to commit the session to save the new record to the database.
        
        if is_mutant:  # Check if the result indicates mutant DNA.
            return jsonify({"message": "Mutant DNA detected"}), 200  #Return a JSON response with status 200-OK.
        else:
            return jsonify({"message": "Human DNA detected"}), 403  #Return a JSON response with status 403-Forbidden.
    except ValueError as e:  #This except isto handle any `ValueError` exceptions raised during processing.
        return jsonify({"error": str(e)}), 402  #Return a JSON response with status 402 and the error message.

@app.route('/stats', methods=['GET'])  #Next I set up the '/stats' endpoint to accept GET requests.
def get_stats():  #This other function definition is for handling GET requests at the '/stats' endpoint.
    total_mutants = DNAResult.query.filter_by(is_mutant=True).count()  #First I count the number of mutant DNA results in the database.
    total_humans = DNAResult.query.filter_by(is_mutant=False).count()  #Second I count the number of human DNA results in the database.
    
    #I define the variable 'ratio' to calculate the ratio of mutants to humans, avoiding division by zero.
    ratio = total_mutants / total_humans if total_humans > 0 else 'undefined'

    # Create a dictionary with the stats data.
    stats = {
        "count_mutant_dna": total_mutants,  #Number of mutant DNA results.
        "count_human_dna": total_humans,  #Number of human DNA results.
        "ratio": ratio  #The ratio of mutant to human DNA results.
    }
    return jsonify(stats)  #Return the stats as a JSON response.

if __name__ == '__main__':  #This ensures the script runs only if it's the main module.
    with app.app_context():  #Set up the application context for database operations.
        db.create_all()  #This ensures that the database tables are created before running the app.
        app.run()  #Finally I start the Flask app with debugging enabled.
