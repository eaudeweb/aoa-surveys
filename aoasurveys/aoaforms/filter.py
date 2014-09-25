from django.db import connection

from aoasurveys.aoaforms.models import FormEntry


def filter_entries(form, filters):
    query = "SELECT f.id FROM aoaforms_formentry f "
    index = 0
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

        query = query.format(index=index, key=key, value=value)
        index += 1
    query += "GROUP BY f.id"

    if filters:
        raw = FormEntry.objects.raw(query)
        cursor = connection.cursor()
        cursor.execute(
            query
            .replace('f.id', 'COUNT(f.id)', 1)
            .replace('GROUP BY f.id', '')
        )
        count = cursor.fetchone()[0]
        raw.count = lambda: count
        raw.order_by = lambda b: raw  # FIXME: actual ordering
        return raw

    return form.entries.all()
