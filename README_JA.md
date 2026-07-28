# 公開ハッブル定数推論における依存関係と数値トレーサビリティ

このリポジトリは、以下の投稿予定論文に対応する公開トレーサビリティ・アーカイブです。

> **Dependency and Numerical Traceability in Public Hubble-Constant Inference: An Integrated Audit of the Local Distance Ladder, Supernova Processing, BAO, CMB, Posterior Geometry, and Other Distance Methods**  
> Keiji Yoshimura（Independent Researcher, 2026）

## 主張の境界

このリポジトリは、次のことを主張しません。

- ハッブルテンションの解決
- 唯一の原因または唯一正当な補正の特定
- 新しい独立なハッブル定数測定
- 原研究グループの完全な解析パイプラインの検証
- 新物理の証拠

目的は、論文中の主張、数値、使用した公開資料の版、著者生成出力、後日追加された限定検証、解釈上の限界を、読者が相互に追跡できる状態にすることです。

## 公開モデル

```text
PACKAGE_VERSION = 1.7.0
TARGET_PUBLIC_RELEASE = v1.7.0
PUBLIC_TAG_STATUS = NOT_CREATED_OR_INDEPENDENTLY_VERIFIED
PUBLICATION_MODEL = MANUSCRIPT_PLUS_VERSION_FIXED_GITHUB_REPOSITORY
JXIV_SUPPLEMENTARY_ZIP = NOT_USED
FULL_RAW_DATA_TO_POSTERIOR_REPRODUCTION = NOT_CLAIMED
E001_FRESH_REPLAY = PASS
E002_FRESH_REPLAY = PASS_FROM_OFFICIAL_EMPTY_CACHE
OFFICIAL_FETCH_EMPTY_CACHE_STATUS = PASS_WITH_SCOPE_RANGE_SELECTED_MEMBER_IDENTITY
LOCAL_FINAL_PACKAGE = PASS
REMOTE_TAG_ACTION = NOT_PERFORMED
```

Jxivには補足ZIPを添付せず、バージョン固定GitHubリポジトリを唯一の関連トレーサビリティ・アーカイブとします。数値の追跡可能性と再実行可能性は別々に記録します。

## 現在の状態

```text
PUBLICATION_PACKAGE_VERSION = 1.7.0
BASE_PUBLIC_VERSION          = 1.5.5
PUBLICATION_CORE_MEMBER_SET  = 102 files
REPOSITORY_RELEASE_FILES     = 483 files
HASHED_RELEASE_FILES         = 482 / 482 VERIFIED
ORIGINAL_STATEMENT_COUNT     = 30
ORIGINAL_NUMBER_COUNT        = 46
POST_SYNTHESIS_VALIDATIONS   = 1
PACKAGE_BUILD_STATUS         = FINAL_ASSEMBLED_UNTAGGED_V1.7.0
PERSISTENT_IDENTIFIER        = NOT_ASSIGNED
REPOSITORY_PUBLIC_URL        = https://github.com/yokken0907/hubble-constant-inference-traceability
```

公開済みv1.5.5は、TDCOSMO第二実装証拠の正式統合前の歴史的公開版として変更せず保存します。v1.7.0はローカルで組立・検証済みの最終パッケージであり、`v1.5.5`タグやReleaseを付け替えたり、履歴を書き換えたりするものではありません。

パッケージ作成時点では、`v1.7.0`タグURL、Jxiv DOI、Jxiv URL、Release URL、永続識別子は未割当でした。後日記録する場合も、実際に成立した公開識別子だけを使用します。

## v1.7.0の追加範囲

v1.7.0では、v1.6.0で接続済みのTDCOSMO V001証拠を維持したまま、Jxiv補足ZIP方式を廃止し、公開証拠位置と再実行状態をバージョン固定GitHubリポジトリへ統一しました。DESI BAO Gaussian fitには、固定外部入力を用いる再実行契約を追加しました。

- 構造比較 13/13 PASS
- q16・q50・q84比較 39/39 が固定済みtolerance内でPASS
- Table 6比較 12/12 が公開精度で一致

13ファイル拡張前に、実装コード、quantile方法、入力manifest、tolerance、停止条件を固定しています。

次は変更していません。

- 既存30主張`C001–C030`
- 主要科学数値`N001–N046`
- Table 2の数値、単位、scope、claim status
- C026・C027が記録する旧時点の`NOT_DONE`およびHOLD

後日の結果は`V001 = COMPLETE_WITH_SCOPE`として別レジスターに追加しました。`NOT_DONE`と`COMPLETE_WITH_SCOPE`は異なる時点と段階を表しており、矛盾しません。

## 最初に確認するファイル

