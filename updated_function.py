#!usr/bin/env python3
"""
Module that contains the functions for the SATAlytics GUI.
"""

from __future__ import division
import heapq
import pandas as pd
import matplotlib as mpl
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from tkinter.filedialog import askdirectory


def residues_graph(resultfile, client, crop, date = "all", hide = False, fsize=20): ## n.1
    """ This function creates a graph on average amount of residues per client 
    for a single crop in a certain time span, including the limit. 
    Variables:
        - Client: Compulsory (Column Cliente)
        - Crop: Compulsory (Column Gruppo_Prodotto)
        - Date: Optional. 
    Returns list of figures as strings.
    """
    counter_to_save_the_day = ""
    if hide == False:
        counter_to_save_the_day = " CLIENTS SHOWN"
    elif counter_to_save_the_day == True:
        counter_to_save_the_day = " CLIENTS HIDDEN"
    data = resultfile[resultfile["Gruppo_prodotto"] == crop]
    data = data[data["Cliente"] == client]
    dates = list(set(data["ANNO"].tolist()))
    
    if date != "all":
        data[data["ANNO"] == str(date)]
        dates = [date]
    
    fig_list = []
    
    client_count = 1
    client_dic = {}
    for year in dates: # Will produce a graph for each date.
        prod = {}
        err_val = {}
        data2 = data[data["ANNO"] == year]
        list_check = []
        for element in data["Prova"]:
            # This will hide the compound names if hide == True
            if hide == False:
                name = element + "_" + str(year)
            if hide == True:
                name = element[:15] + "_" + str(year)
                client_dic[str(name)] = element+ "_" + str(year)
                
            prev = data2[data2["Prova"] == element]
            # prev contains the data from a single year, client, crop and compound
            prev2 = prev["Risultato"].astype(str).str.replace(".", "").str.replace(',','.')
            # prev2 contains the concentration stored in prev
            if len(prev["Limite"].tolist()) > 0:
                threshold = prev["Limite"].tolist()[0]
            if len(prev["Limite"].tolist()) == 0:
                threshold = "nan"
            try:
                if not element + "_" + str(year) in list_check:
                    list_check.append(element + "_" + str(year))
                    threshold = float(str(threshold).replace(".", "").replace(",", "."))
                    client_count = client_count + 1
                    prod[name] = [np.mean(list(map(float, prev2.tolist()))), threshold]
            except ValueError:
                err_val[name] = prev2.tolist() # This is just to store the weird values
        
        sizes = []
        label = []
        limits = []
        count = 0
        for element in sorted(prod.keys()):
            sizes.append(prod[element][0])
            label.append(str(element))
            bool_th =  prod[element][0] > prod[element][1]
            if bool_th == True and prod[name][1] != float("nan"):
                limits.append(count)
            count = count + 1

        start = 0
        limits1 = limits            
        while start < len(sizes):
            fig = plt.figure()
            fig.set_size_inches(18.0, 18.0)
            sizes2 = list(map(float, sizes[start:start+30]))
            label2 = label[start:start+30]

            x2 = range(len(sizes2))
            plt.xticks(rotation='vertical', size=fsize)
            plt.yticks(size=fsize)
            barlist = plt.bar(x2, sizes2, width=0.4, tick_label = label2, \
                              align='center')
            
            limits2 = []
            for element in limits1:
                if element < 30:
                    barlist[element].set_color('indianred')
                else:
                    limits2.append(element-30)
                    
            limits1 = limits2 

            # titles of graphs
            if date == "all":
                year1 = dates[0]
                year2 = dates[-1]
                if year1 == year2:
                    fig_title = "Average concentration of all compounds found in " + crop + " from " + client + " in " + str(year1) + ' ' + str(int(1+(start/30))) + counter_to_save_the_day + " font " + str(fsize)
                else:
                    fig_title = "Average concentration of all compounds found in " + crop + " from " + client + " in {}-{}".format(year1, year2) + " " + str(int(1+(start/30))) + counter_to_save_the_day + " font " + str(fsize)
            else:
                fig_title = "Average concentration of all compounds found in " + crop + " from " + client + " in " + str(date) + " " + str(int(1+(start/30))) + counter_to_save_the_day + " font " + str(fsize)
            plt.title(fig_title, fontweight= "bold", size=fsize)
            plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%f mg/kg'))
            mpl.rcParams['font.size'] = 20
            
            fig_name = "{}.png".format(fig_title)
            fig.savefig(fig_name, dpi=100, bbox_inches="tight")
            fig_list.append(fig_name)
            
            start = start + 30

        if hide == True:
            data_client = pd.DataFrame.from_dict(client_dic, orient="index")
            choose_dr = askdirectory()
            writer = pd.ExcelWriter('{}\\Compound_index_on_{}_{}_{}.xlsx'.format(choose_dr, crop, client, str(date)), engine='xlsxwriter')
            data_client.to_excel(writer, sheet_name='Sheet1')
            writer.save()
        
        return(fig_list)


