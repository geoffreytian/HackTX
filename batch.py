from __future__ import print_function
import feedparser as fp
from newspaper import Article
import json
import newspaper
from time import mktime
import datetime
import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import urllib.request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import csv
import datetime
import io
import os
import sys
import time
import config
try:
	input = raw_input
except NameError:
	pass

import azure.storage.blob as azureblob
import azure.batch.batch_service_client as batch
import azure.batch.batch_auth as batch_auth
import azure.batch.models as batchmodels

sys.path.append('.')
sys.path.append('..')



def create_pool(batch_service_client, pool_id):
	"""
	Creates a pool of compute nodes with the specified OS settings.
	:param batch_service_client: A Batch service client.
	:type batch_service_client: `azure.batch.BatchServiceClient`
	:param str pool_id: An ID for the new pool.
	:param str publisher: Marketplace image publisher
	:param str offer: Marketplace image offer
	:param str sku: Marketplace image sku
	"""
	print('Creating pool [{}]...'.format(pool_id))

	# Create a new pool of Linux compute nodes using an Azure Virtual Machines
	# Marketplace image. For more information about creating pools of Linux
	# nodes, see:
	# https://azure.microsoft.com/documentation/articles/batch-linux-nodes/
	new_pool = batch.models.PoolAddParameter(
		id=pool_id,
		virtual_machine_configuration=batchmodels.VirtualMachineConfiguration(
			image_reference=batchmodels.ImageReference(
				publisher="Canonical",
				offer="UbuntuServer",
				sku="18.04-LTS",
				version="latest"
			),
			node_agent_sku_id="batch.node.ubuntu 18.04"),
		vm_size=config._POOL_VM_SIZE,
		target_dedicated_nodes=config._POOL_NODE_COUNT
	)
	batch_service_client.pool.add(new_pool)


def create_job(batch_service_client, job_id, pool_id):
	"""
	Creates a job with the specified ID, associated with the specified pool.
	:param batch_service_client: A Batch service client.
	:type batch_service_client: `azure.batch.BatchServiceClient`
	:param str job_id: The ID for the job.
	:param str pool_id: The ID for the pool.
	"""
	print('Creating job [{}]...'.format(job_id))

	job = batch.models.JobAddParameter(
		id=job_id,
		pool_info=batch.models.PoolInformation(pool_id=pool_id))

	batch_service_client.job.add(job)



def add_tasks(batch_service_client, job_id, input_files):
	"""
	Adds a task for each input file in the collection to the specified job.
	:param batch_service_client: A Batch service client.
	:type batch_service_client: `azure.batch.BatchServiceClient`
	:param str job_id: The ID of the job to which to add the tasks.
	:param list input_files: A collection of input files. One task will be
	 created for each input file.
	:param output_container_sas_token: A SAS token granting write access to
	the specified Azure Blob storage container.
	"""

	print('Adding {} tasks to job [{}]...'.format(len(input_words), job_id))

	tasks = list()

	for idx, file in enumerate(input_file):
		# command = "python scraper.py "+repr(file.file_path)[1:-1]
		command="/bin/bash -c \"pwd\""
		tasks.append(batch.models.TaskAddParameter(
			id='Task{}'.format(idx),
			command_line=command,
            resource_files=[file]
		)
		)
		print(command)
	batch_service_client.task.add_collection(job_id, tasks)


def wait_for_tasks_to_complete(batch_service_client, job_id, timeout):
	"""
	Returns when all tasks in the specified job reach the Completed state.
	:param batch_service_client: A Batch service client.
	:type batch_service_client: `azure.batch.BatchServiceClient`
	:param str job_id: The id of the job whose tasks should be to monitored.
	:param timedelta timeout: The duration to wait for task completion. If all
	tasks in the specified job do not reach Completed state within this time
	period, an exception will be raised.
	"""
	timeout_expiration = datetime.datetime.now() + timeout

	print("Monitoring all tasks for 'Completed' state, timeout in {}..."
		  .format(timeout), end='')

	while datetime.datetime.now() < timeout_expiration:
		print('.', end='')
		sys.stdout.flush()
		tasks = batch_service_client.task.list(job_id)

		incomplete_tasks = [task for task in tasks if
							task.state != batchmodels.TaskState.completed]
		if not incomplete_tasks:
			print()
			return True
		else:
			time.sleep(1)

	print()
	raise RuntimeError("ERROR: Tasks did not reach 'Completed' state within "
					   "timeout period of " + str(timeout))

