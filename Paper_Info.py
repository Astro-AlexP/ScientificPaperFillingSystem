import requests
import urllib.parse


def fetch_openalex_data(doi):
    clean_doi = doi.replace("https://doi.org/", "").strip()
    base_url = "https://api.openalex.org/works"
    url = f"https://api.openalex.org/works/https://doi.org/{clean_doi}"
    headers = {"User-Agent": "PaperNetworkApp/1.0 (mailto:pottiedsalex@gmail.com)"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            title = data.get("title", "Unknown Title")

            authors_list = []
            for authorship in data.get("authorships", []):
                author_name = authorship.get("author", {}).get("display_name", "")
                if author_name:
                    authors_list.append(author_name)
            authors = ", ".join(authors_list)

            year = data.get("publication_year", None)

            referenced_works = data.get("referenced_works", [])

            reference_dois = []

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
                            if work_doi:
                                # Clean it up so it's just the raw standard DOI string
                                reference_dois.append(work_doi.replace("https://doi.org/", ""))


            return {
                "title": title,
                "authors": authors,
                "year": year,
                "citations": reference_dois,
            }
        else:
            print(f"OpenAlex returned status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error querying OpenAlex: {e}")
        return None


def find_doi_by_title_openalex(title, email="your_email@example.com"):
    encoded_title = urllib.parse.quote(title)

    url = f"https://api.openalex.org/works?filter=title.search:{encoded_title}&per_page=3&mailto={email}"
    print('here')

    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])

            if not results:
                return None

            top_match = results[0]

            doi_url = top_match.get("doi")

            if doi_url:
                return doi_url.replace("https://doi.org/", "")

        else:
            print("Error Bad response: " + str(response.status_code))

        return None
    except Exception as e:
        print(f"Error searching title: {e}")
        return None


if __name__ == "__main__":

    DOI = find_doi_by_title_openalex('An introduction to Bayesian inference in gravitational-wave astronomy')
    if DOI is not None:
        result = fetch_openalex_data(DOI)

    if result:
        print(f"Title: {result['title']}\n")
        print(f"Authors: {result['authors'][:100]}...\n")
        #print(f"Global Citations: {result['node_size_weight']}\n")
        print(f"First 5 referenced work IDs (Edges): {result['citations'][:5]}")