def compound_per_client(resultfile, infofile, compound, crop, date ="all", hide=False, fsize=20): ## function 5
    """This function creates a graph on average amount of residues in a single 
    crop for a single client in a certain time span, including the limit.
    Variables:
        - Compound: compulsory (column Prova)
        - Crop: compulsory (column Gruppo_prodotto)
        - Date: optional
        - Hide: optional - default: False
    """
    fig_list = []

    data = resultfile[resultfile["Gruppo_prodotto"] == crop]
    data = data[data["Prova"] == compound]
    dates = list(set(data["ANNO"].tolist()))
    
    if date != "all":
        data[data["ANNO"] == str(date)]
        dates = [date]
    infofile = infofile[infofile["Gruppo_prodotto"] == crop]

    client_count = 0
    client_dic = {}
    hidden_dic = {}
    for year in dates:#Creates a graph per year
        infofile = infofile[infofile["ANNO"] == year]
        
        reduced_info = pd.DataFrame(columns= infofile.columns.values)
        for trials in set(infofile["Analisi_richiesta_EX_NOTE_LAB"].tolist()):
            trial = str(trials)
            if compound in trial or "Multiresiduale Full" in trial:
                reduced_info = reduced_info.append(infofile[infofile\
                                ["Analisi_richiesta_EX_NOTE_LAB"] == trials])
    
        for sample in set(reduced_info["N_campione"].tolist()):
            if not sample in set(resultfile["N_campione"].tolist()):
                infodata= infofile[infofile["N_campione"]==sample]
                if not infodata["Cliente"].tolist()[0] in client_dic:
                    client_dic[infodata["Cliente"].tolist()[0]] = [0]
                if infodata["Cliente"].tolist()[0] in client_dic:
                    client_dic[infodata["Cliente"].tolist()[0]].append(0)

        prod = {}
        err_val = {}
        data2 = data[data["ANNO"] == year]
        list_check = []
        # data2 contains the information for single crop, year and compound.
        for element in data["Cliente"]:
            if hide == False:
                name = element + "_" + str(year)
            if hide == True:
                name = client_count
                
            prev = data2[data2["Cliente"] == element]
            # prev contains the information for single crop, year, compound and client.
            prev2 = prev["Risultato"].astype(str).str.replace(".", "").str.replace(',','.')

            prev_list = list(map(float, prev2.tolist()))
            if len(prev["Limite"].tolist()) > 0:
                threshold = prev["Limite"].tolist()[0]
            if len(prev["Limite"].tolist()) == 0:
                threshold = "nan"

            if element in client_dic:
                for cero in client_dic:
                    prev_list.append(client_dic[cero][0])

            try:
                if not element + "_" + str(year) in list_check:
                    list_check.append(element + "_" + str(year))
                    client_count = client_count + 1
                    threshold = float(str(threshold).replace(".", "").replace(",", "."))
                    prod[name] = [np.mean(prev_list), threshold]
                    hidden_dic["Client " + str(name)] = element + "_" + str(year)
            except ValueError:
                err_val[name] = prev2.tolist()

        counter_to_save_the_day = ""
        if hide == True:
            counter_to_save_the_day = " CLIENTS HIDDEN"
        else:
            counter_to_save_the_day = " CLIENTS SHOWN"
                
        # Creates bar charts in groups of 30 clients:
        label = []
        sizes = []
        limits = []
        x = range(len(prod))
        count = 0
        for element in sorted(prod.keys()):
            if str(prod[element][0]) != "nan":
                sizes.append(prod[element][0])
            if str(prod[element][0]) == "nan":
                sizes.append(0.0)
            label.append("Client " + str(element))
            bool_th =  prod[element][0] > prod[element][1]
            if bool_th == True and prod[element][1] != float("nan"):
                limits.append(count)
            count = count + 1

        if len(sizes) <= 30:
            fig = plt.figure()
            fig.set_size_inches(18.0, 18.0)
            plt.xticks(rotation='vertical', size=fsize)
            plt.yticks(size=fsize)
            barlist = plt.bar(x, sizes, width=0.4, tick_label = label)
            for element in limits:
                barlist[element].set_color('indianred')

            # titles of graphs
            if date == "all":
                year1 = dates[0]
                year2 = dates[-1]
                if year1 == year2:
                    fig_title = "Average concentration of " + compound + " in " + crop + " in " + str(year1) + str(counter_to_save_the_day) + " font " + str(fsize)
                else:
                    fig_title = "Average concentration of " + compound + " in " + crop + " in {}-{}".format(year1, year2) + str(counter_to_save_the_day) + " font " + str(fsize)
            else:
                fig_title = "Average concentration of " + compound + " in " + crop + " in " + str(date) + str(counter_to_save_the_day) + " font " + str(fsize)

            plt.title(fig_title, fontweight="bold", size=fsize)
            plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%f mg/kg'))
            mpl.rcParams["font.size"] = 20
            fig_name = "{}.png".format(fig_title)
            fig.savefig(fig_name, dpi=100, bbox_inches="tight")
            fig_list.append(fig_name)  

        if len(sizes) > 30:
            start = 0
            limits1 = limits            
            while start < len(sizes):
                fig = plt.figure()
                fig.set_size_inches(18.0, 18.0)

                sizes2 = list(map(float, sizes[start:start+30]))
                label2 = label[start:start+30]

                x2 = range(len(sizes2))
                plt.xticks(rotation='vertical', size=fsize)
                plt.yticks(size=fsize)
                barlist = plt.bar(x2, sizes2, width=0.4, tick_label = label2, \
                                  align='center')
                
                limits2 = []
                for element in limits1:
                    if element < 30:
                        barlist[element].set_color('indianred')
                    else:
                        limits2.append(element-30)
                        
                limits1 = limits2 
                
                # titles of graphs
                if date == "all":
                    year1 = dates[0]
                    year2 = dates[-1]
                    if year1 == year2:
                        fig_title = "Average concentration of " + compound + " in " + crop + " in " + str(year1) + str(counter_to_save_the_day) +" " + str(int(1+(start/30))) + " font " + str(fsize)
                    else:
                        fig_title = "Average concentration of " + compound + " in " + crop + " in {}-{}".format(year1, year2) + str(counter_to_save_the_day) + " " + str(int(1+(start/30))) + " font " + str(fsize)
                else:
                    fig_title = "Average concentration of " + compound + " in " + crop + " in " + str(date) + str(counter_to_save_the_day) + " " + str(int(1+(start/30))) + " font " + str(fsize)

                plt.title(fig_title, \
                          fontweight= "bold", size=fsize)
                plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%f mg/kg'))
                mpl.rcParams["font.size"] = 20
                
                fig_name = "{}.png".format(fig_title)   
                fig.savefig(fig_name, dpi=100, bbox_inches="tight")
                fig_list.append(fig_name)  

                start = start + 30
    
    if hide == True:            
        data_client = pd.DataFrame.from_dict(hidden_dic, orient="index")
        choose_dr = askdirectory()
        writer = pd.ExcelWriter('{}\\Client_index_on_{}_{}_{}.xlsx'.format(choose_dr, compound, crop, str(date)), engine='xlsxwriter')
        data_client.to_excel(writer, sheet_name='Sheet1')
        writer.save()
    return(fig_list)


