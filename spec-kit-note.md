# 001-sbom-web-scanner

## constitution

Create principles focused on code quality, testing standards, user experience consistency, and performance requirements

## specify

我想要設計一個網頁應用程式可以用來掃描指定的專案原始碼，然後產生 SBOM, 支援 SPDX 與 CycloneDX 格式。除了可以根據當前專案目錄的程式碼產生之外，還能夠掃描 package manager 描述檔案，找出相依的第三方軟體組件，並確保這些用到的第三方組件也要描述在 SBOM 中。

## clarify

## plan

預計使用 Fossology 與 OSS-Review-Toolkit 這兩個官方的 docker images, 可以直接使用 Fossology 的網頁介面當作 UI, 需要自動設定 Fossology 與 OSS-Review-Toolkit 之間的整合，我需要單一的操作介面。

## checklist

## tasks

## analyze

## implement

---
