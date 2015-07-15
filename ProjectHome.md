# Walrus Pioneer (The project is paused due to some external force. Sorry for this!) #
## Tools to provide easy access to the Walrus service of Eucalyptus project ##

The tools are aiming at providing a easier way for Eucalyptus users to access to the Walrus service.

Most tools currently on the Internet are for Amazon's S3 service. Though Walrus is compatible with S3 in many aspects, a specific tool for Walrus is necessary. The tool is using REST to communicate with the Walrus. We want to create tools to fully support Walrus, and may be compatible with S3.

Secondly, I have tried several open source or free software tools for S3, and I found most of them are for advanced users. We want to make tools allowing normal users can also enjoy the service while advanced users can still maintain there flexibility.

## Components ##
  * A high-level library
  * A command line tool
  * A GUI tool

## Notice ##
The tools are proposed to be written in Python 2.6 which make them available to various platforms.

## Current Features ##
  * List the contents under root or other buckets
  * Create a bucket
  * Delete a bucket
  * Upload files
  * Download files
  * Delete files
  * Check the access control list of each file/bucket

## Proposed Features ##
  * More commands support, such access control
  * Nicer output of command line tools
  * A better error process mechanism
  * GUI support