def print_batch_exception(batch_exception):
    """
    Prints the contents of the specified Batch exception.
    :param batch_exception:
    """
    print('-------------------------------------------')
    print('Exception encountered:')
    if batch_exception.error and \
            batch_exception.error.message and \
            batch_exception.error.message.value:
        print(batch_exception.error.message.value)
        if batch_exception.error.values:
            print()
            for mesg in batch_exception.error.values:
                print('{}:\t{}'.format(mesg.key, mesg.value))
    print('-------------------------------------------')


# all_data={"cnn": {"link": ["https://www.cnn.com/2019/10/31/politics/world-series-washington-nationals-trump-unity/index.html", "https://www.cnn.com/2019/10/29/us/lebron-james-taco-truck-firefighters-trnd/index.html", "https://www.cnn.com/us/live-news/california-fires-los-angeles-october-2019/index.html", "https://www.cnn.com/2019/10/28/us/lebron-james-evacuates-home-due-to-la-fire-trnd/index.html", "https://www.cnn.com/2019/10/23/sport/nba-china-t-shirt-protest-lakers-clippers/index.html", "https://www.cnn.com/2019/10/23/us/shaquille-oneal-nba-china-intl-hnk-scli/index.html", "https://www.cnn.com/2019/10/23/sport/nba-opening-day-la-lakers-and-la-clippers/index.html", "https://www.cnn.com/2019/10/22/sport/zion-williamson-injury-nba-new-orleans-pelicans-spt-intl/index.html", "https://www.cnn.com/2019/10/16/us/lebron-james-nba-china-controversy-trnd/index.html", "https://www.cnn.com/2019/10/14/us/lebron-james-nba-china-intl-hnk-scli/index.html"]}, "bbc": {"link": ["http://www.bbc.co.uk/news/world-us-canada-44978813", "http://www.bbc.co.uk/news/newsbeat-44681504"]}, "fox": {"link": ["https://www.foxnews.com/sports/leonard-leads-clippers-over-lebron-and-lakers-112-102", "https://www.foxnews.com/transcript/shaq-charles-barkley-argue-over-lebron-james-and-china", "https://www.foxnews.com/sports/taco-tuesdays-lebron-james-sends-food-truck-to-feed-getty-fire-first-responders", "https://www.foxnews.com/sports/lebron-james-anthony-davis-lakers-23-jersey-report", "https://www.foxnews.com/us/getty-fire-mandatory-evacuation-california-los-angeles-wildfire-risk", "https://www.foxnews.com/sports/lebron-james-taco-tuesday-trademark", "https://www.foxnews.com/sports/lebron-james-anthony-davis-trade-lakers-reactions", "https://www.foxnews.com/sports/lebron-james-trade-rumors-lakes-negotiations-report", "https://www.foxnews.com/sports/lebron-james-reaction-magic-johnson-leaving-lakers", "https://www.foxnews.com/sports/andrew-bogut-lebron-james-china-hong-kong-tweet"]}}

def upload_file_to_container(block_blob_client, container_name, file_path):
    """
    Uploads a local file to an Azure Blob storage container.
    :param block_blob_client: A blob service client.
    :type block_blob_client: `azure.storage.blob.BlockBlobService`
    :param str container_name: The name of the Azure Blob storage container.
    :param str file_path: The local path to the file.
    :rtype: `azure.batch.models.ResourceFile`
    :return: A ResourceFile initialized with a SAS URL appropriate for Batch
    tasks.
    """
    blob_name = file_path.decode("utf-8")


    print('Uploading file {} to container [{}]...'.format(file_path,
                                                          container_name))

    block_blob_client.create_blob_from_bytes(container_name,
                                            blob_name,
                                            file_path)

    sas_token = block_blob_client.generate_blob_shared_access_signature(
        container_name,
        blob_name,
        permission=azureblob.BlobPermissions.READ,
        expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=2))

    sas_url = block_blob_client.make_blob_url(container_name,
                                              blob_name,
                                              sas_token=sas_token)

    return batchmodels.ResourceFile(http_url=sas_url, file_path=blob_name)


