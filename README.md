# RSS feeds for Associated Press
Associated Press no longer offers their content via RSS. This repo contains code to extract the data from the site and convert it into RSS form.

A working version is hosted on AWS: topics for each feed can be found at:\
http://associated-press.s3-website-us-east-1.amazonaws.com \
Each file is updated hourly.

For example, if you are using Slack, you can type:\
`/feed http://associated-press.s3-website-us-east-1.amazonaws.com/topnews.xml`\
to subscribe to the Top News stories.
