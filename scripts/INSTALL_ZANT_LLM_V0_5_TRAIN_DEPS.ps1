$ErrorActionPreference = "Stop"
python -m pip install --upgrade pip
python -m pip install -r .\requirements-v0.5.txt
Write-Host "ZANT_LLM_V0_5_TRAIN_DEPS_INSTALLED=True"
