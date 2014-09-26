from django.db import connection

from aoasurveys.aoaforms.models import FormEntry


class SmartRawQuery(object):
    def __init__(self, query, model, field_map):
        self.query = query
        self.model = model
        self.field_map = field_map
        self._raw_query = None

    def __iter__(self):
        if self._raw_query is None:
            self._raw_query = self.model.objects.raw(self.query)

        return self._raw_query.__iter__()

    def __getitem__(self, item):
        return list(self)[item]

    def count(self):
        count_query = (
            self.query
            .replace('f.id', 'COUNT(f.id)', 1)
            .replace('GROUP BY f.id', '')
        )
        cursor = connection.cursor()
        cursor.execute(count_query)
        return cursor.fetchone()[0]

    def order_by(self, column):
        if column.startswith('-'):
            column = column[1:]
            order = 'DESC'
        else:
            order = 'ASC'

        ob_query = " ORDER BY f{index}.value {order}".format(
            index=self.field_map[column],
            order=order)
        self.query += ob_query
        return self


def filter_entries(form, filters):
    query = "SELECT f.id FROM aoaforms_formentry f "
    field_map = {}
    index = 0
    extra_fields = [
        str(field.id) for field in form.visible_fields
        if str(field.id) not in filters
    ]
    for field_id in filters:
        if field_id not in field_map:
            field_map[field_id] = index
            index += 1
    for field_id in extra_fields:
        if field_id not in field_map:
            field_map[field_id] = index
            index += 1
    for key, value in filters.iteritems():
        query += (
            "JOIN aoaforms_fieldentry f{index} ON f{index}.entry_id=f.id "
            "AND f{index}.field_id='{key}' "
        )
        if isinstance(value, list):
            query += "AND ("
            query += " OR ".join([
                "f{index}.value LIKE '%%{choice}%%'".format(index=index,
                                                            choice=choice)
                for choice in value])
            query += ") "
        else:
            query += "AND f{index}.value LIKE '%%{value}%%' "

        query = query.format(index=field_map[key], key=key, value=value)
    for field in extra_fields:
        query += (
            "JOIN aoaforms_fieldentry f{index} ON f{index}.entry_id=f.id "
            "AND f{index}.field_id='{field}' "
        ).format(index=field_map[field], field=field)

    query += " WHERE f.form_id='{form_id}' ".format(form_id=form.id)

    if filters:
        query += "GROUP BY f.id"

    return SmartRawQuery(query, FormEntry, field_map)
