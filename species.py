
from flask import (Flask, render_template, redirect, request,
                   send_from_directory, )

sp_list = None

def species_entry(list):
    sp_list=list
    return render_template('species.html', list=list)