def samples_product_type(resultfile, client = "all", detail = True,\
                         date = "all", fsize=20): # n.3 and n.6
    """ This function creates a graph on number of samples per product/cultivar
    Variables:
        - Client = optional"""
    
    fig_list = []

    if client != "all":
        resultfile = resultfile[resultfile["Cliente"] == str(client)]

    if date == "all":
        years = list(set(resultfile["ANNO"].tolist()))
    else:
        resultfile = resultfile[resultfile["ANNO"] == date]
        years = [str(date)]
    
    # This is to choose if we want the pie chart for product detail:
    if detail == True:
        product_detail = "dettaglio_prodotto"
    if detail == False:
        product_detail = "Gruppo_prodotto"   
    
    for year in years:
        prod = {}
        explode = []
        for element in resultfile[product_detail]:
            if not element in prod:
                data2 = resultfile[resultfile[product_detail] == element]
                samples = list(set(data2["N_campione"].tolist()))
                # Creates a list without repetitions
                prod[element] = len(samples)
        # Prod dictionary structure -> Product: Amount of times it has been analyzed

        # Create pie chart:
        sizes = []
        labels = []
        
        if "..." in prod.keys():
            del prod["..."]

        # if dict is empty, show message in empty figure
        if not prod:
            fig = plt.figure(figsize=(18.0, 18.0))
            if date != "all":
                message = "No more detailed results detected for " + client + " in " + str(year)
            else: 
                year1 = years[0]
                year2 = years[-1]
                if year1 == year2:
                    message = "No more detailed results detected for " + client + " in " + str(year1)
                else:
                    message = "No more detailed results detected for " + client + " in {}-{}".format(year1, year2)
            text = fig.text(0.5, 0.5, message, ha='center', va='center', size=20)
            text.set_path_effects([path_effects.Normal()])
            
            fig_name = "{}.png".format(message)   
            fig.savefig(fig_name, dpi=100, bbox_inches="tight")
            fig_list.append(fig_name)            

        else:
            max_labels = heapq.nlargest(10, prod, key=prod.get)
            for element in max_labels:
                sizes.append(prod[element])
                labels.append(element)
                explode.append(0.1)      
                
            other = 0
            for element in prod:
                if not element in max_labels:
                    other = other + prod[element]
            
            colors = ['lightskyblue', 'lightblue', 'cyan', "coral", "gold",\
                      "lightcoral", "lavender", "cyan", "lime", "lightgreen","aquamarine"]
            
            if other != 0:
                labels.append("Other")
                sizes.append(other)
                explode.append(0.1)
            fig = plt.figure()
            fig.set_size_inches(18.0, 18.0)

            # create titles
            if client == "all":
                fig_title = "Amount of samples for all clients in " + str(year) + " font " + str(fsize)
            elif date == "all":
                year1 = years[0]
                year2 = years[-1]
                if year1 == year2:
                    fig_title = "Amount of samples for " + client + " in " + str(year1) + " font " + str(fsize)
                else:
                    fig_title = "Amount of samples for " + client + " in {}-{}".format(year1, year2) + " font " + str(fsize)
            else:
                fig_title = "Amount of samples for " + client + " in " + str(year) + " font " + str(fsize)

            if detail == True:
                fig_title += " DETAILED"
            plt.title(fig_title, fontweight= "bold", size=fsize)

            plt.pie(np.array(sizes), labels=labels, shadow=True, colors=colors, \
                    explode=explode, autopct='%1.1f%%', pctdistance=0.8, startangle=150)
            mpl.rcParams["font.size"]=24
            
            fig_name = "{}.png".format(fig_title)   
            fig.savefig(fig_name, dpi=100, bbox_inches="tight")
            fig_list.append(fig_name)  

    return(fig_list)


