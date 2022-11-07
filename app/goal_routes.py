from flask import Blueprint
from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
import datetime as dt

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

#validate function 
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


#CREATE goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    try:
        new_goal = Goal.from_dict(request_body)

    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400)) 

    db.session.add(new_goal)
    db.session.commit()

    return {"goal":new_goal.to_dict()},201


# GET all goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response)


# Get goal: Get one goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal":goal.to_dict()}


#Update goal: Update one goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal":goal.to_dict()}