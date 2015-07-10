for index, item in enumerate(beatles_results['artists']):
    if index > 0:
        try:
            if item['country'] == 'SP':
                pprint(item)
                break
        except KeyError as ex:
            pprint("item has no country code".format(ex))


for index, item in enumerate(beatles_results['artists'][0]['aliases']):
    if index > 0:
        try:
            if item['locale'] == 'es':
                pprint(item)
                break
        except KeyError as ex:
            pprint("item has no country code".format(ex))