def residues_graph_esp(resultfile, infofile, client, crop, compound, fsize=20):  ## 7
    """ This function creates a graph with the average concentration of a compound 
    through the year for a single client.
    Variables:
        - Client: Compulsory (column Cliente)
        - Crop: Compulsory (column Gruppo_prodotto)
        - Compound: Compulsory (column Prova)
    Things to do: 
        - Make client optional and use this function to give an average
        concentration.
        - Order dates chronologicaly
        """
    messages  = None
    fig_list = []
    
    data = resultfile[resultfile["Gruppo_prodotto"] == crop]
    data = data[data["Cliente"] == client]
    data = data[data["Prova"] == compound]
    dates = list(set(data["Data_Arrivo"].tolist()))
    years = list(set(data["ANNO"].tolist()))
    
    prod = {}
    err_val = {}
    for date in dates:
        data2 = data[data["Data_Arrivo"] == date]
        
        for element in data2["N_campione"]:
            name = "Sample_" + str(int(element)) + "_" + str(date)[:-9]
            prev = data2["Risultato"].astype(str).str.replace(".", "").str.replace(',','.')
            if len(data2["Limite"].tolist()) > 0:
                threshold = data2["Limite"].tolist()[0]
            if len(data2["Limite"].tolist()) == 0:
                threshold = "nan"
            try:
                threshold = float(str(threshold).replace(".", "").replace(",", "."))
                prod[name] = [np.mean(list(map(float, prev.tolist()))), threshold, date]

                
            except ValueError:
                err_val[name] = prev.tolist()
    
    infofile = infofile[infofile["Gruppo_prodotto"] == crop]
    infofile = infofile[infofile["Cliente"] == client]
    
    date_infofile = pd.DataFrame(columns= infofile.columns.values)
    for year in set(resultfile["ANNO"].tolist()):
        date_infofile = date_infofile.append(infofile[infofile["ANNO"] == year])
        
    infofile = date_infofile
    
    reduced_info = pd.DataFrame(columns= infofile.columns.values)
    for trials in set(infofile["Analisi_richiesta_EX_NOTE_LAB"].tolist()):
        trial = str(trials)
        if compound in trial or "Multiresiduale Full" in trial:
            reduced_info = reduced_info.append(infofile[infofile\
                            ["Analisi_richiesta_EX_NOTE_LAB"] == trials])

    for sample in reduced_info["N_campione"].tolist():
        if not sample in set(resultfile["N_campione"].tolist()):
            name = "Sample_" + str(int(sample)) + "_" +\
            str(reduced_info[reduced_info["N_campione"] == sample]\
                ["Data_Arrivo"].tolist()[0])[:-9]
            prod[name] = [0,0, reduced_info[reduced_info["N_campione"] == sample]\
                 ["Data_Arrivo"].tolist()[0]]


    # Create bar chart:
    labels = []
    sizes = []
    limits = []
    x = range(len(prod))
    count = 0
    for el in sorted(prod.items(), key=lambda prod: prod[1][2]): # This sorts the dates
        element = el[0] # This is necessary because previous function produces a tuple
        labels.append(element)
        sizes.append(prod[element][0])
        if prod[element][0] > prod[element][1] and prod[element][1] != float("nan"):
            limits.append(count)
        count = count + 1
    
    fig = plt.figure()
    if len(sizes) <= 20: # Only one graph is needed.
        if sum(sizes) == 0: # Checks if the graph is empty.
            fig = plt.figure(figsize=(18.0, 18.0))
            message = "No results detected between " + str(labels[0]) + \
                " and " + str(labels[-1])
            text = fig.text(0.5, 0.5, message, ha='center', va='center', size=20)
            text.set_path_effects([path_effects.Normal()])
            
            messages = [message]
            
            fig_name = "{}.png".format(message)   
            fig.savefig(fig_name, dpi=100, bbox_inches="tight")
            fig_list.append(fig_name)
            # This saves an images with the message
        
        if sum(sizes) != 0: # Saves the normal graph
            fig = plt.figure()
            fig.set_size_inches(18.0, 18.0)  
            plt.xticks(rotation='vertical', size=fsize)
            plt.yticks(size=fsize)
            barlist = plt.bar(x, sizes, width=0.4, tick_label = labels)
            for element in limits:
                barlist[element].set_color('indianred')
            # titles of graphs
            year1 = years[0]
            year2 = years[-1]
            if year1 == year2:
                fig_title = "Concentration of " + compound + " in " + crop + " from " + client + " in " + str(year1) + " font " + str(fsize)
            else:
                fig_title = "Concentration of " + compound + " in " + crop + " from " + client + " in {}-{}".format(year1, year2) + " font " + str(fsize)
            plt.title(fig_title, fontweight = "bold", size=fsize)
            plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%f mg/kg'))
            mpl.rcParams["font.size"] = 20
            fig_name = "{}.png".format(fig_title)   
            fig.savefig(fig_name, dpi=100, bbox_inches="tight")
            fig_list.append(fig_name)
    
    if len(sizes) > 20: # Creates more than one graph
        ind = 20
        limits1 = limits
        results_count = 0
        list_no = []
        while ind-20 < len(sizes):
            sizes1 = sizes[ind-20:ind]
            labels1 = labels[ind-20:ind]
            check = results_count
            
            if sum(sizes1) == 0.0: # Checks if the graph is empty.
                # Following if statements are to give all the no results found 
                # in one images.
                if check != results_count:
                    if list_no != []:
                        list_no.append(labels1[-1])
                    if list_no == []:
                        list_no.append(labels1[0], labels1[-1])
                if check == 0 and results_count == 0:
                    if list_no != []:
                        list_no.append(labels1[-1])
                    if list_no == []:
                        list_no = [labels1[0], labels1[-1]]

                if (check != 0 and check == results_count) or labels1[-1] == labels[-1]:
                    # This if statement is the one that saves the messages
                    messages = []
                    fig = plt.figure(figsize=(18.0, 18.0))
                    message = "No results detected between " + str(list_no[0]) + \
                    " and " + str(list_no[-1])
                    text = fig.text(0.5, 0.5, message, ha='center', va='center', size=20)
                    text.set_path_effects([path_effects.Normal()])
                    fig_name = "{}.png".format(message)   
                    fig.savefig(fig_name, dpi=100, bbox_inches="tight")
                    fig_list.append(fig_name)
                    
                    fig_list.append(message)
                    list_no = []
                    check = 0
                    results_count = 0
                
                # Limits indexes need to be updated
                limits2 = []
                    
                for number in limits1:
                    limits2.append(number-20)
                    
                limits1 = limits2
                
            if sum(sizes1) != 0.0: # Saves the normal graph
                results_count = results_count + 1
                fig = plt.figure()
                fig.set_size_inches(18.0, 18.0)        
                plt.xticks(rotation='vertical', size=fsize)
                plt.yticks(size=fsize)
                barlist = plt.bar(range(len(sizes1)), sizes1, width=0.4, \
                                  tick_label = labels1)
                
                limits2 = []
                for element in limits1:
                    if element < 20:
                        barlist[element].set_color('indianred')
                    else:
                        limits2.append(element-20)
                        
                limits1 = limits2    
                
             # titles of graphs
                year1 = years[0]
                year2 = years[-1]
                if year1 == year2:
                    fig_title = "Concentration of " + compound + " in " + crop + " from " + client + " in " + str(year1) + " " + str(int(ind/20)) + " font " + str(fsize)
                else:
                    fig_title = "Concentration of " + compound + " in " + crop + " from " + client + " in {}-{}".format(year1, year2) + " " + str(int(ind/20)) + " font " + str(fsize)

                plt.title(fig_title, fontweight = "bold", size=fsize)
                plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%f mg/kg'))
                mpl.rcParams["font.size"] = 20
                
                fig_name = "{}.png".format(fig_title)   
                fig.savefig(fig_name, dpi=100, bbox_inches="tight")
                fig_list.append(fig_name)
            
            ind = ind + 20

    return(fig_list)
        # This update is just to make sure that the graph is not messy, dividing
        # the samples in groups of 20


