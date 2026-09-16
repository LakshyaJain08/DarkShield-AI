import requests

def search_hf_datasets(query):
    url = f"https://huggingface.co/api/datasets?search={query}"
    response = requests.get(url)
    if response.status_code == 200:
        datasets = response.json()
        for ds in datasets:
            print(ds.get('id', 'Unknown'))
    else:
        print("Failed to fetch")

if __name__ == "__main__":
    search_hf_datasets("darkpattern")
    print("---")
    search_hf_datasets("ec-darkpattern")
