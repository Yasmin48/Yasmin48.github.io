import markdown2
import os
import re

def replace_ticks_for_code(matchobj):
    return '<code>' + matchobj.group(0)[1:-1] + '</code>'

def fix_code_tags(html):
    html = re.sub('`([a-zA-Z]+?)`', replace_ticks_for_code, html)
    return html

# get post text
def get_post_md(post):
    post_path = 'blog/posts/' + post
    with open(post_path, 'r') as post_file:
        post_text = post_file.read()
    return post_text

# get the html of the whole posts page
def get_post_html_and_meta(md_text):
    html = markdown2.markdown(md_text, extras=["tables", "metadata", "fenced-code-blocks"])
    title = html.metadata['title']
    date = html.metadata['date']
    h1 = "<h1>" + title + "</h1>"
    page = header + h1 + html + footer
    return page, title, date

# get the url
def get_url(title):
    url = "-".join(title.split()).lower()
    if url[-1] == "?":
        return url[:-1]
    return url

# write the html file
def write_page_html(page_html, post_url):
    if not os.path.exists(post_url):
        os.makedirs(post_url)
    with open(post_url + '/index.html', 'w') as html_file:
        html_file.write(page_html)

# read file
def get_template(template):
    path = 'blog/templates/' + template + '.html'
    with open(path, 'r') as f:
        file_contents = f.read()
    return file_contents

def get_page_list_unit(post):
    html = "<li><a href=" + post['url'] + ">" + post['title'] + "</li>"
    return html

# makes index.html in root
def make_post_list_page():
    index_html = header + '<ul class="page-list">'
    for post in ordered_posts:
        index_html += get_page_list_unit(post)
    index_html += "</ul>"
    index_html += footer
    with open('index.html', 'w') as index_file:
        index_file.write(index_html)

# takes markdown file name, generates and writes the html file (in appropriate folder), and adds to posts data list
def make_post_page(post):
    print('\n post:', post)
    post_markdown = get_post_md(post)
    page, page_title, post_date =  get_post_html_and_meta(post_markdown)
    page = fix_code_tags(page)
    page_url = get_url(page_title)
    write_page_html(page, page_url)
    posts_data.append({'title': page_title, 'url': page_url, 'date': post_date})


if __name__ == "__main__":

    # get template html
    header = get_template('header')
    footer = get_template('footer')

    # get all posts in the posts folder
    posts = [post for post in os.listdir('blog/posts') if post[:2] != "xx"]

    posts_data = []

    for post in posts:
        make_post_page(post)

    ordered_posts = sorted(posts_data, reverse=True, key=lambda post: post['date'])

    # write post list as index.html in root
    make_post_list_page()

    # updates atom feed - to do"""
