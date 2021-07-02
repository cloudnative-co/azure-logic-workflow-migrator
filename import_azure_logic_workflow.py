# インポートするworkflowのデータに重要な情報があっても気にせず入れるので注意
# You need `az login`
# Import the needed credential and management objects from the libraries.
import logging
import os
import sys
import glob
import pickle
import argparse
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import AzureCliCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.logic import LogicManagementClient
from azure.mgmt.logic.models import Workflow

# デバッグ用のログ有効化設定
# logger = logging.getLogger('azure')
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(stream=sys.stdout)
# logger.addHandler(handler)

# get argument
parser = argparse.ArgumentParser(
    description="require --all or --workflow_file_name")
parser.add_argument("-g", "--group_name",
                    help="target resource group name", required=True)
parser.add_argument("-a", "--all",  action="store_true",
                    help="get all Logic App workflow files in current dir")
parser.add_argument("-w", "--workflow_file_name",
                    help="target workflow file name", default=None)
args = parser.parse_args()

# option check
if args.all is False and args.workflow_file_name is None:
    print("require only --all or --workflow_file_name")
    sys.exit()
if args.all is True and args.workflow_file_name is not None:
    print("require only --all or --workflow_file_name")
    sys.exit()

GROUP_NAME = args.group_name

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()
subscription_client = SubscriptionClient(credential)
sub_list = list(subscription_client.subscriptions.list())

# Retrieve subscription ID from environment variable.
SUBSCRIPTION_ID = sub_list[0].subscription_id
SUBSCRIPTION_NAME = sub_list[0].display_name
print("Subscription Name: " + SUBSCRIPTION_NAME)
print("Group Name: " + GROUP_NAME)

agree = input('Is it Trust? (y/n): ')
if agree != 'y':
    sys.exit()

resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)

logic_client = LogicManagementClient(
    credential=credential,
    subscription_id=SUBSCRIPTION_ID
)

# 対象ファイル一覧作成
WORKFLOWS_PATH = "./.workflows"
workflow_list = []
if args.workflow_file_name is not None:
    if os.path.isfile(args.workflow_file_name):
        workflow_list.append(args.workflow_file_name)
if args.all is True:
    workflow_list.extend(glob.glob(os.path.join(WORKFLOWS_PATH, "*.pickle")))

# 対象確認
print("Target file list:")
for wf in workflow_list:
    print("  " + wf)

agree = input('Add all the above? (y/n): ')
if agree != 'y':
    sys.exit()

# インポート
print("Import Start...")
for wf in workflow_list:
    with open(wf, 'rb') as f:
        w = pickle.load(f)

    print("Workflow name: " + w.name)

    WORKFLOW_NAME = w.name
    # Create logic
    workflow = Workflow(
        location=w.location,
        definition=w.definition,
        parameters={}  # parametersは環境に依存した値のため
    )
    try:
        logic_client.workflows.create_or_update(
            GROUP_NAME,
            WORKFLOW_NAME,
            workflow,
            logging_enable=True
        )
    except Exception as e:
        print(e)
print("Import Complete.")
