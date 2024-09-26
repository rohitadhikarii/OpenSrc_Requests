import requests
import creds

""" Initialize your personal github api key in a seperate file called 'creds.py '"""


headers = {
    'Authorization': f'Token {creds.token}',
    'Accept': 'application/vnd.github.v3+json'
}

def fetch_projects(keywords, page=1):
    query = '+'.join([f'topic:{keyword}' for keyword in keywords])
    url = f'https://api.github.com/search/repositories?q={query}&page={page}'

    response = requests.get(url, headers=headers)
    return response.json()

def main():
    keywords = input("Enter specific keywords (separated by commas): ").split(",")
    keywords = [keyword.strip() for keyword in keywords]

    page = 1 
    total_projects = 0
    limit_projects = 10 

    while True:
        data = fetch_projects(keywords, page)
        if 'items' not in data or not data['items']:
            print("No desired projects to work on.")
            break  

        for i, project in enumerate(data['items']):
            check_description = project['description'] or '' 
            check_description = check_description.lower()
            if any(keyword.lower() in check_description for keyword in keywords):
                print(f"{i + 1} - Project Name: {project['name']}")
                print(f"URL: {project['html_url']}")
                print(f"Description: {project['description']}")
                for _ in range(2):
                    print() 

        total_projects += len(data['items'])        

        if total_projects >= limit_projects:
            user_input = input("Press 'Enter' to load more projects or type 'exit' to exit out: ")
            if user_input.lower() == "exit":
                return
            else:
                page += 1  
        else:
            break  
if __name__ == "__main__":
    main()