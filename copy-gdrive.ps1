# Copies new/updated files from Google Drive → E:\My Drive
# Does NOT delete anything locally (safe incremental backup)

# Create log folder if missing
$logDir = "C:\rclone\logs"
if (!(Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

# Timestamped log file
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$logFile = "$logDir\copy-$timestamp.log"

# Run rclone copy
rclone copy "gdrive:" "E:\My Drive" `
  --progress `
  --log-file="$logFile" `
  --log-level=INFO
