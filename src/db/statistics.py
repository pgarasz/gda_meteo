from sqlalchemy import select, func


def monthly_avg_rainfall(outpost):

    subq =                                                          \
        select(
            outpost.datetime,
            func.sum(outpost.rain).label('sums'))                   \
        .group_by(
            func.strftime('%Y-%m', outpost.datetime))               \
        .subquery()  # monthly rainfall totals

    query =                                                         \
        select(
            func.strftime('%m', subq.c.datetime)
                .label('month'),
            func.round(func.avg(subq.c.sums), 1)
                .label('rainfall_sum'))                             \
        .group_by(
            func.strftime('%m', subq.c.datetime))

    return query


def monthly_avg_temp(outpost):

    query =                                                         \
        select(
            func.strftime('%m', outpost.datetime)
                .label('month'),
            func.round(func.avg(outpost.temp), 1)
                .label('avg_temp'))                                 \
        .group_by(
            func.strftime('%m', outpost.datetime))                  \

    return query
