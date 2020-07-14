# This Sample Code is provided for the purpose of illustration only and is not intended to be used
# in a production environment.  THIS SAMPLE CODE AND ANY RELATED INFORMATION ARE PROVIDED "AS IS" WITHOUT
# WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.  We grant You a nonexclusive,
# royalty-free right to use and modify the Sample Code and to reproduce and distribute the object code
# form of the Sample Code, provided that You agree: (i) to not use Our name, logo, or trademarks to market 
# Your software product in which the Sample Code is embedded; (ii) to include a valid copyright notice
# on Your software product in which the Sample Code is embedded; and (iii) to indemnify, hold harmless,
# and defend Us and Our suppliers from and against any claims or lawsuits, including attorneys’ fees,
# that arise or result from the use or distribution of the Sample Code.
# Please note: None of the conditions outlined in the disclaimer above will supersede the terms and
# conditions contained within the Premier Customer Services Description

import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import ast

#Use of special library of requests where pfx certis are supported
import requests_pkcs12 as requests

#Set connection parameters to access Key Vault. Parameters are returned when Service Principal is created. Or they are found in the Azure Portal.
os.environ['AZURE_CLIENT_ID']  = "your_client_id"
os.environ['AZURE_CLIENT_SECRET'] = "your_client_secret"
os.environ['AZURE_TENANT_ID'] = "your_tenant_id"

#Access Key Vault
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://your_vault_name.vault.azure.net/", credential=credential)

#Get certificate as encoded, encrypted bytestring out of KeyVault
secret = secret_client.get_secret("your_name_of_certificate_secret")

#Key Vault returns bytestring as pure string. Transform to bytestring
certAsBytes=ast.literal_eval(secret.value)

#Get Pw for Certificate out of Key Vault
pwForCerti=(secret_client.get_secret("your_name_of_PW_secret")).value

#set connection parameters
url = "url_to_RestAPI"

payload = "any_payload_you_want_to_pass"
headers = {
  'content-type': 'text',
  'whatever_is_needed': 'whatever_is_needed'
}

#use certificate within python rest request
response = requests.request("POST", url, headers=headers, data = payload, pkcs12_data=certAsBytes, pkcs12_password=pwForCerti)

print(response.text.encode('utf8'))