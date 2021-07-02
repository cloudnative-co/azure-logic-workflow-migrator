# azure-logic-workflow-migrator

Azure Logic AppのWorkflowをエクスポートし、別環境にインポートするスクリプト

## 使い方

### export_azure_logic_workflow.py

- Logic App Workflowをエクスポートするスクリプト
- リソースグループ内のすべてのWorkflowか、個別のWorkflowを指定してエクスポート可能
- エクスポートしたデータはpickleファイルとしてWorkflow毎に出力
- 出力先は`.workflows/`配下
- 使い方
    - コンソールにて`az login`でログイン
    - `az account set -s "hoge"`で適切なサブスクリプションを選択する(任意)
    - `python export_azure_logic_workflow.py -g GROUP_NAME -a`でリソースグループ内のすべてのLogicAppをカレントディレクトリにpickleファイルとして出力
    - `-a`オプションの代わりに`-w`オプションで任意のWorkflow名を指定して出力可能

### import_azure_logic_workflow.py
- Logic App Workflowをpickleファイルからインポートするスクリプト
- `.workflows/`内のすべてのpickleファイルか、個別のpickleファイルを指定してインポート可能
- 使い方
- `az login`する
    - `az account set -s "hoge"`で適切なサブスクリプションを選択する(任意)
    - `python import_azure_logic_workflow.py -a -g GROUP_NAME`でカレントディレクトリのすべてのpickleファイルをLogicAppにインポートする。同名のリソースは確認無しで上書き
    - `-a`オプションの代わりに`-w`オプションで任意のpickleファイル名を指定してインポート可能

## 注意事項などのメモ

- pickleファイルには出力したすべての情報が含まれています。取り扱い注意
- インポートするときにはほぼすべての情報がインポートされます。取り扱い注意
- connectionの設定など、別環境で正常に利用できない設定は引き継げません。要再設定
- `az login`以外の認証情報利用には対応していません

