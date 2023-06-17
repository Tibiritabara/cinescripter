from utils.openai_client import get_embedding, generate_video_script
from utils.weaviate_client import get_answers

class Script:
    def __init__(self, question, tone):
        self.question = question
        self.tone = tone

    def _create_paragraphs(self, answers):
        return '\n'.join(answers)

    def generate(self,):
        question_embedding = get_embedding(self.question)
        answers = get_answers(question_embedding)
        full_text = self._create_paragraphs(answers)
        return generate_video_script(self.question, full_text, self.tone)
