
from flask import (Flask, render_template, redirect, request,
                   send_from_directory, )

def species_entry():
    return render_template('species.html')