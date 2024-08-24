import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class CreatGraphs:
    def __init__(self, data_frame=pd.DataFrame(), height=int(), margin=dict(), size=int(),
                 title=str(), x=str(), y = str()):
        self.data_frame = data_frame
        self.height = height
        self.margin = margin
        # margin=dict(l=0, r=0, t=27, b=0)
        self.size = size
        self.title = title
        self.x = x
        self.y = y

    def create_bar_chart(self, label_column, bar_color='#1f77b4', background_color='#ffffff'):
        bar_chart = px.bar(self.data_frame, x=self.x, y=self.y, title=self.title, text=label_column,
                           color_discrete_sequence=[bar_color])

        bar_chart.update_yaxes(visible=False)
        bar_chart.update_traces(texttemplate='%{text}', textposition='outside', marker=dict(color=bar_color))
        bar_chart.update_layout(
            height=self.height,
            margin=self.margin,
            showlegend=False,
            font=dict(size=self.size, family="Arial, sans-serif"),
            plot_bgcolor=background_color
        )
        bar_chart.update_xaxes(title='', showgrid=False)

        return bar_chart


    def creat_bar_chart_blank(self, xaxis_name=str(), yaxis_name=str()):
        data = {xaxis_name: list(range(1, 32)),
                yaxis_name: [0] * 31}  # Inicializando todas as distâncias como 0
        df = pd.DataFrame(data)

        bar_chart_black = px.bar(df, x=self.x, y=self.y,
                                       title=self.title)
        bar_chart_black.update_yaxes(visible=False)
        bar_chart_black.update_traces(texttemplate='%{y}', textposition='outside')
        bar_chart_black.update_layout(
            height=self.height,  # Ajustar a altura conforme necessário
            #dict(l=0, r=0, t=27, b=0)
            margin=self.margin,  # Remover margens para ocupar todo o espaço
            showlegend=False,  # Ocultar legenda
            font=dict(size=self.size, family="Arial, sans-serif"),  # Ajustar o tamanho da fonte
        )
        bar_chart_black.update_xaxes(title='', showgrid=False)

        return bar_chart_black


    def create_map_box(self, hover_name=str(), zoom=int, mapbox_style=str, hover_data=None,
                       destacar_primeiro_ultimo=True):
        if hover_data is None:
            hover_data = []

        map_box = px.scatter_mapbox(
            self.data_frame,
            lat=self.x,
            lon=self.y,
            hover_name=hover_name,
            hover_data=hover_data,
            zoom=zoom,
        )

        # Atualizar os marcadores
        map_box.update_traces(marker=dict(size=8), selector=dict(mode='markers'))

        # Destacar o primeiro ponto em verde, o último ponto em vermelho e os demais em azul
        if destacar_primeiro_ultimo:
            primeiro_ponto = self.data_frame.iloc[0]
            ultimo_ponto = self.data_frame.iloc[-1]

            map_box.add_trace(go.Scattermapbox(
                lat=[primeiro_ponto[self.x]],
                lon=[primeiro_ponto[self.y]],
                mode='markers',
                marker=dict(color='green', size=16),
                hoverinfo='text',
                hovertext=self.get_hover_text(primeiro_ponto, hover_data),
            ))

            map_box.add_trace(go.Scattermapbox(
                lat=[ultimo_ponto[self.x]],
                lon=[ultimo_ponto[self.y]],
                mode='markers',
                marker=dict(color='red', size=16),
                hoverinfo='text',
                hovertext=self.get_hover_text(ultimo_ponto, hover_data),
            ))

            # Atualizar as bolinhas intermediárias para azul
            map_box.update_traces(marker=dict(color='blue', size=8), selector=dict(mode='markers', marker='scattermapbox'))

        # Ajustar o layout do mapa e desligar a legenda
        map_box.update_layout(
            mapbox_style=mapbox_style,
            mapbox_center_lon=self.data_frame[self.y].mean(),
            mapbox_center_lat=self.data_frame[self.x].mean(),
            height=self.height,
            margin=self.margin,
            showlegend=False
        )

        return map_box


    def get_hover_text(self, ponto, hover_data):
        hover_texts = [f"{col}: {ponto[col]}" for col in hover_data]
        return "<br>".join(hover_texts)


    def creat_map_box_blanck(self, zoom=int, mapbox_style=str):
        data = {'Lat': [0], 'Long': [0], 'Address': ['']}
        df = pd.DataFrame(data)

        # Criando o mapa em branco
        map_box_blanck = px.scatter_mapbox(
        df,
        lat='Lat',
        lon='Long',
        zoom=zoom,
        )

        # Atualizando os marcadores para torná-los invisíveis
        map_box_blanck.update_traces(marker=dict(color='rgba(0, 0, 0, 0)', size=0), selector=dict(mode='markers'))

        # Ajustando o layout do mapa
        map_box_blanck.update_layout(
        mapbox_style=mapbox_style,
        mapbox_center_lon=0,
        mapbox_center_lat=0,
        height=self.height,  # Ajuste a altura conforme necessário
        margin=self.margin
        )

        return map_box_blanck


    def create_table(self, columns=None):
        if columns is None:
            columns = list(self.data_frame.columns)

        header_values = [column.capitalize() for column in columns]
        header = dict(values=header_values, fill_color='paleturquoise', align='left')

        cells_values = [self.data_frame[column] for column in columns]
        cells = dict(values=cells_values, fill_color='lavender', align='left')

        creat_table = go.Figure(data=[go.Table(header=header, cells=cells)])

        creat_table.update_layout(
            height=self.height,
            # dict(l=0, r=15, t=27, b=0)
            margin= self.margin,
            font=dict(size=self.size)
        )

        return creat_table

    def create_table_blank(self, columns=None):
        # Creating an empty table
        table_data = []

        if columns:
            # Adding columns to the table
            header = go.Table(
                header=dict(values=columns),
                cells=dict(values=[[] for _ in columns])
            )

            table_data.append(header)

        # Creating the figure with the table
        blank_table = go.Figure(data=table_data)

        # Updating the layout of the table
        blank_table.update_layout(
            height=self.height,  # Adjust the height as needed
            margin=self.margin
        )

        return blank_table


