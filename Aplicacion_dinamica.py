#librerias base
import pandas as pd
import numpy as np
import streamlit as st

#estadistica
import scipy.stats as stats

#graficos
import matplotlib.pyplot as plt
import plotly.express as px
#import rsa
 
st.title('Bienvenidos antes de comenzar escriban la contraseña del QR')




numero = "Arriba_Banca_Digital.2022"

st.text_input("Escribe la contraseña que viene en el QR", key="name")
if str(numero).lower() == st.session_state.name.lower():
    with st.spinner("Por favor espere..."):
        
        #TITULO
        st.title('Informacion del Mes de Agosto')
        
        #SIDE BAR
        #st.sidebar.write("This lives in the sidebar")
        gporta = st.sidebar.selectbox("Como quieres el grafico de portabilidad",("Scatter", "Bar"))
        CA = st.sidebar.selectbox("Escoje que ver en Clientes Activos",("CLIENTES ACTIVOS", "PPTO 2022"))
        TR = st.sidebar.selectbox("Escoje que comparar en Transacciones",("Monetarias", "No Monetarias",'Totales'))
        periodo =st.sidebar.selectbox("Escoge periodo de prediccion NPS BXI",([i for i in range(1,24)]))
        periodo_2 =st.sidebar.selectbox("Escoge periodo de prediccion NPS Movil",([i for i in range(1,24)]))
        


        #st.sidebar.button("Click me!")
        
        
        #INDICADORES
        st.header("Banca Digital")

        col1, col2, col3,col4 = st.columns(4)
        col1.metric("Transacciones", "241M", "-39,607,105")
        col2.metric("Contrataciones", "285,709", "15%")
        col3.metric("Activaciones", "277,311", "44%")
        col4.metric("Ctes. Digitales", "5,091,843", "-7%")


        st.header("PePer")

        col1, col2, col3,col4 = st.columns(4)
        col1.metric("Transacciones Monetarias", "6,387", "+26")
        col2.metric("Transacciones No Monetarias", "49354", "5.1%")
        col3.metric("Usuarios Activos", "11,361", "-3.2%")
        col4.metric("Usuarios Inactivos", "164,035", "1.2%")

        st.header("Apoyos Banorte")
        st.subheader("La caida se debe de acuerdo a las dispersiones que le hace el gobierno a las cuentas de los clientes y en agosto no hubo dispersion")
        col1, col2, col3,col4 = st.columns(4)
        col1.metric("Transacciones Monetarias", "734", "-75%")
        col2.metric("Transacciones No Monetarias", "52,761", "-55%")
        col3.metric("Usuarios Activos", "21,142", "1.2%")
        col4.metric("Usuarios Inactivos", "263,554", "1088")
        
        #GRAFICO 1
        st.subheader("Portabilidad")
        meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto']
        meses_num =[1,2,3,4,5,6,7,8]
        portabilidad =[1740,1861,2020,1793,2335,2386,2549,3158]
        df_porta =pd.DataFrame.from_dict({'Meses':meses,'Meses numericos': meses_num,'Portabilidad':portabilidad})
        
        if gporta == 'Scatter':
            fig_3 = px.scatter(df_porta, x='Meses numericos', y='Portabilidad',trendline='ols')
            fig_3.update_yaxes(range=[0, 3200], autorange=False)

            st.plotly_chart(fig_3, use_container_width=True)
        else:
            fig_3 = px.bar(df_porta, x='Meses', y='Portabilidad')

            st.plotly_chart(fig_3, use_container_width=True)
        
        #GRAFICO 2
        st.subheader("Transacciones por semana, cluster, NombreServicio en porcentaje")
        
        grafico= pd.read_csv('grafico_1.csv')
        data_select = grafico['NOMBRESERVICIO'].isin(['Todas Mis Cuentas'
              ,'Consulta de Información Personal'
              ,'Consulta General De Promociones Vigentes'
              ,'Mis Cuentas con o sin Chequera'
              ,'Consulta de Tracking TDC'
              ,'Activar Token Celular'])
        grafico = grafico[~data_select]
        
        fig = px.bar(grafico.sort_values(by=['SEMANA','percent'], ascending=[True,False]), x='percent',
                     y='CLUSTER',color='NOMBRESERVICIO',animation_frame='SEMANA')
        fig.update_xaxes(range=[0, .05], autorange=False)
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 1000
        st.plotly_chart(fig, use_container_width=True)
    
        #GRAFICO 3
        st.subheader("Distribucion de edades por cluster de uso de la aplicacion")
        df = pd.read_csv('grafico_2.csv', index_col='Unnamed: 0').reset_index()
        df.drop('index', axis=1, inplace=True)

        fig_2 = px.histogram(df, x='EDAD', y='COUNT', color='CLUSTER',
                             histnorm="probability density",animation_frame='SEMANA' )
        st.plotly_chart(fig_2, use_container_width=True)
        #GRAFICO 5
        st.subheader("CLIENTES ACTIVOS")
        
        df_5 = pd.read_csv('salida_1.csv', index_col='Unnamed: 0').reset_index()
        df_5.drop('index', axis=1, inplace=True)
        if CA == 'CLIENTES ACTIVOS':
            fig_5 = px.bar(df_5, x='FECHA', y='CLIENTES ACTIVOS')
            st.plotly_chart(fig_5, use_container_width=True)
        else:
            fig_5 = px.bar(df_5, x='FECHA', y='PPTO 2022')
            st.plotly_chart(fig_5, use_container_width=True)
        
        #GRAFICO 4
        st.subheader("TRANSACCIONES")
        df_4 = pd.read_csv('transaccionales.csv', index_col='Unnamed: 0').reset_index()
        
        df_4.drop('index', axis=1, inplace=True)
        df_4.columns = ['TX  Monetarias presupuesto', 'TX No Monetarias presupuesto', 'TX Totales Presupuesto', 'Mes',
       'Monetarias', 'No Monetarias', 'Total']
        st.dataframe(df_4)
        if TR == 'Monetarias':
            fig_4 = px.scatter(df_4, x='Mes', y=['TX  Monetarias presupuesto','Monetarias'],trendline='ols' )
            st.plotly_chart(fig_4, use_container_width=True)
        elif TR == 'No Monetarias':
            fig_4 = px.scatter(df_4, x='Mes', y=['TX No Monetarias presupuesto','No Monetarias'],trendline='ols' )
            st.plotly_chart(fig_4, use_container_width=True)
        else:
            fig_4 = px.scatter(df_4, x='Mes', y=['TX Totales Presupuesto','Total'],trendline='ols' )
            st.plotly_chart(fig_4, use_container_width=True)
        
        
        #GRAFICO 6
        st.subheader("NPS BXI")
        
        bxi =pd.DataFrame.from_dict({'ds':['01/01/2022','01/02/2022','01/03/2022','01/04/2022'
       ,'01/05/2022','01/06/2022','01/07/2022','01/08/2022'],'y':[82.3,83.5,81.4,82,81,83,84,84.5]})
        bxi['ds'] = pd.to_datetime(bxi ['ds'], format='%d/%m/%Y')
        from prophet import Prophet

        m = Prophet()
        m.fit(bxi)
        data_forecast = m.make_future_dataframe(periods=int(periodo), freq='M')
        forecast = m.predict(data_forecast)
        for_pred= forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
        for_pred.columns=['Fecha','NPS_predicha','NPS_minima','NPS_maxima']
        
        col1_1, col2_1= st.columns(2)
        col1_1.subheader('prediccion')
        col2_1.subheader('Realidad')
        col1_1.dataframe(for_pred)
        bxi.columns=['Fecha','NPS']
        col2_1.dataframe(bxi)
        
        fig_pred_1 = m.plot(forecast)
        fig_pred_1_2 = m.plot_components(forecast)
        st.pyplot(fig_pred_1)#, use_container_width=True)
        st.pyplot(fig_pred_1_2)#, use_container_width=True)
                                      
            
        
        #GRAFICO 7
        st.subheader("NPS Movil")
        
        movil =pd.DataFrame.from_dict({'ds':['01/01/2022','01/02/2022','01/03/2022','01/04/2022'
       ,'01/05/2022','01/06/2022','01/07/2022','01/08/2022'],'y':[80.1,78.2,79,79.3,79.6,81.9,82.1,82.8]})
        movil['ds'] = pd.to_datetime(movil['ds'], format='%d/%m/%Y')
        modelo_2 = Prophet()
        modelo_2.fit(movil)
        
        futuro = modelo_2.make_future_dataframe(periods=periodo_2, freq='M')
        predicciones = modelo_2.predict(futuro)
        for_pred2 = predicciones[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
        for_pred2.columns=['Fecha','NPS_predicha','NPS_minima','NPS_maximas']
        
        col2_1, col2_2= st.columns(2)
        col2_1.subheader('prediccion')
        col2_2.subheader('Realidad')
        col2_1.dataframe(for_pred2)
        bxi.columns=['Fecha','NPS']
        col2_2.dataframe(bxi)
        
        fig_pred_2 = m.plot(predicciones)
        fig_pred_2_2 = m.plot_components(predicciones)
        st.pyplot(fig_pred_2)#, use_container_width=True)
        st.pyplot(fig_pred_2_2)#, use_container_width=True)
        

        
        
        
       
