import requests

#requests.packages.urlib3.disable_warnings(requests.packages.urlib3.exceptions.InsecureRequestWarning)

response = requests.post("https://www.cyberdiscovery.rocks/cs/2/tutorial-result.php", verify=False)
print response

