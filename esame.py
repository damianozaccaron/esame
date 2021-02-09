class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name=name

    def get_data(self):
        #se il nome del file non e' una stringa errore
        if(not isinstance(self.name, str) or self.name == None):
            raise ExamException('Il nome del file deve essere una stringa')
        
        #se non trovo il file
        try:
            my_file=open(self.name,'r')
        except:
            raise ExamException('File non trovato')
        
        #dichiaro la lista risultato
        stats=[]

        for line in my_file:
            elements = line.split(',')

            #se non ci sono solo due elementi nella riga saltala
            if(len(elements) != 2):
                continue
           
            epoch = elements[0]
            temperature = elements[1]

            #se epoch non e' un intero o temperature non e' un numero salto la riga
            try: 
                epoch = int(epoch)
                temperature = float(temperature)
            except: 
                continue

            provv = [epoch,temperature]
            stats.append(provv)

        #se ci sono epoch doppi o non sono ordinati chiudo il file
        for i in range(1,len(stats)):
            if get_epoch(stats[i]) <= get_epoch(stats[i-1]):
                raise ExamException('Trovati epoch doppi o non ordinati')

        if(stats == []):
            raise ExamException('Il file e\' vuoto o non contiene dati leggibili')


        return stats

def daily_stats(time_series):
    #controllo di avergli passato una lisa
    if(not isinstance(time_series,list)):
        raise ExamException("Fornire in input una lista")

    for i in time_series:
        if(not isinstance(i,list) or len(i) != 2):
            raise ExamException("Fornire in input una lista di liste di due elementi")

    #inizializzo il vettore risultati e passo il giorno iniziale, inizializzo un vettore giornaliero
    daily_stats = []
    first_element = time_series[0]
    epoch = first_element[0]
    day_start_epoch = epoch - (epoch % 86400)

    daily_temperatures = []
    last_element = time_series[len(time_series)-1]  

    #analizzo tutti gli elementi della lista uno a uno
    for element in time_series:
        epoch = element [0]
        temperature = element [1]

        #se mi trovo in un giorno diverso dal precedente calcolo le temperature del giorno prima e le aggiungo al risultato
        if(epoch - (epoch % 86400) != day_start_epoch):
            daily_stats.append(calcola_temperature(daily_temperatures))
            
            #svuoto l'array giornaliero e inizializzo un nuovo giorno
            daily_temperatures = []
            day_start_epoch = epoch - (epoch % 86400)
            daily_temperatures.append(temperature)
        
        #altrimenti semplicemente aggiungo alla lista di temperature giornaliere
        else:
            daily_temperatures.append(temperature)
        
        #se questo e' l'ultimo elemento calcolo le temperature dell'ultimo giorno
        if(element == last_element):
            daily_stats.append(calcola_temperature(daily_temperatures))
            
    return daily_stats

#funzione che calcola minima, massima e media giornaliere
def calcola_temperature(daily_temperatures):
    somma = 0
    minima = daily_temperatures[0]
    massima = daily_temperatures[0]
            
    for i in daily_temperatures:
        somma += i
        if(i<minima):
            minima = i
        if(i>massima):
            massima = i
            
    return [minima,massima,somma/len(daily_temperatures)]

#funzione che mi ritorna l'epoch di un determinato elemento
def get_epoch(element):
    return element[0]