def number_of_molecules(infofile, client = "all", date = "all", fsize=20): ## Function 4
    """ This function creates a graph on average number of molecules per crop
    over a certain time span.
    Variables:
        Date: optional"""   
    fig_list = []

    if date != "all":
        infofile = infofile[infofile["ANNO"] == str(date)]
    if client != "all":
        infofile = infofile[infofile["Cliente"] == client]
    years = list(set(infofile["ANNO"].tolist())) 
    
    for year in years: # Produces a graph per year
        data2 = infofile[infofile["ANNO"] == year]
        prod = {}
        for element in set(data2["Gruppo_prodotto"].tolist()):
            if not element in prod:
                data = data2[data2["Gruppo_prodotto"] == element]
                list_check = set(data["N_campione"].tolist())
                # data contains the information for a single crop in a year
                prev = []
                for sample in list_check:
                    esp_data = data[data["N_campione"]==sample]
                    if float(esp_data["N_Molecole"]) != 0.0 and str(float(esp_data["N_Molecole"].tolist()[0])) != "nan":
                        prev.append(float(esp_data["N_Molecole"]))
                # prev contains a list with all the trials to that especific crop excluding nans and 0
                if prev != []:
                    prod[element] = np.mean(prev)
                    # It is storing the average

        # Create bar chart:
        sizes = []
        labels = []
        explode = [0.1]

        max_labels = heapq.nlargest(20, prod, key=prod.get)
        # It selects the 20 greatest averages
        
        for element in max_labels:
            sizes.append(prod[element])
            labels.append(element)
            explode.append(0.1)

        fig = plt.figure()
        fig.set_size_inches(18.0, 18.0)  
        plt.xticks(rotation='vertical', size=fsize)
        plt.yticks(size=fsize)

        if client == "all":
            fig_title = "Average amount of analyses per product for all clients in " + str(year) + " font " + str(fsize)
        elif date == "all":
            year1 = years[0]
            year2 = years[-1]
            if year1 == year2:
                fig_title = "Average amount of analyses for " + client + " in " + str(year1) + " font " + str(fsize)
            else:
                fig_title = "Average amount of analyses for " + client + " in {}-{}".format(year1, year2) + " font " + str(fsize)
        else:
            fig_title = "Average amount of analyses for " + client + " in " + str(year) + " font " + str(fsize)

        plt.title(fig_title, fontweight = "bold", size=fsize)
        plt.bar(range(len(sizes)), sizes, width=0.4, tick_label = labels, color="aquamarine")
        mpl.rcParams["font.size"] = 20
        fig_name = "{}.png".format(fig_title)   
        fig.savefig(fig_name, dpi=100, bbox_inches="tight")
        fig_list.append(fig_name) 

    return(fig_list) 


