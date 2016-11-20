$LoneJupiterUrl = "http://ec2-52-59-220-91.eu-central-1.compute.amazonaws.com"
#$ThisComputerName = $env:COMPUTERNAME
$ThisComputerName = "EC2AMAZ-KEBS2AU"

$appmaps = Invoke-RestMethod -Uri "$LoneJupiterUrl/api/applicationmaps"
foreach ($appmap in $appmaps)
{
    $Name = $appmap.name
    $DesiredCount = $appmap.instancecount

    $ExistingDeployments = Invoke-RestMethod -Uri "$LoneJupiterUrl/api/deployments/"
    $ExistingDeployments | where {($_.version -eq $appmap.gitfilter.version) -and ($_.branch -eq $appmap.gitfilter.branch)}

    $ThisServerFitsAppMap = $True

    foreach ($tag in ($appmap.targettags))
    {
        $EnvVarValue = Get-childitem -Path "env:" | where {$_.Name -eq $tag.name}
        if (($EnvVarValue.Value) -eq ($tag.value))
        {
            #Tag fits
        }
        else
        {
            $ThisServerFitsAppMap = $False
        }
    }

    if ($ThisServerFitsAppMap -eq $false)
    {
        #Server doesn't fit, break out of appmap loop
        break
    }

    if ($ExistingDeployments.count -eq $DesiredCount)
    {
        #already hosting the required number of instances of this app/version/branch
        break
    }
    else
    {
        $MissingCount = $DesiredCount - $ExistingDeployments.count
        #We want to spread the load evenly and make sure not all packages end up on the first server.
        #Figure out the potential servers for this app
        
    }
}

Write-Output "Done"