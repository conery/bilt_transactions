# bilt_transactions

The web site for the Bilt 2.0 credit card has a wallet section where cardholders can view transactions and a section in the card management page to download statements in PDF format, but there is currently no way to export transactions in CSV format so they can be imported into a spreadsheet or financial management software.

This repo has a simple command line application that will extract transactions from a web page and format them as CSV records.  Extracting transactions is a two-step process:

1. log in to the Bilt web site, go to the wallet to view the transactions you want, and use your browser's "save page" menu to save the HTML source of the web page
2. open a terminal window and type the command that runs the script and saves the output.

## Caveats

Users must be familiar with running command line applications.  Installing the script is simple if a Python environment is set up.  For most people that is probably the case, but ideally users will know how to create a new Python environment for this script.

The test data is very skimpy -- one month's worth of transactions from one user.  If you run into any problems create a new issue.

## Installation

The easiest way to install the script is to tell PIP to get it from GitHub:

```bash
$ pip install git+https://github.com/conery/bilt_transactions.git
```

Alternatively, download or clone the repo, cd to the project folder, and install it locally:

```bash
$ pip install .
```

## Usage

As mentioned above, creating a CSV file with `bilt_transactions` is a two-step process.

### Download Transactions 

To download a file with Bilt Card transactions you need a browser that saves pages in [MHTML](https://en.wikipedia.org/wiki/MHTML) format.  Chrome (and Arc, which is built with Chrome) supports this format, Safari does not. 

To export a set of transactions, log in to your Bilt account.  Open your wallet and scroll down to the recent transactions section, then click "View All".

> **Important:** make sure you are viewing transactions in the Wallet and not looking at a monthly statement.  If you download a statement you will be getting a PDF file, not the MHTML file that can be parsed by `bilt_transactions`.

By default you will see transactions for the last 30 days but you can select a previous month.  Once you are viewing the transactions you want to export choose File > Save Page As... from the browser menu.  

The browser will pop up a dialog to ask you where you want to save the file.  Give it a name if you want -- for example `February.mhtml`.  

Most importantly, tell the browser you want an MHTML file.  In Chrome, at the bottom of the dialog, where you see the Format options, choose **Webpage, Single File.** 

### Parse the MHTML File

To run `bilt_transactions` simply type the script name followed by the path to the MHTML file you want to process.  The script will print a CSV header line and then the CSV records for all the transactions it finds.  Here is an example, using the test data packaged with the script:

```
$ bilt_transactions tests/demo.mhtml
date,description,amount
2026-02-09,Best Buy,39.99
2026-02-08,Bill &amp; Tim's Barbecue,28.26
2026-02-08,Art House,13.2
```

To save the transactions in a CSV file simply redirect the output, _e.g._

```
$ bilt_transactions tests/demo.mhtml > demo.csv
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`bilt_transactions` was created by John Conery. It is licensed under the terms of the MIT license.

## Credits

`bilt_transactions` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

MHTML files are parsed with [`unmhtml`](https://pypi.org/project/unmhtml/0.2.0/).

Terminal output is generated with [`rich`](https://rich.readthedocs.io/en/latest/introduction.html).

