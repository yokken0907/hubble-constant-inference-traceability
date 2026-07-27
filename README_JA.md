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

目的は、論文中の主張、数値、使用した公開資料の版、著者生成出力、解釈上の限界を、読者が相互に追跡できる状態にすることです。

## 現在の状態

```text
PUBLICATION_PACKAGE_VERSION = 1.5.5
PUBLICATION_CORE_MEMBER_SET = 102 files
REPOSITORY_RELEASE_FILES    = 121 files
HASHED_RELEASE_FILES        = 120 / 120 VERIFIED
MANUSCRIPT_STATUS           = PREPARED_FOR_JXIV_SUBMISSION
PERSISTENT_IDENTIFIER       = NOT_ASSIGNED
REPOSITORY_PUBLIC_URL       = NOT_YET_RECORDED
```

この公開前パッケージには、未確定のJxiv DOI、Jxiv URL、公開リポジトリURL、Release URL、公開済みステータスを記載していません。実情報が確定した後にのみ [`PUBLICATION_UPDATE_GUIDE.md`](PUBLICATION_UPDATE_GUIDE.md) に従って更新します。

## 元アーカイブの識別情報

```text
FROZEN_CORE_SOURCE_ARCHIVE_FILENAME = Yoshimura_2026_Dependency_and_Numerical_Traceability_in_Public_Hubble_Constant_Inference_Data.zip
FROZEN_CORE_SOURCE_ARCHIVE_SHA256   = e7074403b3fc4ddce1b11c05696cc3735b1f39c52fc5cb0e71ce517ebb949bce
FROZEN_CORE_SOURCE_ARCHIVE_INCLUDED = NO
```

このハッシュは、元の公開コアを構成した内部ソースアーカイブを識別するものであり、現在のリポジトリZIPのハッシュではありません。詳細は [`SOURCE_ARCHIVE_RECORD.md`](SOURCE_ARCHIVE_RECORD.md) を参照してください。

## バージョン1.5.5の修正範囲

`TABLES/TABLE2_NUMERICAL_RESULTS.tsv`へ安定した`NUMBER_ID`（`N001`～`N046`）を直接追加しました。科学的数値、単位、scope、解釈、claim statusは変更していません。詳細は [`CHANGELOG.md`](CHANGELOG.md) と [`PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv`](PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv) に記録しています。

## 最初に確認するファイル

| 確認したい内容 | ファイル |
|---|---|
| 論文の各主張と証拠の対応 | [`PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv`](PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv) |
| 46件の主要数値の出所・丸め・ハッシュ | [`PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv`](PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv) |
| Table 2と`N001`～`N046`の直接対応 | [`PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv`](PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv) |
| 使用した公開資料とバージョン | [`PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv`](PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv) |
| 収録出力と保存アーカイブの対応 | [`PROVENANCE/ARCHIVED_OUTPUT_INDEX.tsv`](PROVENANCE/ARCHIVED_OUTPUT_INDEX.tsv) |
| 全公開ファイルのサイズとハッシュ | [`MANIFEST.tsv`](MANIFEST.tsv) と [`SHA256SUMS.txt`](SHA256SUMS.txt) |
| 再現可能範囲と不可能範囲 | [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) |

## 整合性確認

Python 3.9以降だけで実行できます。追加パッケージは不要です。

```bash
python tools/verify_publication_package.py
```

主張ID、数値ID、公開資料IDから対応記録を表示できます。

```bash
python tools/trace_record.py C002
python tools/trace_record.py N001
python tools/trace_record.py S001
```

## 収録範囲

このリポジトリは、論文の主張から指定された出力までの追跡、Table 2から数値レジスターへの直接対応、数値と丸めの確認、収録ファイルの同一性確認、使用した公開資料の版の確認を可能にします。

一方で、第三者の大容量posterior、likelihood、観測生データは再配布していません。したがって、原観測から各共同研究の完全な解析パイプラインを再構築するものではありません。

## AI利用

本研究は、非専門家の独立研究者が汎用AIを広範に利用して実施しました。AIの役割と限界は [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md) に記載しています。

## 引用

[`CITATION.cff`](CITATION.cff)を参照してください。公開リポジトリURLとJxiv情報は、実際に確定した後にのみ追加します。科学的な主要引用先は論文であり、このリポジトリは対応するトレーサビリティ・アーカイブです。

## ライセンス

特記がない文書、表、データ、図の元データ、来歴レジスター、監査記録はCC BY 4.0です。`tools/`配下のPythonコードはMIT Licenseです。詳細は [`LICENSE`](LICENSE) と [`tools/LICENSE`](tools/LICENSE) を参照してください。第三者資料の識別子や引用情報は、元提供者の利用条件を変更しません。
