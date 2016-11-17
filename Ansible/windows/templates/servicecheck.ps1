try{
    invoke-webrequest http://localhost -UseBasicParsing -ErrorAction Stop
}
catch
{
    throw "error"
}

