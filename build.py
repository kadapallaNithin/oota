bootstrap_css_link = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">'
remove_bs_css_link = '<link rel="stylesheet" type="text/css" href="{% static \'home/bs/css/bootstrap.css\' %}" >'
remove_jquery_link = '<script src="{% static \'home/jquery/jquery-3.4.1.min.js\' %}"></script>'
rm_bs_js_link = '<script src="{% static \'home/bs/js/bootstrap.min.js\' %}"></script>'
jq_link = '<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>'
bs_link = '<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>'
base_path = 'oota/home/templates/home/base.html'
base = open(base_path).read()
f = open(base_path,'w')
f.write(base.replace(remove_bs_css_link, bootstrap_css_link).replace(remove_jquery_link,jq_link).replace(rm_bs_js_link,bs_link))
f.close()