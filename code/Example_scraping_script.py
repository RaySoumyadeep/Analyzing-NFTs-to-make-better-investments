import re
from bs4 import BeautifulSoup

html_doc = """
<html>
<body>
<span class="blue">here is a lot of text that i don't need</span>
<span class="blue">this is the span i need because it contains 04/18/13 7:29pm</span>
<span class="blue">04/19/13 7:30pm</span>
<span class="blue">Posted on 04/20/13 10:31pm</span>
</body>
</html>
"""# parse the html
soup = BeautifulSoup(html_doc)

# find a list of all span elements
spans = soup.find_all('span', {'class' : 'blue'})

# create a list of lines corresponding to element texts
lines = [span.get_text() for span in spans]

# collect the dates from the list of lines using regex matching groups
found_dates = []
for line in lines:
    m = re.search(r'(\d{2}/\d{2}/\d{2} \d+:\d+[a|p]m)', line)
    if m:
        found_dates.append(m.group(1))

# print the dates we collected
for date in found_dates:
    print(date)