## Installing Wordle for Development

Create a new conda environment.  Say you want to call the environment 'wordle'

    conda env create -n wordle --file environment.yml

Activate the new environemnt

    conda activate wordle

Install this package in "development mode", so you can go "import wordle"

    invoke develop

To run formatting checks, autoformatting and unit tests

    invoke check
    invoke format
    invoke test
