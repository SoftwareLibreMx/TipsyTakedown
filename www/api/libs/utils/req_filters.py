def filter_items(model, query, items: list):
    def get_operations(item):
        operations = {
            'equal': lambda query, field, value: query.filter(field=value),
            'not_equal': lambda query, field, value: query.filter(
                field != value),
            'greater_than': lambda query, field, value: query.filter(
                field > value),
            'greater_than_or_equal': lambda query, field, value: query.filter(
                field >= value),
            'less_than': lambda query, field, value: query.filter(
                field < value),
            'less_than_or_equal': lambda query, field, value: query.filter(
                field <= value),
            'like': lambda query, field, value: query.filter(
                field.like(value)),
            'not_like': lambda query, field, value: query.filter(
                ~field.like(value)),
            'in': lambda query, field, value: query.filter(field.in_(value)),
            'not_in': lambda query, field, value: query.filter(
                ~field.in_(value)),
        }

        return operations.get(item, lambda query, field, value: query)

    for item in items:
        if not hasattr(model, item['field']):
            continue

        field = getattr(model, item['field'])
        operation = get_operations(item['operator'])
        query = operation(query, field, item['value'])

    return query


def process_filters(model, query, filters: dict):
    items = filters.get('items', None)

    if items:
        query = filter_items(model, query, items)

    return query
