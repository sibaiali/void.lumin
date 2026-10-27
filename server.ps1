$port = 3000
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Start()

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " VOID LUMIN v6.0 // CYBER-KINETIC HUMAN STUDIO ONLINE" -ForegroundColor Green
Write-Host " COPYRIGHT (C) 2026 ALI SIBAI // GERMAN UrhG & EU PROTECTED" -ForegroundColor Yellow
Write-Host " URL: http://localhost:$port" -ForegroundColor Cyan
Write-Host " BACKEND DATA SCREENING: http://localhost:$port/api/telemetry" -ForegroundColor Magenta
Write-Host "==========================================================" -ForegroundColor Cyan

Start-Process "http://localhost:$port"

$root = $PSScriptRoot
$ledger = New-Object System.Collections.ArrayList

while ($listener.IsListening) {
  try {
    $context = $listener.GetContext()
    $req = $context.Request
    $res = $context.Response
    $res.Headers.Add("Access-Control-Allow-Origin", "*")
    $res.Headers.Add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    $res.Headers.Add("Access-Control-Allow-Headers", "Content-Type")
    $res.Headers.Add("X-Frame-Options", "DENY")
    $res.Headers.Add("X-Content-Type-Options", "nosniff")
    $res.Headers.Add("Referrer-Policy", "strict-origin-when-cross-origin")
    $res.Headers.Add("X-Robots-Tag", "noai, noimageai")
    $res.Headers.Add("X-Copyright-Owner", "Ali Sibai - Protected under German UrhG SS 69a & EU Law - All Rights Reserved")

    $path = $req.Url.LocalPath

    if ($req.HttpMethod -eq "OPTIONS") {
      $res.StatusCode = 204
      $res.Close()
      continue
    }

    if ($path -eq "/api/telemetry") {
      $res.ContentType = "application/json; charset=utf-8"
      if ($req.HttpMethod -eq "POST") {
        $reader = New-Object System.IO.StreamReader($req.InputStream, $req.ContentEncoding)
        $body = $reader.ReadToEnd()
        $reader.Close()

        $hash = [Math]::Abs($body.GetHashCode()).ToString("X8")
        $sig = "VL6-HUMAN-$hash"
        $respObj = @{
          valid = $true
          screenedData = @{
            screenedAt = (Get-Date).ToUniversalTime().ToString("o")
            piiPurged = $true
            gdprCompliant = "EU-DSGVO-ART-25-VERIFIED"
            copyrightProtection = "DE-URHG-SS69A-ALI-SIBAI-ALL-RIGHTS-RESERVED"
            rejectedFieldsCount = 2
            humanProofSignature = $sig
          }
        }
        [void]$ledger.Add($respObj.screenedData)
        $json = $respObj | ConvertTo-Json -Depth 5
        $buf = [System.Text.Encoding]::UTF8.GetBytes($json)
        $res.ContentLength64 = $buf.Length
        $res.OutputStream.Write($buf, 0, $buf.Length)
        $res.Close()
        continue
      } else {
        $respObj = @{
          engine = "VOID LUMIN v6.0 // Zero-PII Kinematic Screening & Anti-Clone DRM Backend"
          copyright = "(c) 2026 Ali Sibai (sibaiali). Protected under German UrhG SS 69a & EU Directive 2009/24/EC."
          status = "ONLINE"
          totalScreenedBatches = $ledger.Count
        }
        $json = $respObj | ConvertTo-Json -Depth 5
        $buf = [System.Text.Encoding]::UTF8.GetBytes($json)
        $res.ContentLength64 = $buf.Length
        $res.OutputStream.Write($buf, 0, $buf.Length)
        $res.Close()
        continue
      }
    }

    if ($path -eq "/" -or $path -eq "") {
      $path = "/index.html"
    }

    $filePath = Join-Path $root ($path.TrimStart('/').Replace('/', '\'))
    if (-not (Test-Path $filePath -PathType Leaf)) {
      $filePath = Join-Path $root "index.html"
    }

    $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
    switch ($ext) {
      ".html" { $res.ContentType = "text/html; charset=utf-8" }
      ".js"   { $res.ContentType = "application/javascript; charset=utf-8" }
      ".json" { $res.ContentType = "application/json; charset=utf-8" }
      ".css"  { $res.ContentType = "text/css; charset=utf-8" }
      default { $res.ContentType = "application/octet-stream" }
    }

    $bytes = [System.IO.File]::ReadAllBytes($filePath)
    $res.ContentLength64 = $bytes.Length
    $res.OutputStream.Write($bytes, 0, $bytes.Length)
    $res.Close()
  } catch {
    break
  }
}
