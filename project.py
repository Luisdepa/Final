class Project:
    
    def __init__(self,countries,participants,projects):
        #import all three excel data bases
        self.countries = countries
        self.participants= participants
        self.projects=projects

    def annual_grants1(self,participants,projects):
      import pandas as pd
        #unify participants and projects dta base (given the label projectID)
      union = pd.merge(participants, projects, on="projectID", how='inner')
      union
      #now that we have a data base with the years and ecContribution per partener, 
      #we create a group by year, and we are going to sum all the total contibutions per year
      contribution_peryear = union.groupby("year").agg({"ecContribution":"sum"})
      return(contribution_peryear)
  
    def annual_grants2(self,contribution_peryear):
      import streamlit as st
      representacion = st.bar_chart(contribution_peryear )
      #we return it so when we call the function it will give as the representation
      return(representacion)

    def descriptive_statistics(self,participants):
      #use the function describe
      analisis = participants.describe()
      return(analisis)

    def contribution(self,participants,name_country,a = False):
      import pandas as pd
      import streamlit as st
      acronym = {'Belgium': 'BE', 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany':
      'DE', 'Estonia': 'EE', 'Ireland': 'IE','Greece': 'EL', 'Spain': 'ES', 'France': 'FR', 'Croatia':
      'HR', 'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT','Luxembourg': 'LU',
      'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL', 'Portugal':
      'PT','Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE'} 
      acronym = acronym[name_country]
      #filter by the country
      ejercicio = participants[participants["country"]==acronym]
      ejercicio["role"]= ejercicio["role"].map({"coordinator":1,"participant":0,"thirdparty":0})
      #sum of contributions, count the number of times an organization appears and count the number of times it is a coordinator.
      resultado = ejercicio.groupby("name").agg({"ecContribution" : "sum"})
      #modify from our new data frame the columns
      #modify the name of the column ecContribution into Sum_Contribution
      resultado = resultado.rename(columns={"ecContribution":"Sum_Contribution"})
      #linking this new data frame with general participant data, given the vase of the data frame we have created
      prueba = pd.merge(resultado,participants, on="name", how='left')
      #delete duplicates to be left with each case only
      prueba = prueba.groupby("name").first()
      prueba
      #delete columns that we do not need
      #delete column "projectID"
      prueba = prueba.drop(["projectID"], axis=1)
      #delete column "projectAcronym"
      prueba = prueba.drop(["projectAcronym"], axis=1)
      #delete column "organisationID"
      prueba = prueba.drop(["organisationID"], axis=1)
      #delete column "country"
      prueba = prueba.drop(["country"], axis=1)
      #delete column "role"
      prueba = prueba.drop(["role"], axis=1)
      #delete column "ecContribution"
      prueba = prueba.drop(["ecContribution"], axis=1)
      #sort the values of the data frame in descending order of the contribution
      prueba = prueba.drop(["index"], axis=1)
      prueba = prueba.sort_values("Sum_Contribution",ascending=False)     
      if a == False:
          escrito = st.subheader("Participants in {}".format(name_country)) 
          return(escrito,st.write(prueba))
      else:
          return(prueba)
   
#aportación del pais por año   

    def aportacion(self,participants,projects,name_country):
        import pandas as pd
        import streamlit as st
        acronym = {'Belgium': 'BE', 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany':
       'DE', 'Estonia': 'EE', 'Ireland': 'IE','Greece': 'EL', 'Spain': 'ES', 'France': 'FR', 'Croatia':
       'HR', 'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT','Luxembourg': 'LU',
       'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL', 'Portugal':
       'PT','Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE'} 
        acronym = acronym[name_country]
        fusion = pd.merge(participants, projects, on="projectID", how='inner')
        resultado = fusion[fusion["country"]==acronym]
        resultado = resultado.groupby("year").agg({"ecContribution":"sum"})
        title = st.header("Total ecContribution per year in {}".format(name_country))
        representacion = st.bar_chart(resultado)
        return(title,representacion)

    def coordinators(self,participants,name_country,a = False):
       import pandas as pd
       import streamlit as st
       #once we have the name of the country start the process
       #find the country acronym
       #Dictionary with the name of the countroes
       acronym = {'Belgium': 'BE', 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany':
       'DE', 'Estonia': 'EE', 'Ireland': 'IE','Greece': 'EL', 'Spain': 'ES', 'France': 'FR', 'Croatia':
       'HR', 'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT','Luxembourg': 'LU',
       'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL', 'Portugal':
       'PT','Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE'} 
       acronym = acronym[name_country]
       #filter by the country
       ejercicio = participants[participants["country"]==acronym]
       #we began the process of counting the number of times the organization has been a coordinator.
       #modify the role column if it is coordinator 1, otherwise 0
       ejercicio["role"]= ejercicio["role"].map({"coordinator":1,"participant":0,"thirdparty":0})
       ejercicio
       #sum of contributions, count the number of times an organization appears and count the number of times it is a coordinator.
       resultado = ejercicio.groupby("name").agg({"role":"sum"})
       #modify from our new data frame the columns
       #modify the name of the column role into Number_of_times_Coordinating
       resultado = resultado.rename(columns={"role":"Number_of_times_Coordinating"})
       #linking this new data frame with general participant data, given the vase of the data frame we have created
       prueba = pd.merge(resultado,participants, on="name", how='left')
       #delete duplicates to be left with each case only
       prueba = prueba.groupby("name").first()
       prueba
       #delete columns that we do not need
       #delete column "projectID"
       prueba = prueba.drop(["projectID"], axis=1)
       #delete column "projectAcronym"
       prueba = prueba.drop(["projectAcronym"], axis=1)
       #delete column "organisationID"
       prueba = prueba.drop(["organisationID"], axis=1)
       #delete column "country"
       prueba = prueba.drop(["country"], axis=1)
       #delete column "role"
       prueba = prueba.drop(["role"], axis=1)
       #delete column "ecContribution"
       prueba = prueba.drop(["ecContribution"], axis=1)
       prueba = prueba.drop(["index"], axis=1)
       prueba = prueba.drop(["organizationURL"], axis=1)
       prueba = prueba[prueba["Number_of_times_Coordinating"]>0]
       #sort the values of the data frame in descending order of the contribution
       prueba = prueba.sort_values("shortName",ascending=True) 
       if a == False:
           escrito = st.subheader("Coordinators in {}".format(name_country)) 
           return(escrito,st.write(prueba))  
       else:
           return(prueba)
       







