from scoremodel import app
from scoremodel.modules.api import ScoremodelApi
from flask import request


@app.route('/api/question', methods=['POST'])
@app.route('/api/question/<question_id>', methods=['GET', 'PUT', 'DELETE'])
def a_question(question_id=None):
    pass
