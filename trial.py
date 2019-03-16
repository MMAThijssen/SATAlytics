            prev = data2[data2["Cliente"] == element]
            prev_list = []
            # prev contains the information for single crop, year, compound and client.
            prev2 = prev["Risultato"].astype(str).str.replace(".", "").str.replace(',','.')
            for result_prev in prev2:
                try:
                    prev_list += float(result_prev)
                except ValueError:
                    continue
            if len(prev["Limite"].tolist()) > 0:
                threshold = prev["Limite"].tolist()[0]
            if len(prev["Limite"].tolist()) == 0:
                threshold = "nan"