from sqlalchemy import select, func, case, cast, Float


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


def wind_rose(outpost):

    angle = outpost.winddir
    lvl = outpost.windlevel

    whens_angle = {
        ((angle >= 0) & (angle < 11.25)): 'N',
        ((angle >= 11.25) & (angle < 33.75)): 'NNE',
        ((angle >= 33.75) & (angle < 56.25)): 'NE',
        ((angle >= 56.25) & (angle < 78.75)): 'ENE',
        ((angle >= 78.75) & (angle < 101.25)): 'E',
        ((angle >= 101.25) & (angle < 123.75)): 'ESE',
        ((angle >= 123.75) & (angle < 146.25)): 'SE',
        ((angle >= 146.25) & (angle < 168.75)): 'SSE',
        ((angle >= 168.75) & (angle < 191.25)): 'S',
        ((angle >= 191.25) & (angle < 213.75)): 'SSW',
        ((angle >= 213.75) & (angle < 236.25)): 'SW',
        ((angle >= 236.25) & (angle < 258.75)): 'WSW',
        ((angle >= 258.75) & (angle < 281.25)): 'W',
        ((angle >= 281.25) & (angle < 303.75)): 'WNW',
        ((angle >= 303.75) & (angle < 326.25)): 'NW',
        ((angle >= 326.25) & (angle < 348.75)): 'NNW',
        ((angle >= 348.75) & (angle <= 360)): 'N'
    }

    whens_lvl = {
        (lvl == 0): "c",
        ((lvl > 0) & (lvl < 1)): "0-1",
        ((lvl >= 1) & (lvl < 3)): "1-3",
        ((lvl >= 3) & (lvl < 5)): "3-5",
        ((lvl >= 5) & (lvl < 8)): "5-8",
        ((lvl >= 8) & (lvl < 11)): "8-11",
        ((lvl >= 11) & (lvl < 18)): "11-18",
        ((lvl >= 18) & (lvl < 30)): "18-30",
        (lvl >= 30): ">=30",
    }

    total =                                                          \
        select(
            cast(func.count(lvl), Float).label("total"))             \
        .where(angle != None)                                        \
        .subquery()

    query =                                                          \
        select(
            case(whens_angle, else_=None).label("direction"),
            case(whens_lvl, else_=None).label("strength"),
            func.count().label("count"),
            cast(func.count() / total * 100, Float)
                .label("frequency"))                                \
        .where(angle != None)                                       \
        .group_by("direction", "strength")                          \
        .order_by("direction", "strength")

    return query

# It's necessary to pass output of arithmetic on columns to
# a function like cast, so it can be labeled.
# Otherwise current version of sqlalchemy_utils_create_view raises an error.