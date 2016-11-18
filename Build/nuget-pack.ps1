Write-Output "Setting .nuspec version tag to $versionStr"

$nuspecfiles = get-childitem *.nuspec -Recurse
foreach ($file in $nuspecfiles)
{
    $fullname = $file.fullname
    Write-Output "Found nuspec file at $fullname"
    & nuget.exe pack $fullname -properties owners=$env:APPVEYOR_REPO_COMMIT_AUTHOR;version=$env:APPVEYOR_BUILD_VERSION

}


$content = $content -replace '\$version\$',$versionStr

$content | Out-File $root\nuget\MarkdownLog.compiled.nuspec

& $root\NuGet\NuGet.exe pack $root\nuget\MarkdownLog.compiled.nuspec