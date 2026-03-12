# bilt_transactions

The web site for the Bilt 2.0 credit card has a wallet section where cardholders can view transactions and a section in the card management page to download statements in PDF format, ~~but there is currently no way to export transactions in CSV format so they can be imported into a spreadsheet or financial management software.~~

#### Update (Mar 10)

Bilt now allows users to export data to a CSV.  I'll leave this repo here for a while, maybe it will be useful again in the future?

#### Synopsis

This repo has a simple command line application that will extract transactions from a web page and format them as CSV records.  Extracting transactions is a two-step process:

1. log in to the Bilt web site, go to the wallet to view the transactions you want, and use your browser's "save page" menu to save the HTML source of the web page
2. open a terminal window and type the command that runs the script and saves the output.

## Caveats

Users must be familiar with running command line applications.  Installing the script is simple if a Python environment is set up.  For most people that is probably the case, but ideally users will know how to create a new Python environment for this script.

The test data is very skimpy -- one month's worth of transactions from one user.  If you run into any problems with your own data and would like to help us improve the program see the section on **Debugging** below.

The output file is extremely simple, with only three columns for each transaction:  **date**, **payee**, and **amount**.  That's all there is on the web page, and that's all you will get in the CSV file.

## Installation

The easiest way to install the script is to tell PIP to get it from GitHub.  Open a terminal window and type this command:

```bash
$ pip install git+https://github.com/conery/bilt_transactions.git
```

An alternative (if you want to look at the code) is to download or clone the repo, `cd` to the project folder, and install it locally:

```bash
$ pip install .
```

## Usage

As mentioned above, creating a CSV file with `bilt_transactions` is a two-step process.

### 1.  Download Transactions 

To download a file with Bilt Card transactions you need a browser that saves pages in [MHTML](https://en.wikipedia.org/wiki/MHTML) format.  Chrome (and Arc, which is built with Chrome) supports this format, Safari does not. 

To export a set of transactions, log in to your Bilt account.  Open your wallet and scroll down to the recent transactions section, then click "View All".

> **Important:** make sure you are viewing transactions in the Wallet and not looking at a monthly statement.  If you download a statement you will be getting a PDF file, not the MHTML file that can be parsed by `bilt_transactions`.

By default you will see transactions for the last 30 days but you can select a previous month.  Once you are viewing the transactions you want to export choose File > Save Page As... from the browser menu.  

The browser will pop up a dialog to ask you where you want to save the file.  Give it a name if you want -- for example `February.mhtml`.  

Most importantly, tell the browser you want an MHTML file.  In Chrome, at the bottom of the dialog, where you see the Format options, choose **Webpage, Single File.** 

### 2.  Parse the MHTML File

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

### Debugging

Two kinds of errors might pop up when you run the script on your own data:

- missing transactions -- a transaction that is displayed in your browser is not showing up in your CSV file

- garbled data -- text is appearing in the wrong column, for example you see a payee description in the amount column

What this probably means is the parser lost track of where it was in the file.  The parsing algorithms is based on a simple state machine that transitions between states as it finds each paragraph.  

If you include `--tokens` as part of the command the script will print all the paragraphs it finds in the file:

```shell
$ bilt_transactions --tokens tests/demo.mhtml
<p class="sc-iOyoOp hjBxMK">February 9, 2026</p>
<p class="sc-iOyoOp gSHtoa sc-hwpaKV gvdukv">Best Buy</p>
<p class="sc-iOyoOp gSHtoa">$39.99</p>
<p class="sc-iOyoOp hjBxMK">February 8, 2026</p>
<p class="sc-iOyoOp gSHtoa sc-hwpaKV gvdukv">Bill &amp; Tim's Barbecue</p>
<p class="sc-iOyoOp gSHtoa">$28.26</p>
<p class="sc-iOyoOp gSHtoa sc-hwpaKV gvdukv">Art House</p>
<p class="sc-iOyoOp gSHtoa">$13.20</p>
```

If you are not a Python programmer but would like to help us improve the script:

1. run the script with the `--tokens` option and save the output in a file (it will be a plain text file, you can name it anything you want, but the convention is to use `.txt` as the extension)

2. **edit the file** -- to keep your data private, you can edit the payees and amounts, but please leave the dates as they are, if possible

3. open a new issue (click on Issues at the top of this page); include your file and describe the output you were expecting


Of course, if you are a Python programmer and want to dig in to the code, feel free, and send us a pull request with your suggested improvements.

> Documentation will be included in a future release.
>

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`bilt_transactions` was created by John Conery. It is licensed under the terms of the MIT license.

## Credits

`bilt_transactions` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

MHTML files are parsed with [`unmhtml`](https://pypi.org/project/unmhtml/0.2.0/).

Terminal output is generated with [`rich`](https://rich.readthedocs.io/en/latest/introduction.html).

