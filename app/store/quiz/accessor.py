from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Theme,
    Question,
    Answer,
    ThemeModel,
    QuestionModel,
    AnswerModel,
)
from typing import List


class QuizAccessor(BaseAccessor):
    @staticmethod
    async def create_theme(title: str) -> Theme:
        new_theme = await ThemeModel.create(title=title)
        return Theme(id=new_theme.id, title=new_theme.title)

    @staticmethod
    async def get_theme_by_title(title: str) -> Optional[Theme]:
        theme = await ThemeModel.query.where(ThemeModel.title == title).gino.first()
        return None if not theme else Theme(id=theme.id, title=theme.title)

    @staticmethod
    async def get_theme_by_id(id_: int) -> Optional[Theme]:
        theme = await ThemeModel.query.where(ThemeModel.id == id_).gino.first()
        return None if not theme else Theme(id=theme.id, title=theme.title)

    @staticmethod
    async def list_themes() -> List[Theme]:
        themes = await ThemeModel.query.gino.all()
        return [Theme(id=theme.id, title=theme.title) for theme in themes]

    @staticmethod
    async def create_answers(question_id, answers: List[Answer]):
        await AnswerModel.insert().gino.all(
            [{
                'title': a.title,
                'is_correct': a.is_correct,
                'question_id': question_id
            }
                for a in answers])

    @staticmethod
    async def create_question(title: str, theme_id: int, answers: List[Answer]) -> Question:
        question_db = await QuestionModel.create(title=title, theme_id=theme_id)
        question = Question(
            id=question_db.id,
            title=question_db.title,
            theme_id=question_db.theme_id,
            answers=answers
        )

        await QuizAccessor.create_answers(question.id, answers)
        return question

    @staticmethod
    async def get_question_by_title(title: str) -> Optional[Question]:
        question = await QuestionModel.query.where(QuestionModel.title == title).gino.first()
        if question is None:
            return None

        return Question(
            id=question.id,
            title=question.title,
            theme_id=question.theme_id,
            answers=await QuizAccessor.get_answers_of_question(question.id))

    @staticmethod
    async def get_answers_of_question(question_id: int) -> list[Answer]:
        answers_bd = await AnswerModel.query.where(AnswerModel.question_id == question_id).gino.all()
        return [Answer(title=ans.title, is_correct=ans.is_correct) for ans in answers_bd]

    @staticmethod
    async def list_questions(theme_id: Optional[int] = None) -> List[Question]:
        questions = await QuestionModel.query.gino.all()
        return [Question(id=quest.id,
                         title=quest.title,
                         theme_id=quest.theme_id,
                         answers=await QuizAccessor.get_answers_of_question(quest.id))
                for quest in questions]
