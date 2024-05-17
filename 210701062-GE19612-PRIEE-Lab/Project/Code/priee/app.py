from flask import Flask, redirect, render_template, request, jsonify, url_for
from flask_pymongo import PyMongo
import openai
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import fitz
from docx import Document  # python-docx for DOCX files
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["MONGO_URI"] = "mongodb://localhost:27017/urcareer"
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded files
mongo = PyMongo(app)
collection = mongo.db.resume

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

openai.api_key = 'sk-proj-RLexVVZONbI85fp3CYqkT3BlbkFJ6VpPhCLy2dHmtqmGuLVp'  # Replace with your OpenAI API key

# Function to extract text from PDF files
def extract_text_from_pdf(file_path):
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        app.logger.error('An error occurred while extracting text from PDF: %s', str(e))
    return text

# Function to extract text from DOCX files
def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text
    except Exception as e:
        app.logger.error('An error occurred while extracting text from DOCX: %s', str(e))
    return text

# Function to extract keywords from the resume content
def extract_keywords(resume_content):
    words = word_tokenize(resume_content)
    keywords = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    word_freq = nltk.FreqDist(keywords)
    return word_freq

# Function to assign weightage to keywords
def assign_weightage(keywords):
    weighted_keywords = {keyword: freq * 10 for keyword, freq in keywords.items()}
    return weighted_keywords

# Function to generate MCQs using OpenAI
def generate_mcq(keyword):
    prompt = f"Generate a multiple-choice question (MCQ) for the technical keyword '{keyword}' with 4 options."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to evaluate the assessment answers
def evaluate_answers(user_answers, correct_answers):
    score = 0
    for user_answer, correct_answer in zip(user_answers, correct_answers):
        if user_answer == correct_answer:
            score += 1
    return score

@app.route('/upload_resume', methods=['GET','POST'])
def upload_resume():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if filename.endswith('.pdf'):
                resume_content = extract_text_from_pdf(file_path)
            elif filename.endswith('.docx'):
                resume_content = extract_text_from_docx(file_path)
            else:
                return jsonify({'error': 'Unsupported file format'}), 400
            
            # Extract keywords from resume content
            keywords = extract_keywords(resume_content)
            # Assign weightage to keywords
            weighted_keywords = assign_weightage(keywords)
            # Store keywords with weightage in MongoDB
            mongo.db.keywords.insert_one({'keywords': weighted_keywords})
           
            return redirect(url_for('generate_assessment')), 302
    except Exception as e:
        app.logger.error('An error occurred while uploading resume: %s', str(e))
        return jsonify({'error': 'An error occurred while uploading resume'}), 500

@app.route('/generate_assessment', methods=['GET','POST'])
def generate_assessment():
    try:
        # Fetch the highest-weighted keywords from MongoDB
        keywords_data = mongo.db.keywords.find_one(sort=[("_id", -1)])
        if not keywords_data:
            return jsonify({'error': 'No keywords found in database'}), 400

        keywords = keywords_data['keywords']
        sorted_keywords = sorted(keywords.items(), key=lambda item: item[1], reverse=True)
        top_keywords = [kw for kw, weight in sorted_keywords[:5]]  # Taking top 5 keywords

        questions = []
        for keyword in top_keywords:
            question = generate_mcq(keyword)
            questions.append(question)
        
        return render_template('generate_assessment.html', questions=questions)
    except Exception as e:
        app.logger.error('An error occurred while generating assessment: %s', str(e))
        return jsonify({'error': 'An error occurred while generating assessment'}), 500

@app.route('/submit_assessment', methods=['POST'])
def submit_assessment():
    try:
        user_answers = request.form.getlist('answers')
        correct_answers = request.form.getlist('correct_answers')  # This should come from the generated questions

        score = evaluate_answers(user_answers, correct_answers)
        return jsonify({'score': score}), 200
    except Exception as e:
        app.logger.error('An error occurred while submitting assessment: %s', str(e))
        return jsonify({'error': 'An error occurred while submitting assessment'}), 500

@app.route('/view_score', methods=['GET'])
def view_score():
    try:
        # Placeholder for retrieving score from MongoDB
        score = 80  # Placeholder for retrieving score
        return render_template('view_score.html', score=score)
    except Exception as e:
        app.logger.error('An error occurred while retrieving score: %s', str(e))
        return jsonify({'error': 'An error occurred while retrieving score'}), 500

@app.route('/recommend_job', methods=['GET'])
def recommend_job():
    try:
        # Placeholder for job recommendation based on score
        recommendation = "Software Engineer"  # Placeholder for recommendation
        return render_template('recommend_job.html', recommendation=recommendation)
    except Exception as e:
        app.logger.error('An error occurred while recommending job: %s', str(e))
        return jsonify({'error': 'An error occurred while recommending job'}), 500

@app.route('/')
def index():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
