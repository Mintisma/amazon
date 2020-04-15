from time import time
from random import randint


def get_url(query, page):
    query = query.replace(' ', '+').replace('_', '+')
    url = 'https://www.amazon.com/s?'

    if randint(0, 1):
        # i
        url += 'i=aps'

    # k
    if 'i=aps' in url:
        url += '&k=' + query
    else:
        url += 'k=' + query

    if page > 1:
        # page
        url += '&page=' + str(page)

    if randint(0, 1):
        # qid
        url += '&qid=' + str(round(time()))

    if randint(0, 1):
        # ref
        if page == 1:
            url += '&ref=nb_sb_noss'
        elif page > 1:
            url += '&ref=sr_pg_' + str(page)
    if randint(0, 1):
        # url
        url += '&url=search-alias'
    return url