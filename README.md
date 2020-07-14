# PythonKeyVaultCertificate
Sample Code on how Python's requests library can be used with a Certificate stored in KeyVault in order to authenticate against a REST Endpoint.

## Problem Description
1: Python's requests library currently does not support the use of ([PFX certificates] (https://github.com/psf/requests/issues/1573)). Therefore, the adopted requests_pks12 (https://github.com/m-click/requests_pkcs12#pkcs12-support-for-requests) is required to use PFX certificats. 
2: Requests_pks12 expects to receive either the path to the PFX certificate or the encoded, encrypted, and raw bytestring (https://github.com/m-click/requests_pkcs12#arguments). The current version of the Azure SDK for Python (https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-certificates) does not provide the possibility to download the certificat
3: You don't want to download and safe the certificate. You rather want to use it straight away without intermediate storage of the certificate on a share.

