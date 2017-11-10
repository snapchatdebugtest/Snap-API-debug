import random
from pathlib import Path

from flask import Blueprint, Markup, render_template, current_app
from flask_cachecontrol import cache_for
from markdown import markdown

from ._utils import samples


blueprint = Blueprint('index-page', __name__)


@blueprint.route("/")
@cache_for(hours=12)
def get():
    template_images = list(samples(blank=True))
    return render_template(
        "index.html",
        template_images=template_images,
        default_template=random.choice(template_images)['key'],
        readme=_load_readme(),
        config=current_app.config,
    )


def _load_readme():
    path = Path(current_app.config['ROOT'], 'README.md')
    with path.open() as f:
        text = f.read()
        content = text.split('<!--content-->')[-1]
        html = markdown(content, extensions=['tables', 'pymdownx.magiclink'])
        return Markup(html)
