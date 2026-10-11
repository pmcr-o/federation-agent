param()
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$r=Split-Path -Parent $PSScriptRoot
foreach($d in @('agents','scripts','references','assets','tests')){ $p=Join-Path $r $d; if(-not(Test-Path $p -PathType Container)){throw "missing $d"}; if(-not(Get-ChildItem $p -File -Recurse|Select-Object -First 1)){throw "empty $d"} }
'PASS'
return
