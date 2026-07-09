import requests
import urllib.parse

def getCredentials():
    userAgent = "PaperNetworkApp/1.0"
    email = "pottiedsalex@gmail.com"

    return {"Agent": userAgent, "Email": email}

def fetchOpenalexDataDOI(doi, credentials):
    clean_doi = doi.replace("https://doi.org/", "").strip()
    base_url = "https://api.openalex.org/works"
    url = f"https://api.openalex.org/works/https://doi.org/{clean_doi}"
    headers = {"User-Agent": f"{credentials['Agent']} (mailto:{credentials['Email']})"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            title = data.get("title", "Unknown Title")

            authors_list = []
            institution_list = {}
            for authorship in data.get("authorships", []):
                author_name = authorship.get("author", {}).get("display_name", "")
                author_insts = authorship.get("institutions", [])

                if author_name:
                    institutions = []
                    for inst in author_insts:
                        institutions.append(inst.get("display_name", ""))
                    institution_list[author_name] = institutions
                    authors_list.append(author_name)
            authors = ", ".join(authors_list)

            year = data.get("publication_year", None)

            referenced_works = data.get("referenced_works", [])

            reference_dois = []
            formatedRef = []

            if referenced_works:
                chunk_size = 50
                for i in range(0, len(referenced_works), chunk_size):
                    chunk = referenced_works[i:i+chunk_size]
                    ids_filter = "|".join(chunk)

                    ref_url = f"{base_url}?filter=openalex_id:{ids_filter}&per_page={chunk_size}"
                    ref_response = requests.get(ref_url, headers=headers)

                    if ref_response.status_code == 200:
                        ref_data = ref_response.json()
                        # Extract the DOI for each referenced work
                        for work in ref_data.get("results", []):
                            work_doi = work.get("doi")
                            work_year = str(work.get("publication_year"))
                            if work.get("primary_location"):
                                try:
                                    work_journal = work.get("primary_location")["source"]["display_name"]

                                except:
                                    work_journal = '...'
                            else:
                                work_journal = '...'
                            if work.get("authorships"):
                                work_author = work.get("authorships")[0]['author']['display_name']
                            else:
                                work_author = '...'
                            if work_doi:
                                # Clean it up so it's just the raw standard DOI string
                                reference_dois.append(work_doi.replace("https://doi.org/", ""))
                                formatedRef.append(work_author+' et al. '+ '('+work_journal+') DOI: '+work_doi.replace("https://doi.org/", "")+' ('+work_year+').')



            return {
                "Title": title,
                "Authors": authors,
                "Institutions": institution_list,
                "DOI": clean_doi,
                "Year": year,
                "formatedRef": formatedRef,
                "refDOI": reference_dois,
            }
        else:
            print(f"OpenAlex returned status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error querying OpenAlex: {e}")
        return None


def fetchOpenalexDataTitle(title, credentials):
    encoded_title = urllib.parse.quote(title)

    url = f"https://api.openalex.org/works?filter=title.search:{encoded_title}&per_page=3&mailto={credentials['email']}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])

            if not results:
                return None

            top_match = results[0]

            doi_url = top_match.get("doi")

            if doi_url:
                return fetchOpenalexDataDOI(doi_url.replace("https://doi.org/", ""))

        else:
            print("Error Bad response: " + str(response.status_code))

        return None
    except Exception as e:
        print(f"Error searching title: {e}")
        return None