$ErrorActionPreference = "Stop"
Write-output "Env variables:"
ls env:

Write-Output "Setting .nuspec version tag to $versionStr"



$nuspecfiles = get-childitem *.nuspec -Recurse
foreach ($file in $nuspecfiles)
{
    $fullname = $file.fullname
    $basename = $file.BaseName
    Write-Output "Found nuspec file at $fullname"
    write-output "Running command nuget.exe pack $fullname -properties owners=$env:APPVEYOR_REPO_COMMIT_AUTHOR;Authors=$env:APPVEYOR_REPO_COMMIT_AUTHOR;version=$env:APPVEYOR_BUILD_VERSION;id=$basename;description=$env:APPVEYOR_REPO_COMMIT_MESSAGE -verbose"
    & nuget.exe pack $fullname -properties "author=$env:APPVEYOR_REPO_COMMIT_AUTHOR;version=$env:APPVEYOR_BUILD_VERSION;id=$basename;title=$basename;description=$env:APPVEYOR_REPO_COMMIT_MESSAGE -verbose"

}
