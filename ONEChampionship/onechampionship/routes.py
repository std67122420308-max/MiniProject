from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from onechampionship.extensions import db
from onechampionship.models import ONEChampionship, Team
from flask_login import login_required, current_user


onechampionship_bp = Blueprint(
    "onechampionship",
    __name__,
    template_folder="templates"
)

@onechampionship_bp.route("/")
def index():

    page = request.args.get("page", 1, type=int)

    if current_user.is_authenticated:
        query = db.select(ONEChampionship).where(
            ONEChampionship.user_id == current_user.id
        ).order_by(ONEChampionship.created_at.desc())

    else:
        query = db.select(ONEChampionship).order_by(
            ONEChampionship.created_at.desc()
        )

    onechampionships = db.paginate(
        query,
        per_page=4,
        page=page
    )

    return render_template(
        "onechampionship/index.html",
        title="Fighter Page",
        onechampionships=onechampionships
    )

@onechampionship_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_onechampionship():

    teams = db.session.scalars(db.select(Team)).all()

    if request.method == "POST":

        name = request.form.get("name")
        age = request.form.get("age")
        country = request.form.get("country")
        weight_class = request.form.get("weight_class")
        gym = request.form.get("gym")
        description = request.form.get("description")
        image = request.form.get("image")

        team_ids = request.form.getlist("teams")

        selected_teams = []
        for team_id in team_ids:
            team = db.session.get(Team, team_id)
            if team:
                selected_teams.append(team)

        existing = db.session.scalar(
            db.select(ONEChampionship).where(
                ONEChampionship.name == name
            )
        )

        if existing:
            flash(f"Fighter {name} already exists!", "warning")
            return redirect(url_for("onechampionship.new_onechampionship"))

        new_fighter = ONEChampionship(
            name=name,
            age=age,
            country=country,
            weight_class=weight_class,
            gym=gym,
            description=description,
            image=image,
            user_id=current_user.id,
            teams=selected_teams
        )

        db.session.add(new_fighter)
        db.session.commit()

        flash("Fighter added successfully!", "success")
        return redirect(url_for("onechampionship.index"))

    return render_template(
        "onechampionship/new_onechampionship.html",
        title="New Fighter",
        teams=teams
    )

@onechampionship_bp.route("/detail/<int:id>")
def detail_onechampionship(id):

    fighter = db.session.get(ONEChampionship, id)

    if not fighter:
        abort(404)

    return render_template(
        "onechampionship/detail.html",
        title=fighter.name,
        fighter=fighter
    )

@onechampionship_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_onechampionship(id):

    fighter = db.session.get(ONEChampionship, id)

    if not fighter:
        abort(404)

    if fighter.user_id != current_user.id:
        abort(403)

    if request.method == "POST":

        fighter.name = request.form.get("name")
        fighter.age = request.form.get("age")
        fighter.country = request.form.get("country")
        fighter.weight_class = request.form.get("weight_class")
        fighter.gym = request.form.get("gym")
        fighter.description = request.form.get("description")
        fighter.image = request.form.get("image")

        db.session.commit()

        flash("Fighter updated!", "success")
        return redirect(url_for("onechampionship.index"))

    return render_template(
        "onechampionship/edit_onechampionship.html",
        fighter=fighter,
        title="Edit Fighter"
    )

@onechampionship_bp.route("/delete/<int:id>")
@login_required
def delete_onechampionship(id):

    fighter = db.session.get(ONEChampionship, id)

    if not fighter:
        abort(404)

    if fighter.user_id != current_user.id:
        abort(403)

    db.session.delete(fighter)
    db.session.commit()

    flash("Fighter deleted!", "danger")

    return redirect(url_for("onechampionship.index"))