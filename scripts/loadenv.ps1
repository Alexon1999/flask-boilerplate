# Check if an argument is provided
if ($args.Count -eq 0) {
    Write-Error "Usage: .\loadenv.ps1 path_to_env_file"
    exit
}

$envFile = $args[0]

if (-not (Test-Path $envFile)) {
    Write-Error "The file '$envFile' does not exist."
    exit
}

Get-Content $envFile | ForEach-Object {
    $pair = $_ -split '=',2
    if ($pair.Count -eq 2) {
        [System.Environment]::SetEnvironmentVariable($pair[0], $pair[1], [System.EnvironmentVariableTarget]::Process)
    }
}

Write-Host "Environment variables loaded from $envFile"