def threshold_pie(resultfile, infofile, date="all", client="all", detail = False, fsize=20): ## 7
    """ This function creates a graph on percentage of samples that exceeds 
    the limit in timeline.
    Variables:
        - Date: optional"""
    fig_list = []

    if date != "all":
        resultfile = resultfile[resultfile["ANNO"] == date]
        infofile = infofile[infofile["ANNO"] == str(date)]
    if client != "all":
        resultfile = resultfile[resultfile["Cliente"] == str(client)]
        infofile = infofile[infofile["Cliente"] == str(client)]
    
    list2 = []
    for element in resultfile['Classi_Ris_Lim_perc']:
        element = str(element)
        if "Tra 0 e 30" in element:
            list2.append("Tra 0 e 30")
        if "Tra 30 e 50" in element:
            list2.append("Tra 30 e 50")
        if "Tra 50 e 80" in element:
            list2.append("Tra 50 e 80")
        if "Tra 80 e 100" in element:
            list2.append("Tra 80 e 100")
        if "Maggiore o uguale a 100" in element:
            list2.append("Maggiore o uguale a 100")
        else:
            list2.append("No limit")
    # List2 contains know all the class of the sample acording to the percentage
    # with the threshold
    
    no_results = len(infofile["N_campione"].tolist()) - \
    len(set(resultfile["N_campione"].tolist()))

    list3 = np.array([list2.count("Tra 0 e 30"), list2.count("Tra 30 e 50"), \
             list2.count("Tra 50 e 80"),list2.count("Tra 80 e 100"), \
             list2.count("Maggiore o uguale a 100"), no_results, list2.count("No limit")])

    # This creates an array with the number of elements in each class
    
    # Create pie chart:
    labels = ["Tra 0 e 30", "Tra 30 e 50", "Tra 50 e 80", "Tra 80 e 100",\
              "Maggiore o uguale a 100", "Nessun risultato", "Senza limiti"]
    colors = ['lightskyblue', 'lightblue', 'cyan',"aquamarine", "coral",\
              "lightgreen", "teal"]
    explode = (0.05, 0.05, 0.05, 0.05, 0.2, 0.05, 0.05)

    fig = plt.figure()
    fig.set_size_inches(18.0, 18.0)
    plt.xticks(rotation='vertical', size=fsize)
    plt.yticks(size=fsize)
    plt.pie(list3, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, \
            pctdistance=0.7, explode=explode, startangle=70)
    
    # title of graph
    if client == "all":
        fig_title = "Occurence of exceeding the limit for all clients in " + str(date) + " font " + str(fsize)
    elif date == "all":
        year1 = years[0]
        year2 = years[-1]
        if year1 == year2:
            fig_title = "Occurence of exceeding the limit for " + client + " in " + str(year1) + " font " + str(fsize)
        else:
            fig_title = "Occurence of exceeding the limit for " + client + " in {}-{}".format(year1, year2) + " font " + str(fsize)
    else:
        fig_title = "Occurence of exceeding the limit for " + client + " in " + str(date) + " font " + str(fsize)
    plt.title(fig_title, fontweight = "bold", size=fsize)
    mpl.rcParams['font.size'] = 22
    
    if detail == True:
        sample_count = {}
        list_samples = resultfile["Gruppo_prodotto"].tolist()
        for element in set(list_samples):
            if not element in sample_count:
                sample_count[element] = list_samples.count(element)
    
        reduced1 = resultfile[resultfile['Classi_Ris_Lim_perc'] == "Maggiore o uguale a 100"]
        reduced2 = sample_count
        reduced3 = client
        reduced4 = date
        over_threshold(reduced1, reduced2, reduced3, reduced4)

    fig_name = "{}.png".format(fig_title)   
    fig.savefig(fig_name, dpi=100, bbox_inches="tight")
    fig_list.append(fig_name)  
    if detail == False:
        return(fig_list) 
    if detail == True:
        return(fig_list, reduced1, reduced2, reduced3, reduced4)