def get_container_sas_token(block_blob_client,
                            container_name, blob_permissions):
    """
    Obtains a shared access signature granting the specified permissions to the
    container.
    :param block_blob_client: A blob service client.
    :type block_blob_client: `azure.storage.blob.BlockBlobService`
    :param str container_name: The name of the Azure Blob storage container.
    :param BlobPermissions blob_permissions:
    :rtype: str
    :return: A SAS token granting the specified permissions to the container.
    """
    # Obtain the SAS token for the container, setting the expiry time and
    # permissions. In this case, no start time is specified, so the shared
    # access signature becomes valid immediately.
    container_sas_token = \
        block_blob_client.generate_container_shared_access_signature(
            container_name,
            permission=blob_permissions,
            expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=2))

    return container_sas_token

# try:
# 	with open('scraped_articles.json', 'w') as outfile:
# 		json.dump(data, outfile)
# except Exception as e: print(e)

# try:
# 	with open('articles_analyze.json', 'w') as outfile:
# 		json.dump(documents, outfile)
# except Exception as e: print(e)


if __name__ == '__main__':

	start_time = datetime.datetime.now().replace(microsecond=0)
	print('Sample start: {}'.format(start_time))
	print()

	# Create the blob client, for use in obtaining references to
	# blob storage containers and uploading files to containers.

	blob_client = BlockBlobService(
		account_name=config._STORAGE_ACCOUNT_NAME,
		account_key=config._STORAGE_ACCOUNT_KEY)

	# Use the blob client to create the containers in Azure Storage if they
	# don't yet exist.

	input_container_name = 'news-sentiment'
	blob_client.create_container(input_container_name, fail_on_exist=False)

	# # The collection of data files that are to be processed by the tasks.
	# input_file_path = [os.path.join(sys.path[0], 'query.txt'),]

	# Upload the data files.
	with open("query.csv") as f:
		reader = csv.reader(f)
		input_words = list(reader)[0]

	# for word in input_words:	
	# 	print(word.encode())	

	input_file = [upload_file_to_container(blob_client, input_container_name, word.encode()) for word in input_words]

	# Create a Batch service client. We'll now be interacting with the Batch
	# service in addition to Storage
	credentials = batch_auth.SharedKeyCredentials(config._BATCH_ACCOUNT_NAME,
												  config._BATCH_ACCOUNT_KEY)

	batch_client = batch.BatchServiceClient(
		credentials,
		batch_url=config._BATCH_ACCOUNT_URL)


	try:
		# Create the pool that will contain the compute nodes that will execute the
		# tasks.
		create_pool(batch_client, config._POOL_ID)

		# Create the job that will run the tasks.
		create_job(batch_client, config._JOB_ID, config._POOL_ID)


		add_tasks(batch_client, config._JOB_ID, input_file)

		# Pause execution until tasks reach Completed state.
		wait_for_tasks_to_complete(batch_client,
								   config._JOB_ID,
								   datetime.timedelta(minutes=30))

		print("  Success! All tasks reached the 'Completed' state within the "
			  "specified timeout period.")

	except batchmodels.BatchErrorException as err:
		print_batch_exception(err)
		raise


	# Print out some timing info
	end_time = datetime.datetime.now().replace(microsecond=0)
	print()
	print('Sample end: {}'.format(end_time))
	print('Elapsed time: {}'.format(end_time - start_time))
	print()

	batch_client.job.delete(config._JOB_ID)
	batch_client.pool.delete(config._POOL_ID)

