# fosso-ort-sbom

Generate SBOM using Fossology and OSS-Review-Toolkit

## 開發環境準備

專案預設使用 Python 虛擬環境 `.venv` 搭配 `pytest` 與 `ruff`：

1. 建立虛擬環境（第一次在本機使用時）：
   ```bash
   python3 -m venv .venv
   ```
2. 啟用虛擬環境並安裝相依套件：
   ```bash
   . .venv/bin/activate
   pip install -r requirements.txt
   ```

之後每次開發只需要啟用 `.venv` 即可。

## 靜態分析與測試

專案提供 `Makefile` 來簡化常見動作，所有指令預設都在 `.venv` 內執行：

- 執行靜態程式碼分析（語法檢查 + Ruff）：
  ```bash
  make lint
  ```

- 執行測試：
  ```bash
  make test
  ```

- 一次執行靜態分析與測試（適合 GitHub PR 檢查）：
  ```bash
  make all
  ```

## SBOM 掃描工具概覽

此專案的目標是提供一個後端協調層，利用官方 Docker 映像檔整合：

- **Fossology**：負責掃描原始碼、管理上傳專案與授權分析。
- **OSS Review Toolkit (ORT)**：解析各種 package manager 的相依檔案，找出第三方套件。

協調層負責：

- 透過 Fossology 的 UI 或 CLI 觸發掃描。
- 針對同一個專案路徑，同步呼叫 ORT 解析相依關係。
- 將第一方與第三方元件合併後，產生 SPDX 與 CycloneDX 兩種 SBOM 輸出。
- 將 SBOM 輸出寫入 `SBOM_OUTPUT_DIR`（預設 `sbom-artifacts/`）。

## Docker 與整合啟動 (基本流程)

在本機或 CI 環境中可以透過 `docker-compose.yml` 啟動整合環境：

```bash
docker compose up -d
```

此設定會啟動：

- `fossology` / `fossology-db`：Fossology 服務與其資料庫。
- `ort`：可供後續整合使用的 ORT 容器。

正式整合流程與環境變數設定，請參考：

- `specs/001-sbom-web-scanner/quickstart.md`
- `specs/001-sbom-web-scanner/spec.md`
