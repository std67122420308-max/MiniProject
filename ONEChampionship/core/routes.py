from flask import Blueprint, render_template, request
from ONEChampionship.extensions import db
from ONEChampionship.models import ONEChampionship

core_bp = Blueprint(
    "core",
    __name__,
    template_folder="templates"
)

@core_bp.route("/")
def index():

    page = request.args.get("page", default=1, type=int)

    ONEChampionships = db.paginate(
        db.select(ONEChampionship).order_by(ONEChampionship.id),
        page=page,
        per_page=4
    )

    return render_template(
        "core/index.html",
        ONEChampionships=ONEChampionships
    )