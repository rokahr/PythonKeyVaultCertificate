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

os.environ['AZURE_CLIENT_ID']  = "your_client_id"
os.environ['AZURE_CLIENT_SECRET'] = "your_client_secret"
os.environ['AZURE_TENANT_ID'] = "your_tenant_id"

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://your_vault_name.vault.azure.net/", credential=credential)

#Load raw, encrypted, and encoded data from pfx
pfx = open(r"path_to_certificate.pfx", 'rb').read()

#Store raw, encrypted, and encoded data as Key Vault Secret
secret = secret_client.set_secret("name_of_certificate", pfx)

#Store password for certificate in KeyVault
pw = secret_client.set_secret("name_of_PW", 'the_actual_password')