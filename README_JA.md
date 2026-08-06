# 公開ハッブル定数推論の依存関係・数値トレーサビリティ

[English README](README.md)

本リポジトリは、次の研究報告に対応する公開科学トレーサビリティ・アーカイブです。

> **公開ハッブル定数推論の依存関係と数値トレーサビリティ - AI主導・公開資料研究報告**  
> Keiji Yoshimura（吉村 圭司）、Independent Researcher（2026）

報告書が固定科学アーカイブとして参照するのは [GitHub Release v1.7.1](https://github.com/yokken0907/hubble-constant-inference-traceability/releases/tag/v1.7.1)（tag `v1.7.1`、commit `8ada39da3c712923b70bae0c060388180e0f3a82`）です。後続のリポジトリ版は、固定科学基準を変更せず、読者向けメタデータのみを更新できます。

## 現在のリポジトリ状態

```text
REPOSITORY_RELEASE = v1.7.2
SCIENTIFIC_ARCHIVE_BASELINE = v1.7.1
SCIENTIFIC_ARCHIVE_TAG = v1.7.1
SCIENTIFIC_ARCHIVE_COMMIT = 8ada39da3c712923b70bae0c060388180e0f3a82
ORIGINAL_STATEMENT_COUNT = 30
ORIGINAL_NUMBER_COUNT = 46
POST_SYNTHESIS_VALIDATIONS = 1
BOUNDED_REPLAY_RECORDS = 2
SCIENTIFIC_VALUES_CHANGED = NO
INDEPENDENT_EXPERT_REVIEW = PENDING
```

`v1.7.2` は現在の読者向けリポジトリ版、`v1.7.1` は対応報告が参照する固定科学アーカイブです。両者の役割は異なり、同じ意味では使用しません。

## 主張境界

本リポジトリは、次を主張しません。

- ハッブルテンションの解決
- 唯一の原因または唯一正当な補正の同定
- ハッブル定数の新しい独立測定
- 元共同研究の完全パイプラインの検証
- 外部独立再現
- 新物理の証拠

目的はより限定的です。登録済み科学ステートメント、主要数値、使用した公開ソースと版、著者生成出力、限定付き検証・再実行記録、解釈上の制限を、読者が追跡・照合できる形で保存します。

## v1.7.2 の範囲

`v1.7.2` は読者向け公開モデル・メタデータの修正版です。

- 英語版、日本語版、機械可読版の案内を、実在する `v1.7.1` tag／Release に整合させました。
- 特定の公開媒体に依存しない研究報告モデルへ統一しました。
- AI 利用表示を対応する AI 主導研究報告書（版 v1.7.1-AIRR2）と整合させました。
- 現行リポジトリ版と固定科学基準版を明確に区別しました。
- ルート manifest と SHA-256 閉包を再生成しました。
- 新しい科学的主張は追加していません。

次の科学記録は変更していません。

- `C001`-`C030`
- `N001`-`N046`
- `V001`
- `E001`、`E002`
- 科学数値、単位、許容差、証拠ハッシュ、分類、主張境界

## 固定科学アーカイブ

```text
RELEASE = v1.7.1
TAG = v1.7.1
COMMIT = 8ada39da3c712923b70bae0c060388180e0f3a82
URL = https://github.com/yokken0907/hubble-constant-inference-traceability/releases/tag/v1.7.1
```

既存の `v1.7.1` tag／Release は歴史的な科学記録です。移動、差し替え、再生成を行いません。`v1.7.2` の文書更新は、報告書による `v1.7.1` の固定版引用を置き換えません。

## ソースアーカイブの同一性

```text
FROZEN_CORE_SOURCE_ARCHIVE_FILENAME = Yoshimura_2026_Dependency_and_Numerical_Traceability_in_Public_Hubble_Constant_Inference_Data.zip
FROZEN_CORE_SOURCE_ARCHIVE_SHA256 = e7074403b3fc4ddce1b11c05696cc3735b1f39c52fc5cb0e71ce517ebb949bce
FROZEN_CORE_SOURCE_ARCHIVE_INCLUDED = NO
```

これは原公開コアの組立に用いた内部ソースアーカイブの識別子であり、GitHub が生成するアーカイブや現行 ZIP のハッシュではありません。詳しくは [`SOURCE_ARCHIVE_RECORD.md`](SOURCE_ARCHIVE_RECORD.md) を参照してください。

## 最初に参照するファイル

| 確認事項 | ファイル |
|---|---|
| アーカイブの目的、読み方、解釈境界 | [`TRACEABILITY_ARCHIVE_DESCRIPTION.pdf`](TRACEABILITY_ARCHIVE_DESCRIPTION.pdf) |
| ステートメントと証拠の対応 | [`PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv`](PROVENANCE/STATEMENT_TO_EVIDENCE_REGISTER.tsv) |
| 46 主要数値の由来 | [`PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv`](PROVENANCE/PRINCIPAL_NUMERICAL_RESULTS_VALIDATION.tsv) |
| Table 2 と `N001`-`N046` の対応 | [`PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv`](PROVENANCE/TABLE2_NUMBER_ID_VALIDATION.tsv) |
| 公開ソースと版 | [`PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv`](PROVENANCE/SOURCE_AND_VERSION_RECORDS.tsv) |
| 後日追加した限定付き検証 | [`PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv`](PROVENANCE/POST_SYNTHESIS_VALIDATION_REGISTER.tsv) |
| 再実行記録 | [`PROVENANCE/REEXECUTION_EVIDENCE_REGISTER.tsv`](PROVENANCE/REEXECUTION_EVIDENCE_REGISTER.tsv) |
| 各分析の再現状態 | [`PROVENANCE/REPRODUCTION_STATUS.tsv`](PROVENANCE/REPRODUCTION_STATUS.tsv) |
| 再現できること・できないこと | [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) |
| 現在の公開状態 | [`RELEASE_STATUS.md`](RELEASE_STATUS.md) |
| ファイル一覧とハッシュ | [`MANIFEST.tsv`](MANIFEST.tsv)、[`SHA256SUMS.txt`](SHA256SUMS.txt) |

## 簡易検証

Python 3.9 以上で実行できます。リポジトリ整合性検証には第三者 Python パッケージを必要としません。

```bash
python tools/verify_publication_package.py --final-package
```

登録記録の追跡例：

```bash
python tools/trace_record.py C026
python tools/trace_record.py N001
python tools/trace_record.py E001
python tools/trace_record.py E002
python tools/trace_record.py R008
python tools/trace_record.py R012
python tools/trace_record.py S001
python tools/trace_record.py V001
```

## 構成

```text
TABLES/                    機械可読な公開表
FIGURE_SOURCE_DATA/        主要図の元データ
PROVENANCE/                ステートメント、数値、ソース、検証、パス、ハッシュの登録表
ANALYSIS_OUTPUTS/          選択した著者生成の保存出力・監査記録
POST_SYNTHESIS_VALIDATION/ 原統合後に追加した限定付き検証記録
REPRODUCTION/              限定付き再実行契約、コード、manifest、期待出力
tools/                     ナビゲーション・整合性検証ユーティリティ
MANIFEST.tsv               パス、サイズ、分類、SHA-256 一覧
SHA256SUMS.txt              checksum ファイル自身を除く全公開ファイルの SHA-256
```

## 証拠・再現性の境界

本アーカイブは、ファイル同一性、出力レベルの数値追跡、指定入力からの再実行、同一情報源内の頑健性、異なるソース要約間の記述的一致、プロジェクト内部の第二実装検証、因果帰属を区別します。一段階の成立は次段階の成立を自動的に意味しません。

`V001`、`E001`、`E002` は限定付きのプロジェクト内部検証・再実行です。元の尤度、sampler、burn-in、thinning、収束評価、posterior weight、log probability、posterior 生成環境を再構築するものではなく、外部独立再現でもありません。

## AI 利用と責任

OpenAI ChatGPT（GPT-5.6 Thinking）は主要な汎用 AI 研究システムとして使用されました。OpenAI Codex はコード生成とリポジトリ関連作業を補助しました。両者は著者ではないツールです。AI 支援部分は、保存された機械可読出力、SHA-256 記録、公開ソース記録、修正履歴、明示的な主張境界と照合されました。いずれのシステムも、専門家承認、外部独立再現、科学的妥当性の独立認証を提供しません。最終的な公開判断と責任は人間著者にあります。

詳細は [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md) を参照してください。

## 引用

リポジトリのメタデータは [`CITATION.cff`](CITATION.cff) を参照してください。対応報告は [GitHub Release v1.7.1](https://github.com/yokken0907/hubble-constant-inference-traceability/releases/tag/v1.7.1) を固定科学トレーサビリティ・アーカイブとして引用します。報告書の公開 URL、DOI、その他の永続識別子は、実際に成立した後の版でのみ追加します。

## ライセンス

- 著者生成の文章、表、図、文書：[`LICENSE`](LICENSE)
- `tools/` 以下のコード：[`tools/LICENSE`](tools/LICENSE)
- 第三者資料：元の利用条件が適用されます。
