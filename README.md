# PythonKeyVaultCertificate
Sample Code on how Python's requests library can be used with a Certificate stored in Azure KeyVault in order to authenticate against a REST Endpoint.

## Problem Description
1. Python's requests library currently does not support the use of [PFX certificates](https://github.com/psf/requests/issues/1573). Therefore, the adopted [requests_pks12](https://github.com/m-click/requests_pkcs12#pkcs12-support-for-requests) is required to use PFX certificats. 
2. Requests_pks12 expects to receive either the path to the PFX certificate or the [encoded, encrypted, and raw bytestring](https://github.com/m-click/requests_pkcs12#arguments). The current version of the [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-certificates) does not provide the possibility to download the certificat
3. You don't want to download and safe the certificate. You rather want to use it straight away without intermediate storage of the certificate on a share.

## Solution
You can store the encoded, encrypted and raw bytestring of your PFX as a [secret](https://docs.microsoft.com/en-us/azure/key-vault/secrets/about-secrets). To do this, you only need to have access to the path where the certificate is stored. You can then use the [PfxToKeyVaultSecret.py](https://github.com/roumen92/PythonKeyVaultCertificate/blob/master/PfxToKeyVaultSecret.py) script to upload it as a secret. You will do the same with the password for the certificate. In the second step, you will access the Azure Key Vault and retrieve the encoded bytestring as well as the password in order to use it in your Rest request:

    #use certificate within python rest request
    response = requests.request("POST", url, headers=headers, data = payload, pkcs12_data=certAsBytes, pkcs12_password=pwForCerti)
    
## Steps
1. Setup Azure Key Vault and create a service principal to access the Azure Key Vault. Use this [guide](https://docs.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python) as a reference. You will need to store the _clientID_, _clientSecret_, and _tenantID_ to use the scripts.

Add this point you should have:
* The name of your Azure Key Vault
* The path to your PFX certificate
* The password of your certificate
* The _clientID_, _clientSecret_, and _tenantID_ of your service principal

2. Open the [PfxToKeyVaultSecret.py](https://github.com/roumen92/PythonKeyVaultCertificate/blob/master/PfxToKeyVaultSecret.py) and replace the "your_client_id", "your_client_secret", "your_tenant_id", "your_vault_name", "path_to_certificate", "name_of_certificate", "name_of_PW" and 'the_actual_password' with your values ("name_of_certificate" and "name_of_PW" can be choosen):


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
    
    
3. Run the script. It will upload both the certificate and the password to Azure Key Vault.
4. Open the [RequestKeyVaultCertificate.py](https://github.com/roumen92/PythonKeyVaultCertificate/blob/master/RequestKeyVaultCertificate.py) and replace "your_client_id", "your_client_secret", "your_tenant_id", "your_vault_name" again with the values you got from the creation of the service principal. Replace "your_name_of_certificate_secret" and "your_name_of_PW_secret" with the values you have choosen above for "name_of_certificate" and "name_of_PW".
5. Change all other values with regard to your RestApi, e.g. url, body, headers, etc..
6. Run the script

## Explanation
As described above, the problem is that [requests_pks12](https://github.com/m-click/requests_pkcs12#pkcs12-support-for-requests) requires the encoded, encrypted, and raw bytestring as an argument. The [PfxToKeyVaultSecret.py](https://github.com/roumen92/PythonKeyVaultCertificate/blob/master/PfxToKeyVaultSecret.py) reads that bytestring into the variable and uploads it to the Azure Key Vault as a secret:

    secret = secret_client.set_secret("name_of_certificate", pfx)

The name can be choosen by yourself. Just remeber you need it afterwards. The same happens with the password that comes with the certificate. The [RequestKeyVaultCertificate.py](https://github.com/roumen92/PythonKeyVaultCertificate/blob/master/RequestKeyVaultCertificate.py) goes and gets the encoded, encrypted, and raw bytestring from the Azure Key Vault. Unfortunately, the encoded, encrypted, and raw bytestring is returned as a pure string. Therefore, it is transformed with ast to a bytestring before it can be used to authenticate your Python script:

    certAsBytes=ast.literal_eval(secret.value)
    
## Conclusion
Even though the Azure Key Vault RestApi supports the download of a certificate, it is not implemented in the Python SDK. In addition to this, we don't want to download the certificate and cache it somewhere. We would rather like to use it directly without any caching. This solution also allows to set the expiration date of the certificate as well as an automated versioning. Check the Python SDK if you would like to add these features

Thanks to Marc Schöni for his contribution.