def clients_graph(resultfile, infofile, date = "all", fsize=20): ## 8
    """ This function produces a Graph on clients always, sometimes and never 
    exceeding the limit. 
    
    Variables needed: None, date is optional."""
    fig_list = []

    if date != "all":
        data = resultfile[resultfile["ANNO"] == date]
        infofile = infofile[infofile["ANNO"] == date]
    if date == "all":
        data = resultfile

    client_dic = {1: [], 2: [], 3: []}
    # This dictionary will store the names of the clients. 1: All samples over
    # over the threshold; 2: Some samples over the threshold; 3: No samples
    # over the threshold.
    client_list = [] # This list is just to make sure that no clients are repeated
    for element in set(data["Cliente"].tolist()):
        reduced_data = data[data["Cliente"] == element]
        data_info = infofile[infofile["Cliente"] == element]

        no_results = len(set(data_info["N_campione"].tolist())) - len(set(reduced_data["N_campione"].tolist()))
        if not element in client_list:
            client_list.append(element)
            percentages = reduced_data["Ris_Lim_perc"].dropna().tolist()
            # At this point, we have a list that contains all the percentages
            # (higher than 100 means over the threshold)
            
            per2 = []
            count = 0
            for number in percentages:
                if number != "nan":
                    per2.append(number)
                    if number > 100:
                        count = count + 1
            # This is for each client, count will be the way to see if none, 
            # some, or all elements of per are above the threshold
            
            if no_results == 0:            
                if len(per2) > 0:
                    if count == len(per2):                                
                        client_dic[1].append(element)
                    if count != 0 and count != len(per2):
                        client_dic[2].append(element)
                    if count == 0:
                        client_dic[3].append(element)

            if no_results != 0:            
                if len(per2) > 0:
                    if count == len(per2):                                
                        client_dic[2].append(element)
                    if count != 0 and count != len(per2):
                        client_dic[2].append(element)
                    if count == 0:
                        client_dic[3].append(element)

    # Create the plot:
    explode = (0.1, 0.05, 0.05) 
    labels = ["All samples over threshold", "Some samples over threshold",\
              "No samples over threshold"]
    colors = ['coral', 'gold', 'lightgreen']

    fig = plt.figure()
    fig.set_size_inches(18.0, 18.0)
    plt.pie(np.array([len(client_dic[1]), len(client_dic[2]), len(client_dic[3])]),\
            labels=labels, shadow=True, explode=explode, autopct='%1.1f%%',\
            pctdistance=0.6, colors=colors)

    fig_title = "Occurence of samples exceeding the limit for clients in " + str(date) + " font " + str(fsize)
    plt.title(fig_title, fontweight= "bold", size=fsize)
    mpl.rcParams['font.size'] = 20
    
    fig_name = "{}.png".format(fig_title)   
    fig.savefig(fig_name, dpi=100, bbox_inches="tight")
    fig_list.append(fig_name)  
    
    return(fig_list)

        
def products_of_client(resultfile, client, date = "all", fsize=20):
    """ This function creates a graph on total number of products for a client.
    Variables:
        - Client: compulsory (column Cliente)
        - Date: Optional."""
    fig_list = []

    if date != "all":
        resultfile = resultfile[resultfile["ANNO"] == str(date)]
    
    years = list(set(resultfile["ANNO"].tolist()))
    
    resultfile = resultfile[resultfile["Cliente"] == str(client)]
    
    prod = {}
    for year in years:
        data = resultfile[resultfile["ANNO"] == str(year)]
        for element in data["Gruppo_prodotto"]:
            if not element in prod:
                data2 = data[data["Gruppo_prodotto"] == element]
                # data contains the information for single client and product
                prev = list(set(data2["Prova"].tolist())) # This are the trials
                samples = list(set(data2["N_campione"].tolist())) # This is the number of samples
                prod[element] = [len(samples), len(prev)]
        
        #Create bar chart: 
        sizes = []
        labels = []
        for element in prod:
            sizes.append(prod[element][0])
            labels.append(element)
        
        fig = plt.figure()
        fig.set_size_inches(18.0, 18.0)
        plt.xticks(rotation='vertical', size=fsize)
        plt.yticks(size=fsize)
        plt.bar(range(len(sizes)), sizes, width=0.4, tick_label = labels,\
                color = "lightgreen")

        # title of graph
        if date == "all":
            year1 = years[0]
            year2 = years[-1]
            if year1 == year2:
                fig_title = "Crops analyzed from " + client + " in " + str(year1) + " font " + str(fsize)
            else: 
                fig_title = "Crops analyzes from " + client + " in {}-{}".format(year1, year2) + " font " + str(fsize)
        else:
            fig_title = "Crops analyzed from " + client + " in " + str(date) + " font " + str(fsize)

        plt.title(fig_title, fontweight = "bold", size=fsize)
        mpl.rcParams['font.size'] = 20
        fig_name = "{}.png".format(fig_title)   
        fig.savefig(fig_name, dpi=100)
        fig_list.append(fig_name)  

    return(fig_list)

             
