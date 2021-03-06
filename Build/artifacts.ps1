$ErrorActionPreference = "Stop"

#really disable stupid azure data collection
New-Item "$($env:appdata)\Windows Azure Powershell\AzureDataCollectionProfile.json" -ItemType File -Force
Set-content "$($env:appdata)\Windows Azure Powershell\AzureDataCollectionProfile.json" -Value '{"enableAzureDataCollection":false}'

$AzureContext = New-AzureStorageContext -StorageAccountName $env:STORAGE_NAME -StorageAccountKey $env:STORAGE_KEY
$AzureContext

foreach ($artifactName in $artifacts.keys) {
  $artifact = $artifacts[$artifactName]
  $type = $artifact.type
  $artifactName = $artifact.name 
  Write-output "pushing artifact metadata for $artifactName"
  $obj = "" | select commit_id, package_name, commit_author, commit_tag, package_version, artifact_url, branch_name, commit_message, artifact_type
  $obj.commit_id = $env:APPVEYOR_REPO_COMMIT
  $obj.package_name = $artifactName
  $obj.commit_author = $env:APPVEYOR_REPO_COMMIT_AUTHOR_EMAIL
  $obj.commit_tag = $env:APPVEYOR_REPO_TAG
  $obj.package_version = $env:APPVEYOR_BUILD_VERSION
  $obj.artifact_type = $type
  $obj.branch_name = $env:APPVEYOR_REPO_BRANCH
  $obj.commit_message = $env:APPVEYOR_REPO_COMMIT_MESSAGE
  write-output $obj
  $url = $env:LONE_JUPITER_URL
  $url = $url + "/api/release"

  $FileName = "$($obj.package_name)_$($obj.branch_name)_$($obj.package_version).zip"
  $obj.artifact_url = "https://$($env:STORAGE_NAME).blob.core.windows.net/artifacts/$($FileName)"
  Set-AzureStorageBlobContent -File ($artifact.path)  -Container "artifacts" -Blob $FileName -Context $AzureContext

  invoke-restmethod -UseBasicParsing -ContentType "application/json" -Method post -Body ($obj | convertto-json) -uri $url
}