| 確認したい内容 | ファイル |
|---|---|
| 論文の各主張と証拠の対応 | [`PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv`](PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv) |
| 46件の主要数値の出所・丸め・ハッシュ | [`PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv`](PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv) |
| Table 2と`N001–N046`の直接対応 | [`PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv`](PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv) |
| 後日追加された限定検証 | [`PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv`](PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv) |
| `NOT_DONE`と`COMPLETE_WITH_SCOPE`の時系列 | [`POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/HISTORICAL_SEQUENCE.md`](POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/HISTORICAL_SEQUENCE.md) |
| v1.5.5科学情報の不変確認 | [`PROVENANCE/V1_5_5_PRESERVATION_RECORD.tsv`](PROVENANCE/V1_5_5_PRESERVATION_RECORD.tsv) |
| 全公開ファイルのサイズとハッシュ | [`MANIFEST.tsv`](MANIFEST.tsv) と [`SHA256SUMS.txt`](SHA256SUMS.txt) |
| 再現可能範囲と不可能範囲 | [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) |
| ローカル完了事項と未実施の外部公開作業 | [`RELEASE_STATUS.md`](RELEASE_STATUS.md) |

## 整合性確認

Python 3.9以降だけで実行できます。リポジトリ整合性検証には追加パッケージは不要です。

```bash
python tools/verify_publication_package.py --final-package
```

主張ID、数値ID、公開資料ID、後日検証IDから対応記録を表示できます。

```bash
python tools/trace_record.py C026
python tools/trace_record.py N001
python tools/trace_record.py S001
python tools/trace_record.py V001
```

## TDCOSMO第二実装の境界

V001は、公開済みサンプル要約に対するプロジェクト内部のimplementation-diversity checkです。第三者HDF5は再配布せず、元のlikelihood、sampler、burn-in、thinning、収束診断、posterior weight、log probability、posterior生成過程は再構築していません。

外部独立再現ではありません。詳細は [`POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/README.md`](POST_SYNTHESIS_VALIDATION/tdcosmo_second_implementation/README.md) を参照してください。

## 収録範囲

このリポジトリは、論文の主張から指定された出力までの追跡、Table 2から数値レジスターへの直接対応、数値と丸めの確認、収録ファイルの同一性確認、公開資料の版確認、後日V001の証拠追跡を可能にします。

第三者の大容量posterior、likelihood、観測生データ、TDCOSMO HDF5、元論文PDFは再配布していません。原観測から各共同研究の完全な解析パイプラインを再構築するものではありません。

## AI利用

本研究は、非専門家の独立研究者が汎用AIを広範に利用して実施しました。AIの役割と限界は [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md) に記載しています。

## 引用

[`CITATION.cff`](CITATION.cff)を参照してください。公開リポジトリURLは記録済みです。後日`v1.7.0`のRelease URLまたはJxiv情報が成立した場合は、実在する公開識別子だけを記録します。科学的な主要引用先は論文であり、このリポジトリは対応するトレーサビリティ・アーカイブです。

## ライセンス

特記がない文書、表、データ、図の元データ、来歴レジスター、監査記録はCC BY 4.0です。`tools/`配下とV001の指定された著者生成PythonコードはMIT Licenseです。第三者資料には著者ライセンスを適用しません。


## Version 1.7.0 replay extension

Version 1.7.0 adds two project-internal replay records without changing C001-C030, N001-N046, or V001: `E001` for the fixed-seed CMB bootstrap (N025-N026) and `E002` for the two-layer posterior-attribution workflow (N029-N035). Third-party posterior chain bytes are not redistributed. See `PROVENANCE/REEXECUTION_EVIDENCE_REGISTER.tsv` and the two new `REPRODUCTION/` capsules.

## v1.7.0 再現性修復結果

E002 verifierは、公式empty-cache Phase2C証拠からN029–N035とHTS66/HTS67分類を直接検証する。この実行は空のcache/work/outputから開始し、51件のselected posterior exportをbyte size・SHA-256で再検証してPASSした。`REPRODUCTION/posterior_attribution/fresh_replay_records/`の先行監査記録は歴史記録として保持するが、現行E002受入れ系統ではない。

Phase2Cではネットワーク可能なWSL環境の完全に空のexternal cacheから公式取得を実行し、51件のselected memberをbyte sizeとSHA-256で検証した上でE002を完走した。ORIGINAL外側archive全体はmaterializeせずHTTP Rangeを用いたためfull-archive SHA-256は主張しない。記録済みETagと観測ETagの差異はHTTP metadataとして保持し、科学入力のidentity gateには用いない。
### HTS67来歴境界

現行E002の唯一の受入れ系統は`PHASE2C-OFFICIAL-EMPTY-CACHE-20260728T122933Z`である。この実行のHTS67 result ZIP（SHA-256 `8254503a8a18d6ca3cfcc6dfb0104458982e19bd13bf89b9c81d3e8f34a31353`）に含まれる指定8科学表は、保存済みhistorical substantive referenceとbyte-for-byteで一致する。現行`HTS67_HISTORICAL_VS_FRESH_COMPARISON.tsv`は、この実ZIP memberから生成する。path依存・packaging依存記録までbyte-identicalとは主張せず、semantic・provenance基準で別途確認する。

旧非byte-identical比較は`historical_earlier_replay/`へbyte不変で分離し、`CURRENT_E002_ACCEPTANCE_EVIDENCE = NO`とした。run IDと実行環境は推測せずUNKNOWN／UNRESOLVEDのまま保持する。リモートタグ作成・確認は外部作業として未実施である。
