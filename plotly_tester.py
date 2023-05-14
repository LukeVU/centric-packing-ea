import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

data = {
   'x': ['a', 'b', 'c'],
   'y': ['d', 'e', 'f'],
   'z': ['a', 'e', 'i']
}
df = pd.DataFrame(data)

fig = make_subplots(rows=5, cols=7)

for i in range(5):
    for j in range(7):
        fig.add_trace(
            go.Scatter(x=df["x"], y=df["y"], name=f"subplot({i+1}, {j+1})"),
            row=i + 1,
            col=j + 1
        )

fig.update_layout(title="Large Plot with Scrolling",
                  showlegend=False, autosize=True)

fig.show()
