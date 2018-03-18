from SPARQLWrapper import SPARQLWrapper, JSON

'''
The image module is a required dependency of pygame,
but it only optionally supports any extended file formats.
By default it can only load uncompressed BMP images.
When built with full image support, the pygame.image.load() function can support the following formats.
JPG
PNG
GIF (non-animated)
BMP
PCX
TGA (uncompressed)
TIF
LBM (and PBM)
PBM (and PGM, PPM)
XPM

By default wikidata returns
image filename with one of these extensions:
jpg, jpeg, jpe, png, svg, tif, tiff, gif, xcf, pdf, webp or djvu (case insensitive) (English)
(?:i).+\.(jpg|jpeg|jpe|png|svg|tif|tiff|gif|xcf|pdf|djvu|webp)

we want only supported formats:
(?:i).+\.(jpg|jpeg|jpe|png|tif|tiff|gif)
'''


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
