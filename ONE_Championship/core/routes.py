from flask import Blueprint, render_template, request
from ..extensions import db
from ..models import Fighter, Division

core_bp = Blueprint(
    "core",
    __name__,
    template_folder="templates"
)

@core_bp.route("/")
def index():

    page = request.args.get("page", 1, type=int)

    fighters = db.paginate(
        db.select(Fighter),
        per_page=4,
        page=page
    )

    return render_template(
        "core/index.html",
        title="Home Page",
        fighters=fighters
    )


@core_bp.route("/fighter/<int:id>")
def detail(id):

    fighter = db.session.get(Fighter, id)

    return render_template(
        "core/fighter_detail.html",
        title="Fighter Detail",
        fighter=fighter
    )