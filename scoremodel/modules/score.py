from scoremodel.models.general import Answer, Question
from scoremodel.modules.error import ItemNotFound


class AnswerScore:
    """
    Every answer has a score. This score is computed as follows:
        * Get the weight of the question via Question.weight
        * Get the value of the given answer via Question.answers and Answer.value
        * Do value * weight
        * Return
    Also provides the value you have to multiply the score with to get to 100:
        * Get the maximum score for every answer corresponding to every question in this section
        * Do 100/maximum
        * Return
    Attributes:
        score: score for this answer to this question. Weight factor included.
        maximum: maximum score for all questions in the section this question belongs to
        multiply_factor: factor to multiply the score with to get the result that will get you to 100
    """
    def __init__(self, question_id, answer_id):
        """
        :param question: the ID of the question
        :param answer_id: the ID of the provided answer
        :return:
        """
        try:
            self.question = Question.query.filter(Question.id == question_id).one()
        except:
            raise ItemNotFound('No question with this ID: {0}'.format(question_id))
        try:
            self.answer = Answer.query.filter(Answer.id == answer_id).one()
        except:
            raise ItemNotFound('No answer with this ID: {0)'.format(answer_id))
        self.score = self.compute_score()
        self.maximum = self.compute_maximum()
        self.multiply_factor = self.compute_multiply_factor(self.maximum)

    def compute_score(self):
        question_weight = self.question.weight
        answer_value = self.answer.value
        return question_weight * answer_value

    def compute_maximum(self):
        section = self.question.section
        all_questions = section.questions.all()
        maximum = 0
        for question in all_questions:
            maximum = maximum + question.highest_answer()
        return maximum

    def compute_multiply_factor(self, maximum):
        return 100/maximum
