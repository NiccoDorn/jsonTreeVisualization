$exclude = @("node_modules", ".git", "venv", "__pycache__")

function Get-FolderTree($path) {
    $result = [ordered]@{}
    $items = Get-ChildItem -Path $path
    $dirs = $items | Where-Object { $_.PSIsContainer -and ($exclude -notcontains $_.Name) } | Sort-Object Name
    $files = $items | Where-Object { -not $_.PSIsContainer } | Sort-Object Name

    foreach ($dir in $dirs) {
        $result[$dir.Name] = Get-FolderTree $dir.FullName
    }
    
    foreach ($file in $files) {
        $relativePath = $file.FullName.Substring($path.Length).TrimStart('\')
        $result[$file.Name] = @{
            path = Join-Path -Path (Split-Path $path -Leaf) -ChildPath $file.Name
        }
    }

    return $result
}

$rootPath = "C:\Users\webac\Documents\GitHub\MiniLibrary"
$rootName = Split-Path $rootPath -Leaf
$treeObject = [ordered]@{
    $rootName = Get-FolderTree $rootPath
}

$json = $treeObject | ConvertTo-Json -Depth 20 -Compress
$json | Out-File -FilePath ".\tree.json" -Encoding utf8
