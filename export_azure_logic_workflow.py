# エクスポートするworkflowのデータに重要な情報があっても気にせずすべて出すので注意
# You need `az login`
# Import the needed credential and management objects from the libraries.
import os
import sys
import pickle
import argparse
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import AzureCliCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.logic import LogicManagementClient
from azure.mgmt.logic.models import Workflow

# get argument
desc = """Export Azure Logic App Workflows.
export pickle files in current dir.
require --all or --workflow_name"""
parser = argparse.ArgumentParser(
    description=desc,
    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-g", "--group_name",
                    help="target resource group name", required=True)
parser.add_argument("-a", "--all",  action="store_true",
                    help="get all Logic App workflow")
parser.add_argument("-w", "--workflow_name",
                    help="target workflow name", default=None)
args = parser.parse_args()

# option check
if args.all is False and args.workflow_name is None:
    print("require only --all or --workflow_name")
    sys.exit()
if args.all is True and args.workflow_name is not None:
    print("require only --all or --workflow_name")
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

resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)

resource_list = resource_client.resources.list_by_resource_group(
    GROUP_NAME,
    expand="createdTime,changedTime"
)

logic_client = LogicManagementClient(
    credential=credential,
    subscription_id=SUBSCRIPTION_ID
)

WORKFLOWS_PATH = "./.workflows"
if not os.path.exists(WORKFLOWS_PATH):
    os.makedirs(WORKFLOWS_PATH, exist_ok=True)

workflows = logic_client.workflows.list_by_resource_group(GROUP_NAME)
for w in workflows:
    if args.all or w.name == args.workflow_name:
        f_workflow_name = w.name + ".pickle"
        print("creating " + f_workflow_name)
        with open(os.path.join(WORKFLOWS_PATH, f_workflow_name), 'wb') as f:
            pickle.dump(w, f)
print("Export Complete.")
