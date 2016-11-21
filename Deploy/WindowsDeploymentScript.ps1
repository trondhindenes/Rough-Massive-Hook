Function Get-Blob
{
    Param(
        $Key,
        $Account,
        $Url
    )

    New-Item "$($env:appdata)\Windows Azure Powershell\AzureDataCollectionProfile.json" -ItemType File -Force | out-null
    Set-content "$($env:appdata)\Windows Azure Powershell\AzureDataCollectionProfile.json" -Value '{"enableAzureDataCollection":false}'

    $AzureContext = New-AzureStorageContext -StorageAccountName $account -StorageAccountKey $key

    [system.uri]$Uri = $Url
    $urlPath = $uri.AbsolutePath
    $Container = $urlPath.split("/")[1]
    $BlobPath = $urlPath.Replace($container, "").TrimStart("//")

    Get-AzureStorageBlobContent -Blob $BlobPath -Container $container -Context $AzureContext -Destination "C:\Staging\$($BlobPath)" -Confirm:$false -Force | out-null
    return "C:\Staging\$($BlobPath)"
}

$LoneJupiterUrl = "http://ec2-54-93-41-146.eu-central-1.compute.amazonaws.com"

$url = "$($LoneJupiterUrl)/api/applicationmaps/"
$AppMaps = Invoke-RestMethod -Uri $url -UseBasicParsing

$url = "$($LoneJupiterUrl)/api/deployments/server/$($env:computername)"
$Deployments = Invoke-RestMethod -Uri $url -UseBasicParsing

$url = "$($LoneJupiterUrl)/api/release"
$Artifacts = Invoke-RestMethod -Uri $url -UseBasicParsing


$PendingDeployments = $Deployments | where {$_.status -eq "reserved"}

foreach ($Deployment in $PendingDeployments)
{
    #Lookup appmap
    $url = "$($LoneJupiterUrl)/api/applicationmaps/"
    $appmap = $AppMaps | where {$_.name -eq ($Deployment.deployment_name)}
    #$appmap
    $thisartifact = $artifacts | where {($_.package_name -eq $appmap.package) -and ($_.branch_name -eq ($appmap.gitfilter.branch)) -and ($_.package_version -eq $appmap.gitfilter.version)}
    if ($thisartifact -eq $null)
    {
        break
    }

    $LocalPath = Get-Blob -Key $env:AZUREKEY -Account $env:AZUREACCOUNT -Url $thisartifact.artifact_url
    
    $LocalFolder = "$($appmap.package)--$($Deployment.deployment_name)--$($Deployment.package_version)--$($Deployment.local_port)"
    
    $LocalIisPath = "C:\Inetpub\$($LocalFolder)"
    new-item $LocalIisPath -ItemType directory -force | out-null
    if (!(Get-IISAppPool -Name $LocalFolder))
    {
        New-WebAppPool -Name $LocalFolder -Force
    }
    if (!(Get-Website -Name $LocalFolder))
    {
        New-Website -Name $LocalFolder -PhysicalPath $LocalIisPath -Port $Deployment.local_port -ApplicationPool $LocalFolder -Force
    }
    & "C:\Program Files\IIS\Microsoft Web Deploy V3\msdeploy.exe" -verb:sync -source:package="$LocalPath" -dest:auto -setParam:kind=ProviderPath,scope=iisApp,value=$LocalFolder

    #Configure service discovery
    $ConsulService = "" | select service
    $ConsulObj = new-object -TypeName "PSCustomObject"
    $ConsulObj | add-member -MemberType NoteProperty -Name "name" -Value $Deployment.deployment_name
    $ConsulObj | add-member -MemberType NoteProperty -Name "id" -Value $LocalFolder
    $ConsulObj | add-member -MemberType NoteProperty -Name "port" -value $Deployment.local_port
    $ConsulObj | add-member -MemberType NoteProperty -Name "address" -value (Get-NetIPAddress -AddressFamily IPv4 | select -First 1 | select -ExpandProperty ipaddress)

    $Checks = @()
    $check = "" | select script,interval
    $check.script = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -file C:\apps\consul\checks\servicecheck.ps1 http://localhost:$($Deployment.local_port)/health"
    $check.interval = "10s"
    $checks += $check
    $ConsulObj | add-member -MemberType NoteProperty -Name "checks" -value $Checks
    $ConsulService.Service = $ConsulObj

    New-item "C:\apps\consul\config\$($LocalFolder).json" -Force
    set-content "C:\apps\consul\config\$($LocalFolder).json" -Value ($ConsulService | convertto-json -Depth 99) -Force

    #reload consul
    & C:\apps\consul\consul reload
}