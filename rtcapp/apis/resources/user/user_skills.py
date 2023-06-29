from flask_restful import Resource, reqparse
from flask import jsonify

from rtcapp import db

from models import User, Skill

parser = reqparse.RequestParser()
parser.add_argument('name',type=str)

class UserSkills(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        skills = [skill.name for skill in user.skills]
        return jsonify({"user_id": user.id, "skills": skills}), 200

    def post(self, user_id):
        args = parser.parse_args()
        skill_name = args['name']
        skill = Skill.query.filter_by(name=skill_name).first()
        if not skill:
            skill = Skill(name=skill_name)
            db.session.add(skill)
        user = User.query.get(user_id)
        user.skills.append(skill)
        db.session.commit()
        return jsonify({"message": "Skill added to user", "user_id": user.id, "skill_name": skill.name}), 201

class UserSkill(Resource):
    def delete(self, user_id, skill_id):
        user = User.query.get(user_id)
        skill = Skill.query.get(skill_id)
        if skill in user.skills:
            user.skills.remove(skill)
            db.session.commit()
            return jsonify({"message": "Skill removed from user", "user_id": user.id, "skill_id": skill.id}), 200
        else:
            return jsonify({"error": "Skill not found for this user"}), 404