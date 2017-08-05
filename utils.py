import pycountry
from palettable.colorbrewer.sequential import OrRd_9

COLOR_SCHEME = OrRd_9


def get_alpha3_country_code(code):
    """
        converts iso alpha2 to iso alpha3 country code. Ex.: RU ->RUS , US-> USA, UA -> UKR
    """
    try:
        if pycountry.countries.lookup(code):
            return pycountry.countries.lookup(code).alpha_3
    except LookupError:
        try:
            if pycountry.countries.lookup(code):
                return pycountry.countries.lookup(code).alpha_3
        except LookupError as e:
            print(e)
            return None


def add_lendprojectcost_sum(grouped_query):
    """
        adds totalcost value of lendprojectcost for each country in grouped by countries query
    """
    lendproject_sums = {}

    for countrycode, country_value in grouped_query.items():
        for countryname, value_array in country_value.items():
            for item in value_array:
                if lendproject_sums.get(countrycode):
                    lendproject_sums[countrycode] += int(item['lendprojectcost'])
                else:
                    lendproject_sums[countrycode] = int(item['lendprojectcost'])

    for countrycode in grouped_query.keys():
        grouped_query[countrycode]['totalcost'] = lendproject_sums[countrycode]

    return grouped_query


def group_projects_by_countries(query):
    """
        groups projects by country code
    """
    grouped_query = dict()
    for country in query:
        if grouped_query.get(country['countrycode']):
            grouped_query[country['countrycode']][country['countryname']].append(
                {k: v for k, v in country.items() if k != 'countrycode' and k != "countryname"})
        else:
            grouped_query[country['countrycode']] = {country['countryname']: []}
            grouped_query[country['countrycode']][country['countryname']].append(
                {k: v for k, v in country.items() if k != 'countrycode' and k != 'countryname'})

    return grouped_query


def add_colorfills(country_code_cost_list):
    """
        add color for each country code from color range
    """
    colorscheme = COLOR_SCHEME
    color_range = len(country_code_cost_list) // len(colorscheme.hex_colors) + 1
    color_pointer = 0

    # assigning color for each country ( fillColor value)
    for index, country in enumerate(country_code_cost_list):
        if index > 0 and index % color_range == 0:
            color_pointer += 1
        list(country.values())[0]['fillColor'] = colorscheme.hex_colors[color_pointer]

    # repack list of dicts to dict
    country_code_cost_list = {list(country.keys())[0]: list(country.values())[0] for country in country_code_cost_list}
    return country_code_cost_list


def get_totalcost_fillcolor_allocation(grouped_query):
    """
     returns list of dicts with countrycode key and totalcost , colorFill values for country
    """
    # list of dicts {'countrycode':{'totalcost':123} }
    country_code_cost_list = [{country_code: {'totalcost': country_values['totalcost']}} for
                              country_code, country_values in grouped_query.items()]
    # ascending sort by totalcost value
    country_code_cost_list.sort(key=lambda x: list(x.values())[0]['totalcost'])

    cost_color_allocation = add_colorfills(country_code_cost_list)
    return cost_color_allocation
