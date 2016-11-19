$AzureContext = New-AzureStorageContext -StorageAccountName $env:STORAGE_NAME -StorageAccountKey $env:STORAGE_KEY
foreach ($artifactName in $artifacts.keys) {
  $artifact = $artifacts[$artifactName]
  $artifactName = $artifact.name 
  Write-output "pushing artifact metadata for $artifactName"
  $obj = "" | select commit_id, package_name, commit_author, commit_tag, package_version, artifact_url, branch_name, commit_message
  $obj.commit_id = $env:APPVEYOR_REPO_COMMIT
  $obj.package_name = $artifactName
  $obj.commit_author = $env:APPVEYOR_REPO_COMMIT_AUTHOR_EMAIL
  $obj.commit_tag = $env:APPVEYOR_REPO_TAG
  $obj.package_version = $env:APPVEYOR_BUILD_VERSION
  $obj.artifact_url = $artifact.url
  $obj.branch_name = $env:APPVEYOR_REPO_BRANCH
  $obj.commit_message = $env:APPVEYOR_REPO_COMMIT_MESSAGE
  write-output $obj
  $url = $env:LONE_JUPITER_URL
  $url = $url + "/api/release"

  $FileName = "$($obj.package_name)_$($obj.branch_name)_$($obj.package_version).zip"
  
  Set-AzureStorageBlobContent -File $artifact.path  -Container "artifacts" ` 
        -Blob $FileName -Context $AzureContext

  invoke-restmethod -UseBasicParsing -ContentType "application/json" -Method post -Body ($obj | convertto-json) -uri $url
}