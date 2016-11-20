Param(
    $url
)
try{
    invoke-webrequest $url -UseBasicParsing -ErrorAction Stop
}
catch
{
    throw "error"
}