def over_threshold(reducedfile, sample_count, client, date, fsize=20):
    """This function creates detailed information about the samples that are 
    over the threshold. It only apears if detail == True"""
    fig_list = []

    prod = {}
    for element in reducedfile["Prova"]:
        if not element in prod:
            prod[element] = 1
        if element in prod:
            prev = prod[element]
            prod[element] = prev + 1
            
    sizes = []
    labels = []
    sample_sizes = []
    explode = []
    max_labels = heapq.nlargest(20, prod, key=prod.get)
        # It selects the 20 greatest averages
        
    for element in max_labels:
        sizes.append(prod[element])
        labels.append(element)
        explode.append(0.1)
    
    other = 0
    for element in prod:
        if not element in max_labels:
            other = other + prod[element]
    
    colors = ['lightskyblue', 'lightblue', 'cyan', "coral", "gold",\
              "lightcoral", "lavender", "cyan", "lime", "lightgreen","aquamarine"]
    
    if other != 0:
        labels.append("Other")
        sizes.append(other)
        explode.append(0.1)
    
    fig = plt.figure()
    fig.set_size_inches(18.0, 18.0)     
    plt.pie(np.array(sizes), labels=labels, shadow=True, colors=colors, \
            explode=explode, autopct='%1.1f%%', pctdistance=0.8, startangle=150)
    fig_title = "Occurences exceeding the limit per compound for " + client + " in " + str(date) + " font " + str(fsize)
    plt.title(fig_title, fontweight = "bold", size=fsize)
    mpl.rcParams['font.size'] = 20
    fig_name = "{}.png".format(fig_title)   
    fig.savefig(fig_name, dpi=100)
    fig_list.append(fig_name)  
    
    prod = {}
    reduced_list = reducedfile['Gruppo_prodotto'].tolist()
    for element in set(reduced_list):
        if not element in prod:
            prod[element] = reduced_list.count(element)
            
    sizes = []
    labels = []
    max_labels = heapq.nlargest(15, prod, key=prod.get)
        # It selects the 15 greatest averages
    
    for element in max_labels:
        sizes.append(prod[element])
        labels.append(element)
        if element in sample_count:
            sample_sizes.append(sample_count[element])
    
    fig = plt.figure()
    fig.set_size_inches(18.0, 18.0)       
    plt.xticks(rotation='vertical', size=fsize)
    plt.yticks(size=fsize)
    plt.bar(range(len(sizes)), sizes, width=0.4, tick_label = labels,\
            color = "lightgreen")
    for i, v in enumerate(sizes):
        plt.text(i, v+0.25, str(sample_sizes[i]), horizontalalignment='center', \
                 color='darkgreen', fontweight='bold', fontsize = 18)
    plt.ylim(0, max(sizes) + 1)
    plt.ylabel("Number of samples", fontsize = 14)
    fig_title = "Occurences exceeding the limit per product for " + client + " in " + str(date) + " font " + str(fsize)
    plt.title(fig_title, fontweight= "bold", size=fsize)
    mpl.rcParams['font.size'] = 20
    fig_name = "{}.png".format(fig_title)   
    fig.savefig(fig_name, dpi=100, bbox_inches = 'tight')
    fig_list.append(fig_name)  

    return(fig_list)


### HELPER FUNCTIONS
def drop_rows(resultfile):

    dic_todrop = {"Prova":["Grado Rifrattometrico", "Acidita", "Acidità", \
    "Acidita (espr. in ac.citrico)", "Acidità (espr. in ac.citrico)", "Calibro medio",\
    "Durezza", "Durezza totale"], "Gruppo_prodotto": ["NON NORMATO"], "ANNO": ["Totale"],
    "Risultato": ["Presente", "Negativo", "niete da segnalare", "Non determinabile",
    "Non rilevato", "NR", "presente ma minore 4", "Presenti ma <4", "Presenza", "Regolare"]}
    # Contains what we want to erase from the database

    for key in dic_todrop:
        for element in dic_todrop[key]:
            #For all the elements and keys in the dictionary
            if key in resultfile.columns.values.tolist() and element in \
            resultfile[key].tolist():
                # Checks if it is on the file and erase it
                resultfile = resultfile[resultfile[key] != element]
    
    return resultfile