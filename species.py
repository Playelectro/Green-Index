
from flask import (Flask, render_template, redirect, request,
                   send_from_directory, )

def species_entry(list):
    return render_template('species.html', list=list)
