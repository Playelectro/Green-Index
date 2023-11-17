
from flask import (Flask, render_template, redirect, request,
                   send_from_directory, )

sp_list = None

def species_entry(list):
    sp_list=list
    
    args = request.args
    
    mrk = None
    
    if args.get('name') is not None:
        
        name = args.get('name')
        
        for marker in sp_list:
            name_mrk = marker['name']
            if name_mrk == name:
                    mrk = marker

        
    return render_template('species.html', list=list)
