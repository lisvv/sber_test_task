import datetime
from typing import Union

from core.normalizer import get_normalized_month
from dateutil.relativedelta import relativedelta
from db.models import Breed, Kitty, db
from flask import url_for
from flask_admin import Admin, form
from flask_admin.babel import lazy_gettext
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_babelex import Babel
from flask_sqlalchemy import BaseQuery
from jinja2.runtime import Context
from markupsafe import Markup
from sqlalchemy import func, or_
from sqlalchemy.orm import InstrumentedAttribute
babel = Babel()



class BreedView(sqla.ModelView):
    column_list = ("name",)


class AgeFilter(filters.BaseSQLAFilter):
    def __init__(
        self,
        column: Union[InstrumentedAttribute, datetime.date],
        name: str,
        options: str = None,
        data_type: str = None,
    ) -> None:
        self.options = options
        super(AgeFilter, self).__init__(name, options, data_type)

        self.column = column

    def get_options(self, view: "KittyView") -> tuple[tuple[str, str], ...]:
        return (
            ("1", "менее месяца"),
            ("2", "до 2 месяцев"),
            ("3", "до 3 месяцев"),
            ("4", "до 4 месяцев"),
            ("5", "до 5 месяцев"),
            ("6", "до 6 месяцев"),
            ("7", "до 7 месяцев"),
            ("8", "до 8 месяцев"),
            ("9", "до 9 месяцев"),
            ("10", "до 10 месяцев"),
            ("11", "до 11 месяцев"),
            ("12", "год и более"),
        )

    def apply(self, query: BaseQuery, value: str, alias=None) -> BaseQuery:
        searching_birthday = datetime.datetime.now() - relativedelta(months=int(value))
        return query.filter(Kitty.birthday >= searching_birthday)

    def operation(self) -> str:
        return lazy_gettext("Возраст")


class KittyView(sqla.ModelView):
    form_extra_fields = {
        "image": form.ImageUploadField(
            "Фото",
            base_path="static",
            max_size=(500, 500, False),
            thumbnail_size=(500, 500, False),
        )
    }
    form_widget_args = {"description": {"rows": 40, "style": "color: black"}}
    page_size = 5
    column_filters = (
        "name",
        "description",
        AgeFilter(column=Kitty.birthday, name="возраст до", options="Возраст"),
    )
    column_searchable_list = ("name",)
    column_sortable_list = (("breed", "breed.name"), "birthday", "name")
    column_list = ("breed", "name", "birthday", "image", "description")
    column_labels = dict(
        breed="Порода",
        name="Кличка",
        description="Описание",
        image="Фото",
        birthday="Возраст",
    )

    def _list_thumbnail(
        self, context: Context, model: Kitty, name: str
    ) -> Markup or str:
        if not model.image:
            return ""
        image_url = url_for("static", filename=model.image)
        return Markup(f'<img src="{image_url}" width="250" height="250">')

    def _birthday_to_age(self, context: Context, model: Kitty, name: str) -> str:
        birthday = model.birthday
        age = relativedelta(dt1=datetime.datetime.now().date(), dt2=birthday)
        normalized_month = get_normalized_month(age.months + age.years * 12)
        return normalized_month

    def _breed(self, context: Context, model: Kitty, name: str) -> str:
        return model.breed.name


    column_formatters = {
        "image": _list_thumbnail,
        "birthday": _birthday_to_age,
        "breed": _breed,
    }

    column_formatters_detail = ("name", "description")

    def _apply_search(
        self,
        query: BaseQuery,
        count_query: BaseQuery,
        joins: dict,
        count_joins: dict,
        search: str,
    ):
        if not search:
            return super(KittyView, self)._apply_search(
                query, count_query, joins, count_joins, search
            )

        query = Kitty.fulltext_search(search)

        count_filter_stmt = []
        count_query = self.session.query(func.count("*")).select_from(query)

        if count_query is not None:
            count_query = count_query.filter(or_(*count_filter_stmt))

        return query, count_query, joins, count_joins

    def search_placeholder(self) -> str:
        return "FTS, имя, порода, описание"


admin = Admin(template_mode='bootstrap4')
admin.add_view(KittyView(Kitty, db.session, "Котята"))
admin.add_view(BreedView(Breed, db.session, "Порода"))
