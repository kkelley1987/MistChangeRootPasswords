import requests
import getpass

#get some variables from user
#maybe we build this part custom for each customer?  Will custom build it for ePlus!
print("Input your Organization ID")
org_id = input()
print("Input your API Key")
api_key = input()


# Prompt user to enter a new password
print("Input the new switch root password for all sites in the organization.")
new_password = getpass.getpass()

##Verify the new password
verify_password = getpass.getpass("Verify password: ")
while new_password != verify_password:
    print("Passwords do not match. Please try again.")
    new_password = getpass.getpass("Enter a new password: ")
    verify_password = getpass.getpass("Verify password: ")

#build auth header
headers = {"Authorization": f"Bearer {api_key}"}
body = {"root_password": new_password}

# Make the API request to get the list of all sites in the organization
url =f"https://api.mist.com/api/v1/orgs/{org_id}/sites"
response = requests.get(url, headers=headers)

# Check the response status code
if response.status_code == 200:
    # Loop through each site in the organization and change the switch root password
    sites = response.json()
    for site in sites:
        site_id = site["id"]
        site_name = site["name"]
        print(f"Changing switch root password on site {site_name}...")
        url = f"https://api.mist.com/api/v1/sites/{site_id}/settings/switch_mgmt"
        response = requests.put(url, headers=headers, json=body)
        if response.status_code == 200:
            print(f"Switch root password changed successfully on site {site_name}.")
        else:
            print(f"Error changing switch root password on site {site_name}.")
else:
    print("Error retrieving list of sites. Check org_id and api_key are still valid.")