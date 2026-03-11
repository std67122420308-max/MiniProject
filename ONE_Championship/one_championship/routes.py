from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..extensions import db
from ..models import Fighter, Division
from flask_login import login_required, current_user

fighter_bp = Blueprint(
    "fighter",
    __name__,
    template_folder="templates"
)

@fighter_bp.route("/")
@login_required
def index():
    fighters = db.session.scalars(
        db.select(Fighter).where(Fighter.user == current_user)
    ).all()

    return render_template(
        "one_championship/index.html",
        title="ONE Championship Fighters",
        fighters=fighters
    )

@fighter_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_fighter():
    divisions = db.session.scalars(
        db.select(Division)
    ).all()

    if request.method == "POST":
        name = request.form.get("name")
        height = request.form.get("height")
        weight = request.form.get("weight")
        age = request.form.get("age")
        country = request.form.get("country")
        team = request.form.get("team")
        description = request.form.get("description")
        img_url = request.form.get("img_url")

        division_id = int(request.form.get("division", 0))
        user_id = current_user.id

        fighter = db.session.scalar(
            db.select(Fighter).where(Fighter.name == name)
        )
        if fighter:
            flash(f"Fighter: {name} already exists!", "warning")
            return redirect(url_for("fighter.new_fighter"))
        new_fighter = Fighter(
            name=name,
            height=height,
            weight=weight,
            age=age,
            country=country,
            team=team,
            description=description,
            img_url=img_url,
            division_id=division_id,
            user_id=user_id
        )

        db.session.add(new_fighter)
        db.session.commit()
        
        flash("Add new fighter successful!", "success")
        return redirect(url_for("fighter.index"))
    
    return render_template(
        "one_championship/new_fighter.html",
        title="Add Fighter",
        divisions=divisions
    )


@fighter_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_fighter(id):
    fighter = db.session.get(Fighter, id)
    if not fighter:
        flash("Fighter not found", "danger")
        return redirect(url_for("fighter.index"))
    if request.method == "POST":
        fighter.name = request.form.get("name")
        fighter.height = request.form.get("height")
        fighter.weight = request.form.get("weight")
        fighter.age = request.form.get("age")
        fighter.country = request.form.get("country")
        fighter.team = request.form.get("team")
        fighter.description = request.form.get("description")

        db.session.commit()

        flash("Update fighter successful!", "success")
        return redirect(url_for("fighter.index"))

    return render_template(
        "one_championship/edit_fighter.html",
        title="Edit Fighter",
        fighter=fighter
    )

@fighter_bp.route("/delete/<int:id>")
@login_required
def delete_fighter(id):
    fighter = db.session.get(Fighter, id)
    if not fighter:
        flash("Fighter not found", "danger")
        return redirect(url_for("fighter.index"))

    db.session.delete(fighter)
    db.session.commit()

    flash("Delete fighter successful!", "success")
    return redirect(url_for("fighter.index"))

@fighter_bp.route("/search")
@login_required
def search():
    keyword = request.args.get("q", "")
    fighters = db.session.scalars(
        db.select(Fighter).where(Fighter.name.contains(keyword))
    ).all()
    return render_template(
        "one_championship/index.html",
        title="Search Result",
        fighters=fighters
    )