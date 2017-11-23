import requests
import json

# Facebook API path, group_id appears in group URL
# Personal access token can be acquired here: https://developers.facebook.com/tools/accesstoken/
path = "https://graph.facebook.com/v2.9/"
group_id = "YOUR_GROUP_ID"
group_posts_path = "{group_id}/feed/?fields=id".format(group_id=group_id)
access_token = "YOUR_ACCESS_TOKEN"

group_url = "{path}{group_posts_path}&access_token={access_token}".format(
    path=path,
    group_posts_path=group_posts_path,
    access_token=access_token)

url_array = []

# go through all group pagination to get all URLs to scrape
def recurse_pages(url):
    response = requests.get(url)
    json_content = response.json()
    print("Getting next url after {url}".format(url=url))
    if len(json_content["data"]) > 0:
        next_url = json_content["paging"]["next"]
        url_array.append(next_url)
        recurse_pages(next_url)


recurse_pages(group_url)

# serialise URLs to scrape
with open("all_group_urls.json", "w") as fp:
    json.dump(url_array, fp)

all_post_ids = []

# scrape all urls for post IDs
def get_ids(url):
    print("\nGetting IDs for {url}".format(url=url))
    post_ids = []
    response = requests.get(url)
    json_content = response.json()
    data = json_content["data"]
    if len(data) > 0:
        for post in data:
            post_id = post["id"]
            post_ids.append(post_id)
    return post_ids


for url in url_array:
    post_ids = get_ids(url)
    all_post_ids += post_ids

# serialise post IDs
with open("all_group_post_ids.json", "w") as fp:
    json.dump(all_post_ids, fp)

all_post_data = []

# define fields to get from posts
fields = "link,story,message,created_time,from,id,likes,name,permalink_url"

# get all post data from all post IDs
def get_post_data(post_id):
    url = "https://graph.facebook.com/{post_id}?fields={fields}&access_token={access_token}".format(
        post_id=post_id,
        fields=fields,
        access_token=access_token)
    print("\nGetting data from {url}".format(url=url))
    response = requests.get(url)
    data = response.json()
    return data


for post_id in all_post_ids:
    all_post_data.append(get_post_data(post_id))

# serialise post data
with open("all_group_post_data.json", "w") as fp:
    json.dump(all_post_data, fp)
