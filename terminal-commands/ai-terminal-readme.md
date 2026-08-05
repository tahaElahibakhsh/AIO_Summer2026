# AI Terminal Command Handbook

A copy-friendly README for everyday terminal work in **Linux** and **Windows** with a strong focus on **AI / ML workflows**.

<details>
<summary><strong>How to use this README</strong></summary>

- Copy a whole command block as-is.
- Replace the placeholder parts like `<dataset>` or `<model.py>`.
- Use the **Linux / Bash** and **Windows / CMD / PowerShell** versions that match your system.
- For GitHub, this file is Markdown-ready and works well in repos.

</details>

---

## Table of contents

- [Core navigation](#core-navigation)
- [Files and folders](#files-and-folders)
- [Search, inspect, and logs](#search-inspect-and-logs)
- [AI setup essentials](#ai-setup-essentials)
- [AI training workflows](#ai-training-workflows)
- [Dataset management](#dataset-management)
- [Git and collaboration](#git-and-collaboration)
- [Windows vs Linux cheat sheet](#windows-vs-linux-cheat-sheet)
- [Troubleshooting](#troubleshooting)

---

## Core navigation

<details open>
<summary><strong>Linux / Bash</strong></summary>

```bash
pwd
ls
ls -la
cd projects
cd ..
cd ~
clear
history
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
cd
dir
dir /a
cd Projects
cd ..
cd %USERPROFILE%
cls
doskey /history
```

</details>

<details>
<summary><strong>PowerShell</strong></summary>

```powershell
Get-Location
Get-ChildItem
Get-ChildItem -Force
Set-Location projects
Set-Location ..
Set-Location ~
Clear-Host
Get-History
```

</details>

---

## Files and folders

<details open>
<summary><strong>Linux / Bash</strong></summary>

```bash
mkdir data
touch notes.txt
cp notes.txt backup-notes.txt
mv backup-notes.txt archive-notes.txt
rm archive-notes.txt
rm -r old-folder
cat notes.txt
less notes.txt
head -n 20 notes.txt
tail -n 20 notes.txt
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
mkdir data
type nul > notes.txt
copy notes.txt backup-notes.txt
move backup-notes.txt archive-notes.txt
del archive-notes.txt
rmdir /s old-folder
type notes.txt
more notes.txt
```

</details>

<details>
<summary><strong>PowerShell</strong></summary>

```powershell
New-Item -ItemType Directory data
New-Item notes.txt
Copy-Item notes.txt backup-notes.txt
Move-Item backup-notes.txt archive-notes.txt
Remove-Item archive-notes.txt
Remove-Item old-folder -Recurse
Get-Content notes.txt
Get-Content notes.txt | Select-Object -First 20
Get-Content notes.txt | Select-Object -Last 20
```

</details>

---

## Search, inspect, and logs

These commands are especially useful when you are debugging AI projects, reading training logs, or checking experiment outputs.

<details open>
<summary><strong>Linux / Bash</strong></summary>

```bash
grep -R "loss" logs/
grep -R "accuracy" .
find . -name "*.csv"
find . -type f -size +100M
wc -l data/train.csv
awk -F, 'NR==1{print NF}' data/train.csv
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
findstr /S /I "loss" logs\*.txt
findstr /S /I "accuracy" *.*
dir /S *.csv
forfiles /S /M *.* /C "cmd /c if @fsize GTR 104857600 echo @path"
find /C /V "" data\train.csv
```

</details>

<details>
<summary><strong>PowerShell</strong></summary>

```powershell
Select-String -Path logs\* -Pattern "loss"
Select-String -Path .\* -Pattern "accuracy"
Get-ChildItem -Recurse -Filter *.csv
Get-ChildItem -Recurse | Where-Object { $_.Length -gt 100MB }
(Get-Content data\train.csv | Select-Object -First 1).Split(',').Count
```

</details>

---

## AI setup essentials

<details open>
<summary><strong>Linux / Bash</strong></summary>

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install jupyter notebook ipykernel
python -m ipykernel install --user --name .venv --display-name "AI Env"
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m pip install jupyter notebook ipykernel
py -m ipykernel install --user --name .venv --display-name "AI Env"
```

</details>

<details>
<summary><strong>PowerShell</strong></summary>

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m pip install jupyter notebook ipykernel
py -m ipykernel install --user --name .venv --display-name "AI Env"
```

</details>

---

## AI training workflows

### 1) Check GPU

<details open>
<summary><strong>Linux / Bash</strong></summary>

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only')"
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
nvidia-smi
py -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only')"
```

</details>

### 2) Run a training script

<details open>
<summary><strong>Linux / Bash</strong></summary>

```bash
python train.py --config configs/train.yaml
python train.py --epochs 20 --batch-size 32 --lr 1e-4
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
py train.py --config configs\train.yaml
py train.py --epochs 20 --batch-size 32 --lr 1e-4
```

</details>

### 3) Launch notebooks

<details open>
<summary><strong>Linux / Bash</strong></summary>

```bash
jupyter lab
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
jupyter lab
```

</details>

### 4) Watch training live

<details open>
<summary><strong>Linux / Bash</strong></summary>

```bash
tail -f logs/train.log
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
type logs\train.log
```

</details>

<details>
<summary><strong>PowerShell</strong></summary>

```powershell
Get-Content logs\train.log -Wait
```

</details>

---

## Dataset management

### Download and unzip

<details open>
<summary><strong>Linux / Bash</strong></summary>

```bash
mkdir -p data/raw
wget https://example.com/dataset.zip -O data/raw/dataset.zip
unzip data/raw/dataset.zip -d data/raw
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
mkdir data\raw
curl -L https://example.com/dataset.zip -o data\raw\dataset.zip
tar -xf data\raw\dataset.zip -C data\raw
```

</details>

<details>
<summary><strong>PowerShell</strong></summary>

```powershell
New-Item -ItemType Directory data\raw
Invoke-WebRequest https://example.com/dataset.zip -OutFile data\raw\dataset.zip
Expand-Archive data\raw\dataset.zip -DestinationPath data\raw
```

</details>

### Compress a project or dataset

<details open>
<summary><strong>Linux / Bash</strong></summary>

```bash
tar czvf dataset-backup.tar.gz data/
zip -r project.zip .
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
tar -czvf dataset-backup.tar.gz data
powershell Compress-Archive -Path * -DestinationPath project.zip
```

</details>

---

## Git and collaboration

<details open>
<summary><strong>Linux / Bash</strong></summary>

```bash
git status
git add .
git commit -m "update experiment"
git push
git pull
git branch
git checkout -b feature/ai-experiments
```

</details>

<details>
<summary><strong>Windows CMD</strong></summary>

```cmd
git status
git add .
git commit -m "update experiment"
git push
git pull
git branch
git checkout -b feature/ai-experiments
```

</details>

---

## Windows vs Linux cheat sheet

| Task | Linux / Bash | Windows CMD |
|---|---|---|
| Show files | `ls -la` | `dir /a` |
| Clear screen | `clear` | `cls` |
| Create file | `touch file.txt` | `type nul > file.txt` |
| Delete file | `rm file.txt` | `del file.txt` |
| Delete folder | `rm -r folder` | `rmdir /s folder` |
| Show file | `cat file.txt` | `type file.txt` |
| Search text | `grep "word" file.txt` | `findstr "word" file.txt` |
| Archive folder | `tar czvf x.tar.gz folder` | `tar -czvf x.tar.gz folder` |

---

## AI-ready command recipes

<details open>
<summary><strong>Recipe 1: start a fresh experiment</strong></summary>

```bash
mkdir ai-experiment
cd ai-experiment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install numpy pandas scikit-learn torch matplotlib jupyter
jupyter lab
```

```cmd
mkdir ai-experiment
cd ai-experiment
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install numpy pandas scikit-learn torch matplotlib jupyter
jupyter lab
```

</details>

<details>
<summary><strong>Recipe 2: inspect a dataset fast</strong></summary>

```bash
head data/train.csv
wc -l data/train.csv
grep -R "NaN" data/
```

```cmd
more data\train.csv
find /C /V "" data\train.csv
findstr /S /I "NaN" data\*.csv
```

</details>

<details>
<summary><strong>Recipe 3: archive results for sharing</strong></summary>

```bash
mkdir -p exports
tar czvf exports/run-01.tar.gz logs/ models/ reports/
```

```cmd
mkdir exports
tar -czvf exports\run-01.tar.gz logs models reports
```

</details>

---

## Keyboard shortcuts worth memorizing

<details open>
<summary><strong>Terminal basics</strong></summary>

- `Ctrl + C` stops the current command.
- `Ctrl + L` clears the screen in many terminals.
- `Tab` autocompletes file and folder names.
- `Up Arrow` brings back the last command.
- `Ctrl + R` searches command history.
- `Ctrl + D` exits many shells or ends input.

</details>

---

## Troubleshooting

<details open>
<summary><strong>Common problems and fixes</strong></summary>

- **Python not found**: make sure your virtual environment is activated.
- **Torch does not see GPU**: check `nvidia-smi`, then reinstall the matching PyTorch build.
- **Command works on Linux but not Windows**: use the cheat sheet above.
- **Long paths on Windows**: keep project folders shallow, like `C:\ai\project`.
- **Line endings look strange in logs or scripts**: use the right editor and Git settings.

</details>

---

## Minimal AI workflow checklist

- Set up the environment.
- Confirm the GPU.
- Download the dataset.
- Run training.
- Watch logs.
- Save checkpoints.
- Zip results.
- Push code to Git.

---

## Notes

This README is designed to be:
- **copy-friendly**
- **GitHub-friendly**
- **beginner-friendly**
- **useful for AI projects**

You can expand it later with project-specific commands for:
- fine-tuning
- data preprocessing
- evaluation
- inference
- model export
