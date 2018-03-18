from SPARQLWrapper import SPARQLWrapper, JSON

def getRealSites():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery("""
        SELECT ?site ?siteLabel ?image WHERE
        {
            ?site wdt:P1435 wd:Q10729054.
            ?site wdt:P18 ?image.
            ?site wdt:P131 wd:Q123709.
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }""")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    sites = []

    for result in results["results"]["bindings"]:
        sites.append((result["siteLabel"]["value"], result["image"]["value"]))

    return sites

def getFakeSites():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery("""
        SELECT ?site ?siteLabel ?image WHERE
        {
            ?site wdt:P1435 wd:Q10729054.
            ?site wdt:P18 ?image.
            MINUS { ?site wdt:P131 wd:Q123709. }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }""")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    sites = []

    for result in results["results"]["bindings"]:
        sites.append((result["siteLabel"]["value"], result["image"]["value"]))

    return sites
