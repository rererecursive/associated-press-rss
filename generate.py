#!/usr/bin/python3
from jinja2 import Template

config = {'config': [
    {
        'name':  'Top News',
        'url':   'topnews'
    },
    {
        'name':  'Sports',
        'url':   'sports'
    },
    {
        'name':  'Entertainment',
        'url':   'entertainment'
    },
    {
        'name':  'Oddities',
        'url':   'oddities'
    },
    {
        'name':  'Travel',
        'url':   'travel'
    },
    {
        'name':  'Lifestyle',
        'url':   'lifestyle'
    },
    {
        'name':  'US News',
        'url':   'usnews'
    },
    {
        'name':  'Health',
        'url':   'Health'
    },
    {
        'name':  'Science',
        'url':   'science'
    },
    {
        'name':  'International News',
        'url':   'intlnews'
    },
    {
        'name':  'Politics',
        'url':   'politics'
    },
    {
        'name':  'Religion',
        'url':   'religion'
    }
]}

file = open('template.yaml').read()
content = Template(file).render(config)
print(content)
