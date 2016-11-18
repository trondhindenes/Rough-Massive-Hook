foreach ($artifactName in $artifacts.keys) {
  $artifact = $artifacts[$artifactName]
  $artifactName = $artifact.name 
  Write-output "pushing artifact metadata for $artifactName"
}