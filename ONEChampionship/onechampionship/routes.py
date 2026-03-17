from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from ONEChampionship.extensions import db
from ONEChampionship.models import ONEChampionship, Team
from flask_login import login_required, current_user

ONEChampionship_bp = Blueprint(
    "ONEChampionship",
    __name__,
    template_folder="templates"
)

@ONEChampionship_bp.route("/")
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

    fighters = db.paginate(query, per_page=4, page=page)

    return render_template(
        "ONEChampionship/index.html",
        title="Fighter Page",
        ONEChampionships=fighters
    )

@ONEChampionship_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_ONEChampionship():

    teams = db.session.scalars(db.select(Team)).all()

    if request.method == "POST":

        name = request.form.get("name")
        age = request.form.get("age", type=int)
        height = request.form.get("height")
        country = request.form.get("country")
        weight_class = request.form.get("weight_class")
        gym = request.form.get("gym")
        description = request.form.get("description")
        image = request.form.get("image")

        if not name:
            flash("Name is required!", "danger")
            return redirect(url_for("ONEChampionship.new_ONEChampionship"))

        existing = db.session.scalar(
            db.select(ONEChampionship).where(
                ONEChampionship.name == name
            )
        )

        if existing:
            flash(f"Fighter {name} already exists!", "warning")
            return redirect(url_for("ONEChampionship.new_ONEChampionship"))

        team_ids = request.form.getlist("teams")
        selected_teams = []

        for team_id in team_ids:
            team = db.session.get(Team, int(team_id))
            if team:
                selected_teams.append(team)

        new_fighter = ONEChampionship(
            name=name,
            age=age,
            height=height,
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
        return redirect(url_for("ONEChampionship.index"))

    return render_template(
        "ONEChampionship/new_ONEChampionship.html",
        title="New Fighter",
        teams=teams
    )

@ONEChampionship_bp.route("/detail/<int:id>")
def detail_ONEChampionship(id):

    fighter = db.session.get(ONEChampionship, id)

    if not fighter:
        abort(404)

    return render_template(
        "ONEChampionship/detail.html",
        title=fighter.name,
        fighter=fighter
    )

@ONEChampionship_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_ONEChampionship(id):

    fighter = db.session.get(ONEChampionship, id)

    if not fighter:
        abort(404)

    if fighter.user_id != current_user.id:
        abort(403)

    teams = db.session.scalars(db.select(Team)).all()

    if request.method == "POST":

        fighter.name = request.form.get("name")
        fighter.age = request.form.get("age", type=int)
        fighter.height = request.form.get("height")
        fighter.country = request.form.get("country")
        fighter.weight_class = request.form.get("weight_class")
        fighter.gym = request.form.get("gym")
        fighter.description = request.form.get("description")
        fighter.image = request.form.get("image")

        team_ids = request.form.getlist("teams")
        fighter.teams.clear()

        for team_id in team_ids:
            team = db.session.get(Team, int(team_id))
            if team:
                fighter.teams.append(team)

        db.session.commit()

        flash("Fighter updated!", "success")
        return redirect(url_for("ONEChampionship.detail_ONEChampionship", id=id))

    return render_template(
        "ONEChampionship/edit_ONEChampionship.html",
        fighter=fighter,
        teams=teams,
        title="Edit Fighter"
    )

@ONEChampionship_bp.route("/delete/<int:id>")
@login_required
def delete_ONEChampionship(id):

    fighter = db.session.get(ONEChampionship, id)

    if not fighter:
        abort(404)

    if fighter.user_id != current_user.id:
        abort(403)

    db.session.delete(fighter)
    db.session.commit()

    flash("Fighter deleted!", "danger")

    return redirect(url_for("ONEChampionship.index"))