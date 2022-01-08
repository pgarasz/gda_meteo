from dash.dependencies import Input, Output

from dashboard.index import app
from dashboard.elements import outpost_figures, compare_outposts, missing_page_error, welcome_txt

from db import connect_engine
from db.utils import DBInfo

engine = connect_engine()
db_info = DBInfo(engine)


@app.callback(Output("content", "children"),
              Input("url", "pathname"),
              Input('url', "hash")
              )
def render_page_content(pathname, hash, engine=engine):

    if pathname == "/":
        return welcome_txt
    elif pathname == "/compare":
        return compare_outposts(db_info.outposts, engine)
    elif "/outpost" in pathname:
        outpost_no = hash.removeprefix('#')

        if outpost_no in db_info.outpost_ids:
            outpost_name = db_info.get_outpost_name(
                outpost_no)  # TODO Optymalizacja
            return outpost_figures(outpost_no, outpost_name, engine)

    return missing_page_error


@app.callback(Output('left_column', 'children'),
              Input('left_dropdown', 'value'))
def get_outpost_figures_left_col(outpost_no, engine=engine):
    if outpost_no:
        outpost_name = db_info.get_outpost_name(outpost_no)
        return outpost_figures(outpost_no, outpost_name, engine)


@app.callback(Output('right_column', 'children'),
              Input('right_dropdown', 'value'))
def get_outpost_figures_right_col(outpost_no, engine=engine):
    if outpost_no:
        outpost_name = db_info.get_outpost_name(outpost_no)
        return outpost_figures(outpost_no, outpost_name, engine)
