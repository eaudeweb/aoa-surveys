from aoasurveys.aoaforms.models import FormEntry


def filter_entries(form, filters):
    query = "SELECT f.entry_id AS id FROM aoaforms_fieldentry f "
    index = 0
    for key, value in filters.iteritems():
        query += (
            "JOIN aoaforms_fieldentry f{index} ON f{index}.entry_id=f.entry_id "
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
    query += "GROUP BY f.entry_id"

    if filters:
        raw = FormEntry.objects.raw(query)
        raw.count = lambda: len(list(raw))
        raw.order_by = lambda b: raw # FIXME: actual ordering
        return raw

    return form.entries.all()
